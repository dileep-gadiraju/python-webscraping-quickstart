import os
from pathlib import Path
from threading import Lock

import config
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

chrome_path = Service(config.CHROMEDRIVER_PATH)
chrome_lock = Lock()


def get_proxy_addr(country):
    with open(config.PROXY_FILE, 'r') as proxylist:
        proxy_list = yaml.safe_load(proxylist)['proxies']
    data = proxy_list.get(country, None)
    if data is None:
        proxy_url = None
    else:
        proxy_url = data.get('URL', None)
        del data, proxy_list
        if proxy_url is not None:
            proxy_url = 'http://{0}'.format(proxy_url)
    return proxy_url


def enable_download_headless(browser, download_dir):
    browser.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {
        'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)


def get_driver(temp_directory, agentcontext):
    # start lock
    chrome_lock.acquire(timeout=60)

    # Set Directory
    Path(temp_directory).mkdir(parents=True, exist_ok=True)
    download_dir = os.path.join(temp_directory)

    # Chrome Capibilities
    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = {'browser': 'ALL'}

    # Chrome Options
    chrome_options = Options()
    # enable proxy
    if hasattr(agentcontext, 'proxy'):
        proxy_addr = get_proxy_addr(agentcontext.proxy)
        if proxy_addr is not None:
            chrome_options.add_argument(
                "--proxy-server={0}".format(proxy_addr))
    # to run without a UI or display server dependencies.
    chrome_options.add_argument("--headless")
    # to set windows size to the specified values
    chrome_options.add_argument("--window-size=1920x1080")
    # to disable the unwanted browser notifications
    chrome_options.add_argument("--disable-notifications")
    # to disables sandbox mode for all processes means browser-level switch for testing purposes only.
    chrome_options.add_argument('--no-sandbox')
    # to disable verbose logging for the ChromeDriver executable
    chrome_options.add_argument('--verbose')
    # to set the minimum log level.
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled")
    # to disables GPU hardware acceleration.
    chrome_options.add_argument('--disable-gpu')
    # The /dev/shm partition is too small in certain VM environments, causing Chrome to fail or crash.
    chrome_options.add_argument('--disable-dev-shm-usage')
    # A string used to override the default user agent with a custom one.
    chrome_options.page_load_strategy = 'normal'
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": str(download_dir),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False,
        "plugins.always_open_pdf_externally": True
    })

    # driver initialization with capibilities and options
    driver = webdriver.Chrome(
        service=chrome_path, options=chrome_options, desired_capabilities=d)
    enable_download_headless(driver, download_dir)

    # release lock
    chrome_lock.release()
    return driver
