import pytest
import sqlite3
from collections import defaultdict

from testmon.process_code import Module, encode_lines
from testmon.testmon_core import (
    TestmonData as CoreTestmonData,
    SourceTree,
    flip_dictionary,
    checksums_to_blob,
    CHECKUMS_ARRAY_TYPE,
    is_python_file,
    TestmonConfig,
    check_mtime,
    split_filter,
    check_fingerprint,
    check_checksum,
    get_new_mtimes,
)


pytest_plugins = ("pytester",)

from array import array


def make_testmon_testdata(node_data, environment="default"):
    td = CoreTestmonData(rootdir="", environment=environment)

    for node, files in node_data.items():
        for filename in files:
            td.source_tree.cache[filename] = Module(
                "", file_name=filename, mtime=1.0, checksum="100"
            )

        td.write_node_data(node, files, {})

    td.determine_stable()
    return td


class TestMisc(object):
    def test_is_python_file(self):
        assert is_python_file("/dir/file.py")
        assert is_python_file("f.py")
        assert not is_python_file("/notpy/file.p")

    def test_flip(self):
        node_data = {"X": {"a": [1, 2, 3], "b": [3, 4, 5]}, "Y": {"b": [3, 6, 7]}}
        files = flip_dictionary(node_data)
        assert files == {"a": {"X": [1, 2, 3]}, "b": {"X": [3, 4, 5], "Y": [3, 6, 7]}}


    def test_sqlite_assumption_foreign_key(self, testdir):
        n1_node_data = {"test_a.py::n1": {"test_a.py": encode_lines(["1"])}}
        td = make_testmon_testdata(n1_node_data)
        con = td.connection
        first_nodeid = con.execute("SELECT id FROM node").fetchone()[0]
        td.write_node_data("test_a.py::n1", {"test_a.py": encode_lines(["1"])})
        second_nodeid = con.execute("SELECT max(id) FROM node").fetchone()[0]
        assert first_nodeid != second_nodeid
        assert (
            con.execute(
                "SELECT count(*) FROM node_fingerprint where node_id = ?",
                (first_nodeid,),
            ).fetchone()[0]
            == 0
        )
        assert (
            con.execute(
                "SELECT count(*) FROM node_fingerprint where node_id = ?",
                (second_nodeid,),
            ).fetchone()[0]
            == 1
        )
        td.connection.execute("DELETE FROM node")
        assert (
            td.connection.execute("SELECT count(*) from node_fingerprint").fetchone()[0]
            == 0
        )


class TestData:
    def test_read_nonexistent(self, testdir):
        td = CoreTestmonData(testdir.tmpdir.strpath, "V2")
        assert td._fetch_attribute("1") == None

    def test_write_read_attribute(self, testdir):
        td = CoreTestmonData(testdir.tmpdir.strpath, "V1")
        td._write_attribute("1", {"a": 1})
        td2 = CoreTestmonData(testdir.tmpdir.strpath, "V1")
        assert td2._fetch_attribute("1") == {"a": 1}

    def test_write_read_nodedata(self, testdir):
        n1_node_data = {"test_a.py::n1": {"test_a.py": encode_lines(["1"])}}
        td = make_testmon_testdata(n1_node_data)
        assert td.all_nodes == {"test_a.py::n1": {}}
        assert td.all_files == {"test_a.py"}

    def test_filenames_fingerprints(self, testdir):
        td = CoreTestmonData(testdir.tmpdir.strpath)
        fs = SourceTree(testdir.tmpdir.strpath)
        td.source_tree = fs
        fs.cache["test_1.py"] = Module(
            "", file_name="test_1.py", mtime=1000.0, checksum="500"
        )

        td.write_node_data(
            "test_1.py::test_1", {"test_1.py": encode_lines("FINGERPRINT1")}, {}
        )

        assert tuple(td.filenames_fingerprints[0]) == ("test_1.py", 1000.0, "500", 1)

    def test_basic(self, testdir):
        td = CoreTestmonData(testdir.tmpdir.strpath)
        fs = SourceTree("")
        td.source_tree = fs
        fs.cache["test_1.py"] = Module("", file_name="test_1.py", checksum="500")

        td.write_node_data(
            "test_1.py::test_1", {"test_1.py": encode_lines(["FINGERPRINT1"])}, {}
        )

        node_data = td.get_changed_file_data({1})

        assert node_data == [
            ("test_1.py", "test_1.py::test_1", encode_lines(["FINGERPRINT1"]), 1)
        ]

    def test_determine_stable_flow(self, testdir):
        td = make_testmon_testdata(
            {"test_1.py::test_1": {"test_1.py": encode_lines(["FINGERPRINT1"])}}
        )

        td.source_tree.cache["test_1.py"].mtime = 1100.0
        td.source_tree.cache["test_1.py"].checksum = "600"
        td.source_tree.cache["test_1.py"].fingerprint = "FINGERPRINT2"

        filenames_fingerprints = td.filenames_fingerprints

        assert tuple(filenames_fingerprints[0]) == ("test_1.py", 1.0, "100", 1)

        _, mtime_misses = split_filter(
            td.source_tree, check_mtime, filenames_fingerprints
        )

        checksum_hits, checksum_misses = split_filter(
            td.source_tree, check_checksum, mtime_misses
        )

        changed_files = {checksum_miss[3] for checksum_miss in checksum_misses}

        assert changed_files == {1}

        changed_file_data = td.get_changed_file_data(changed_files)

        assert changed_file_data == [
            ("test_1.py", "test_1.py::test_1", encode_lines(["FINGERPRINT1"]), 1)
        ]

        hits, misses = split_filter(
            td.source_tree, check_fingerprint, changed_file_data
        )
        assert misses == changed_file_data

    def test_garbage_retain_stable(self, testdir):
        td = make_testmon_testdata(
            {"test_1.py::test_1": {"test_1.py": encode_lines(["FINGERPRINT1"])}}
        )

        td.sync_db_fs_nodes(retain=set())
        assert set(td.all_nodes) == {"test_1.py::test_1"}

    def test_write_data2(self, testdir):
        td = make_testmon_testdata({})

        node_data = {
            "test_1.py::test_1": {
                "a.py": encode_lines(["FA"]),
                "test_1.py": encode_lines(["F1"]),
            },
            "test_1.py::test_2": {
                "a.py": encode_lines(["FA2"]),
                "test_1.py": encode_lines(["F1"]),
            },
            "test_1.py::test_3": {"a.py": encode_lines(["FA"])},
        }

        td.sync_db_fs_nodes(set(node_data.keys()))
        td = make_testmon_testdata(node_data)

        result = defaultdict(dict)

        for filename, node_name, fingerprint, id in td.get_changed_file_data(
            set(range(10))
        ):
            result[node_name][filename] = fingerprint
        assert result == node_data
        td.close_connection()

        change = {
            "test_1.py::test_1": {
                "a.py": encode_lines(["FA2"]),
                "test_1.py": encode_lines(["F1"]),
            }
        }

        node_data.update(change)
        td = make_testmon_testdata(
            {
                "test_1.py::test_1": {
                    "a.py": encode_lines(["FA2"]),
                    "test_1.py": encode_lines(["F1"]),
                }
            }
        )

        for filename, node_name, fingerprint, id in td.get_changed_file_data(
            set(range(10))
        ):
            result[node_name][filename] = fingerprint
        assert result == node_data

    def test_collect_garbage(self, testdir):
        td = make_testmon_testdata(
            {"test_1.py::test_1": {"test_1.py": encode_lines(["FINGERPRINT1"])}}
        )

        td.source_tree.cache["test_1.py"].mtime = 1100.0
        td.source_tree.cache["test_1.py"].checksum = 600
        td.source_tree.cache["test_1.py"].fingerprint = "FINGERPRINT2"

        td.determine_stable()
        assert set(td.all_nodes)
        td.sync_db_fs_nodes(retain=set())
        td.close_connection()

        td2 = CoreTestmonData("")
        td2.determine_stable()
        assert set(td2.all_nodes) == set()

    def test_remove_unused_fingerprints(self, testdir):
        n1_node_data = {"test_a.py::n1": {"test_a.py": encode_lines(["1"])}}
        td = make_testmon_testdata(n1_node_data)

        td.source_tree.cache["test_a.py"] = None
        td.determine_stable()

        td.sync_db_fs_nodes(set())
        td.remove_unused_fingerprints()

        c = td.connection
        assert c.execute("SELECT * FROM fingerprint").fetchall() == []


class TestCoreTestmon:
    def test_check_mtime(self):
        fs = SourceTree("")
        fs.cache["test_a.py"] = Module(
            "", file_name="test_a.py", mtime=1, checksum=1000
        )

        assert check_mtime(fs, {"file_name": "test_a.py", "mtime": 1})
        assert not check_mtime(fs, {"file_name": "test_a.py", "mtime": 2})
        pytest.raises(Exception, check_mtime, fs, ("test_a.py",))

    def test_check_checksum(self):
        fs = SourceTree("")
        fs.cache["test_a.py"] = Module(
            "", file_name="test_a.py", mtime=1, checksum=1000
        )
        assert check_checksum(fs, {"file_name": "test_a.py", "checksum": 1000})
        assert check_checksum(fs, {"file_name": "test_a.py", "checksum": 1001}) is False
        assert pytest.raises(
            Exception, check_checksum, fs, {"file_name": "test_a.py", "bla": None}
        )

    def test_mtime_filter(self):
        fs = SourceTree("")
        fs.cache["test_a.py"] = Module(
            "", file_name="test_a.py", mtime=1, checksum=1000
        )

        record = {"file_name": "test_a.py", "mtime": 1}
        assert split_filter(fs, check_mtime, (record,)) == ([record], [])

        record2 = {"file_name": "test_a.py", "mtime": 2}
        assert split_filter(fs, check_mtime, (record2,)) == ([], [record2])

    def test_split_filter(self):
        assert split_filter(None, lambda disk, x: x == 1, (1, 2)) == ([1], [2])

    def test_get_new_mtimes(self, testdir):
        a_py = testdir.makepyfile(
            a="""
                def test_a():
                    return 0
                """
        )
        fs = SourceTree(testdir.tmpdir.strpath)

        assert next(get_new_mtimes(fs, (("a.py", None, None, 2),))) == (
            a_py.mtime(),
            "de226b260917867990e4fb7aac70c5d6582266d4",
            2,
        )



class TestSourceTree:
    def test_get_file(self, testdir):
        a_py = testdir.makepyfile(
            a="""
                def test_a():
                    return 0
        """
        )
        fs_data = SourceTree(rootdir=testdir.tmpdir.strpath)
        module = fs_data.get_file("a.py")
        assert module.mtime == a_py.mtime()
        assert module.checksum == "de226b260917867990e4fb7aac70c5d6582266d4"

    def test_nonexistent(self, testdir):
        file_system = SourceTree(rootdir=testdir.tmpdir.strpath)
        assert file_system.get_file("jdslkajfnoweijflaohdnoviwn.py") is None


class TestTestmonConfig:
    @pytest.fixture
    def testmon_config(self):
        return TestmonConfig()

    @pytest.fixture()
    def options(self):
        return {
            "testmon": False,
            "testmon_noselect": False,
            "testmon_nocollect": False,
            "testmon_forceselect": False,
            "no-testmon": False,
            "keyword": "",
            "markexpr": "",
            "lf": False,
        }

    def test_easy(self, testmon_config, options):
        options["testmon"] = True
        assert testmon_config._header_collect_select(options) == (
            "testmon: ",
            True,
            True,
        )

    def test_empty(self, testmon_config, options):
        options["testmon"] = None
        assert testmon_config._header_collect_select(options) == (None, False, False)

    def test_dogfooding(self, testmon_config, options):
        options["testmon"] = True
        assert testmon_config._header_collect_select(
            options, dogfooding=True, debugger=True
        ) == ("testmon: ", True, True)

    def test_noselect(self, testmon_config, options):
        options["testmon_noselect"] = True
        assert testmon_config._header_collect_select(options) == (
            "testmon: selection deactivated, ",
            True,
            False,
        )

    def test_noselect_trace(self, testmon_config, options):
        options["testmon_noselect"] = True
        assert testmon_config._header_collect_select(options, debugger=True) == (
            "testmon: collection automatically deactivated because it's not compatible with debugger, selection deactivated, ",
            False,
            False,
        )

    def test_nocollect_minus_k(self, testmon_config, options):
        options["keyword"] = "test1"
        options["testmon_nocollect"] = True
        assert testmon_config._header_collect_select(options) == (
            "testmon: collection deactivated, selection automatically deactivated because -k was used, ",
            False,
            False,
        )
