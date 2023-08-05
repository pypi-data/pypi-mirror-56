import pytest
import coverage

pytest_plugins = ("pytester",)


# #ifdef PYTEST_COV
class TestPytestCovAssumptions:
    class Plugin:
        def pytest_configure(self, config):
            cov_plugin = config.pluginmanager.get_plugin("_cov")
            self.cov_active = bool(cov_plugin and cov_plugin._started)

    def test_inactive(self, testdir):
        plugin = self.Plugin()
        testdir.runpytest_inprocess("", plugins=[plugin])
        assert plugin.cov_active == False

    @pytest.mark.filterwarnings("ignore:")
    def test_active(self, testdir):
        plugin = self.Plugin()

        testdir.runpytest_inprocess("--cov=.", plugins=[plugin])
        assert plugin.cov_active == True

    def test_specify_include(self, testdir):
        testdir.makepyfile(lib="""
        Ahoj
        bka
        # #
        """
                               )

        cov = coverage.Coverage(
            data_file=None, config_file=False, include=[testdir.tmpdir.strpath]
        )
        cov.start()
        cov.stop()
        assert [] == cov.get_data().measured_files()

    @pytest.mark.xfail  # specifying source=".", searches for all python files in that directory and adds them
    # to measured_files(), cov.get_data() calls cov._post_save_work() which searches all py files in the source dir
    def test_specify_source(self, testdir):
        testdir.makepyfile(lib="")

        cov = coverage.Coverage(data_file=None, config_file=False, source=["."])
        cov.start()
        cov.stop()
        assert [] == cov.get_data().measured_files()
