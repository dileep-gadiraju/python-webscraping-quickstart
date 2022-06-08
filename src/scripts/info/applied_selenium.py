import os
import time
import traceback
import config

from common import Log, get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def AppliedSelenium(agentRunContext):
    log = Log(agentRunContext)
    try:

        url = 'https://www.applied.com/search?q=:relevance:FTS:' + \
            agentRunContext.requestBody['search'] + \
            '&page=<page>&search-category=all&override=true&isLevelUp=false'
        download_dir_id = str(agentRunContext.jobId)
        download_dir = os.path.join(
            os.getcwd(), 'temp', 'temp-' + download_dir_id)

        driver = get_driver(download_dir)
        driver.maximize_window()

        driver.get(url)
        wait = WebDriverWait(driver, 20)
        log.job(config.JOB_RUNNING_STATUS, 'Job Started')

        try:
            wait.until(EC.element_to_be_clickable(
                (By.ID, "CybotCookiebotDialogBodyButtonAccept")))
            driver.find_element_by_id(
                "CybotCookiebotDialogBodyButtonAccept").click()
        except:
            pass
        for page_no in range(1, 1000):
            driver.get(url.replace('<page>', str(page_no)))
            time.sleep(2)

            wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'product-list')))

            for item in driver.find_elements_by_xpath('//a[@itemprop="url"][.="View more details"]'):
                href = item.get_attribute('href')
                driver.switch_to.new_window()
                driver.get(href)
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))

                item_dict = {
                    'brand': driver.find_element_by_tag_name('h1').text.strip(),
                    'name': driver.find_element_by_xpath('//*[@itemprop= "mpn name"]').text.strip(),
                    'details': driver.find_element_by_class_name('details').text.strip(),
                    'item_no': driver.find_element_by_class_name('customer-part-number').text.strip(),
                    'company': driver.find_element_by_xpath('//h1[@itemprop="brand"]/a').text.strip(),
                    'product': driver.find_element_by_xpath('//span[@itemprop="mpn name"]').text.strip(),
                    'details': driver.find_element_by_xpath('//div[@class="details"]').text.strip(),
                    'item': driver.find_element_by_xpath('//div[@class="customer-part-number"]').text.strip()
                }

                try:
                    item_dict['short_description'] = list()
                    des = driver.find_element_by_class_name('short-description')
                    for ele in des.find_elements_by_xpath('.//li'):
                        item_dict['short_description'].append(ele.text.strip())
                except:
                    log.info('info', 'No Short-Description Available for {0}'.format(item_dict['brand']))

                try:
                    item_dict['specification'] = dict()
                    spe = driver.find_element_by_id('specifications')
                    for table in spe.find_elements_by_xpath('.//table'):
                        for tr_ele in table.find_elements_by_xpath('./tbody/tr'):
                            key = str(tr_ele.find_element_by_xpath(
                                './td[1]').text).strip()
                            value = str(tr_ele.find_element_by_xpath(
                                './td[2]').text).strip()
                            item_dict['specification'][key] = value
                except:
                    log.info('info', 'No Specification Available for {0}'.format(item_dict['brand']))

                try:
                    log.data(item_dict)
                except:
                    pass
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            
            if 'page' not in driver.current_url:
                break
        
        log.job(config.JOB_COMPLETED_SUCCESS_STATUS,
                'Successfully scraped all data')
    except Exception as e:
        log.job(config.JOB_COMPLETED_FAILED_STATUS, str(e))
        log.info('exception', traceback.format_exc())

    driver.quit()
