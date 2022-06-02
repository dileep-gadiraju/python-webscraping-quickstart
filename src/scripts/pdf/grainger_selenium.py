import os
import shutil
import time
import traceback


import config
from common import Log, get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def single_product(log, driver, download_dir, new_output_dir, win_handle=2):
    try:
        doc_section = driver.find_elements(
            By.XPATH, '//ul[@class="documentation__content"]//li')
        for link in doc_section:
            download_link = link.find_element_by_tag_name(
                'a').get_attribute('href')
            product_name = str(driver.current_url).split('-')[-1].strip()
            try:
                product_name = product_name.split('-')[-1].split('?')[:1][0]
            except:
                pass
            driver.switch_to.new_window()
            driver.get(download_link)
            time.sleep(5)

            file_name = os.listdir(download_dir)[0]
            new_file_name = product_name + "-" + file_name
            os.rename(os.path.join(download_dir, file_name),
                      os.path.join(download_dir, new_file_name))

            shutil.move(os.path.join(download_dir, new_file_name),
                        os.path.join(new_output_dir, new_file_name))

            log.info('info', '{0} Downloaded'.format(new_file_name))

            time.sleep(2)
            driver.close()
            driver.switch_to.window(driver.window_handles[win_handle])
    except Exception as e:
        log.info('exception', traceback.format_exc())


def multi_product(log, wait, driver, download_dir, new_output_dir):
    # Collecting details for all products available
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//div[@class = "multi-tiered-category"]')))
    all_product = driver.find_elements_by_xpath(
        '//div[@class = "multi-tiered-category"]//ul//li/a')

    all_product = [i.get_attribute('href') for i in all_product]

    c_url = driver.current_url

    for p_url in all_product:
        driver.switch_to.new_window()
        driver.get(p_url)
        time.sleep(2)

        try:
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//div[@id="feedbackBrowseModal"]//div[@class="modal-footer"]//a[@class = "close"]')))
            driver.find_element_by_xpath(
                '//div[@id="feedbackBrowseModal"]//div[@class="modal-footer"]//a[@class = "close"]').click()
            time.sleep(2)
        except:
            pass

        for a_tag in driver.find_elements(By.XPATH, "//tbody//a"):
            product_url = str(a_tag.get_attribute('href'))
            driver.switch_to.new_window()
            driver.get(product_url)
            time.sleep(2)
            single_product(log, driver, download_dir, new_output_dir)
            driver.close()
            driver.switch_to.window(driver.window_handles[1])

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.get(c_url)
        time.sleep(5)


def GraingerSelenium(agentRunContext):
    log = Log(agentRunContext)
    try:
        download_dir_id = str(agentRunContext.jobId)
        download_dir = os.path.join(
            os.getcwd(), 'temp', 'temp-' + download_dir_id)

        # Creating an output directory for storing PDFs
        try:
            os.mkdir(os.path.normpath(os.getcwd() +
                                      os.sep + os.pardir) + '\\output')
        except:
            pass
        output_dir = os.path.normpath(
            os.getcwd() + os.sep + os.pardir) + '\\output\\'
        os.mkdir(output_dir + download_dir_id)
        new_output_dir = os.path.join(output_dir, download_dir_id)

        driver = get_driver(download_dir)
        driver.maximize_window()
        driver.get(agentRunContext.URL)

        wait = WebDriverWait(driver, 20)

        log.job(config.JOB_RUNNING_STATUS, 'Job Started')

        # Inputing Search-Param
        driver.find_element_by_xpath(
            '//input[@aria-label="Search Query"]').send_keys(agentRunContext.requestBody['search'])
        time.sleep(2)
        driver.find_element_by_xpath(
            '//button[@aria-label="Submit Search Query"]').click()
        time.sleep(5)

        # If multi_products are there in search params
        if len(driver.find_elements(By.XPATH, '//div[@class = "multi-tiered-category"]')) > 0:
            multi_product(log, wait, driver, download_dir, new_output_dir)
        # If single_products are there in search params
        else:
            single_product(log, driver, download_dir, new_output_dir, 0)

        log.job(config.JOB_RUNNING_STATUS, 'Downloaded All Invoices')

    except Exception as e:
        log.job(config.JOB_COMPLETED_FAILED_STATUS, str(e))
        log.info('exception', traceback.format_exc())

    driver.quit()
