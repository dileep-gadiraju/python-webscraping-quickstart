import os
import time
import traceback
import config

from common import Log, get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def NoScripts(agentRunContext):
    log = Log(agentRunContext)

    log.job(config.JOB_COMPLETED_SUCCESS_STATUS,
            'Script Not Available')
