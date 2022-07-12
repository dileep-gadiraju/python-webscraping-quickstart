import os
from pathlib import Path
from threading import Lock

import config
import yaml
from seleniumwire import webdriver
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
        proxy_username = data.get('username', None)
        proxy_password = data.get('password', None)
        del data, proxy_list
        if proxy_url is None:
            proxy_url = ''
        elif proxy_username is None or proxy_password is None:
            proxy_url = 'https://'+proxy_url
        else:
            proxy_url = 'https://{0}:{1}@{2}'.format(
                proxy_username, proxy_password, proxy_url)
    return proxy_url


def enable_download_headless(browser, download_dir):
    browser.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {
        'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)


def get_driver(temp_directory, agentContext):
    # start lock
    chrome_lock.acquire(timeout=60)

    # Set Directory
    Path(temp_directory).mkdir(parents=True, exist_ok=True)
    download_dir = os.path.join(temp_directory)

    # Chrome Capibilities
    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = {'browser': 'ALL'}

    # seleniumwire_option -> proxy server
    if hasattr(agentContext, 'proxy'):
        proxy_addr = get_proxy_addr(agentContext.proxy)
        print('proxy_addr->', proxy_addr)
        if proxy_addr is not None:
            wire_option = {
                'proxy': {
                    'http': proxy_addr,
                    'https': proxy_addr,
                    'no_proxy': 'localhost,127.0.0.1'
                }
            }

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--verbose')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
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
    driver = webdriver.Chrome(
        service=chrome_path, options=chrome_options, desired_capabilities=d)
    enable_download_headless(driver, download_dir)

    # release lock
    chrome_lock.release()
    return driver
