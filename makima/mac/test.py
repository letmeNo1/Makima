import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait

cap = DesiredCapabilities.CHROME.copy()
cap['goog:chromeOptions'] = {'binary':"/Applications/Jabra Direct.app/Contents/MacOS/Jabra Direct"
                             ,'args':['--remote-debugging-port=7070']}
driver = webdriver.Remote(command_executor="http://127.0.0.1:9515",desired_capabilities=cap)
# time.sleep(340000)
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "items")))
#
# driver.find_element(By.ID, 'items').click()
# windows = driver.window_handles
# print(windows)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'tray-list-empty-button')))

driver.find_element(By.CLASS_NAME, 'tray-list-empty-button').click()
windows = driver.window_handles
driver.switch_to.window(windows[-1])

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'bluetooth')))

driver.find_element(By.ID, 'bluetooth').click()
time.sleep(2)
driver.find_element(By.ID, "updates").click()
time.sleep(2)
driver.find_element(By.ID, "settings").click()
time.sleep(2)
driver.find_element(By.ID, "feedback").click()

driver.quit()

