import pytest, yaml
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

with open("./testdata.yaml", encoding='utf-8') as f:
    testdata = yaml.safe_load(f)
    browser = testdata["browser"]

S = requests.Session()

@pytest.fixture(scope="session")
def browser():
    if browser == "firefox":
        service = Service(executable_path=GeckoDriverManager().install())
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(service=service, options=options)
    else:
        service = Service(executable_path=ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


@pytest.fixture()
def user_login():
    result = S.post(url=testdata['url'], data={'username': testdata['your_login'], 'password': testdata['your_password']})
    response_json = result.json()
    token = response_json.get('token')
    return token


@pytest.fixture()
def post_title():
    return 'Мои мечты'


# Фикстура для создания нового поста
@pytest.fixture()
def new_post_data():
    return testdata['new_post']