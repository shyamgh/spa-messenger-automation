import pytest
from utils.test_base import APP_URL
from pages.selenium_base import screenshot_list


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        
        # add url to report
        extra.append(pytest_html.extras.url(APP_URL))
        xfail = hasattr(report, "wasxfail")

        # append failure screenshots to report
        if (report.skipped and xfail) or (report.failed and not xfail):            
            for screenshot in screenshot_list:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screenshot
                extra.append(pytest_html.extras.html(html))
        report.extra = extra
