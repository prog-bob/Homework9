import pytest
import paramiko
from selenium import webdriver
import allure
import json
from pages.adminpage import AdminPage

def pytest_addoption(parser):
    # Opencart docker container options
    # get address from the "docker inspect vl_opencart_1 | grep IPAddress"
    parser.addoption("--host", action="store", default="192.168.1.44")
    parser.addoption("--port", action="store", default="22")
    parser.addoption("--username", action="store", default="vllobov")
    parser.addoption("--password", action="store", default="111")
    # Selenoid options
    parser.addoption("--browser", default="firefox")
    # parser.addoption("--executor", default="192.168.1.44")
    parser.addoption("--executor", default="localhost")
    parser.addoption("--bversion", action="store", default="83.0")
    parser.addoption("--vnc", action="store_true", default=True)
    parser.addoption("--logs", action="store_true", default=False)
    parser.addoption("--video", action="store_true", default=False)


@pytest.fixture
def ssh(request) -> paramiko.SSHClient:
    """
    Работа с SSH.
    :param request:
    :return:
    """
    host = request.config.getoption("--host")
    port = request.config.getoption("--port")
    username = request.config.getoption("--username")
    password = request.config.getoption("--password")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, port=port, username=username, password=password)

    yield ssh
    ssh.close()

@pytest.fixture
def sftp(request, ssh) -> paramiko.SFTPClient:
    """
    Работа с SFTP.
    :param request:
    :return:
    """
    sftp = ssh.open_sftp()

    yield sftp
    sftp.close()


@pytest.fixture(scope="module")
def url(request):
    return request.config.getoption("--url")


@pytest.fixture(scope="module")
def driver_path(request):
    return request.config.getoption("--driver_path")


@pytest.fixture
def remote_browser(request):
    browser = request.config.getoption("--browser")
    vnc = request.config.getoption("--vnc")
    video = request.config.getoption("--video")
    version = request.config.getoption("--bversion")
    executor = request.config.getoption('--executor')
    executor_url = f"http://{executor}:4444/wd/hub"

    print(browser)
    print(executor_url)

    caps = {
        "browserName": browser,
        "browserVersion": version,
        "selenoid:options": {
            "enableVNC": vnc,
            "enableVideo": video,
        },
        "name": "V.Lobov"
    }

    driver = webdriver.Remote(
        desired_capabilities=caps,
        command_executor=executor_url
    )

    # Attach browser data
    allure.attach(
        name=driver.session_id,
        body=json.dumps(driver.desired_capabilities),
        attachment_type=allure.attachment_type.JSON)

    yield driver
    driver.quit()


@pytest.fixture()
def admin_page(remote_browser):
    page = AdminPage(remote_browser)
    page.go_to("http://127.0.0.1")
    return page


