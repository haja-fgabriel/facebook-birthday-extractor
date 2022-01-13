from selenium import webdriver
from selenium.webdriver.common.by import By
import os

driver = webdriver.Chrome(os.path.join(os.pardir, "chromedriver"))
driver.get("https://bws.rocks")
assert driver.find_element(By.XPATH, '//*[contains(text(), "not private")]')
advanced_button = driver.find_element(By.ID, "details-button")
advanced_button.click()
proceed_button = driver.find_element(By.ID, "proceed-link")
proceed_button.click()
assert "Clever Software Solutions Inc." == driver.title

driver.implicitly_wait(10)
driver.quit()
