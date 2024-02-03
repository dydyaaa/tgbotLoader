from selenium import webdriver
import os, time, cfg
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

directory = cfg.directory
timeout = 60
poll_interval = 1

def main(urll):
    
    index = int(urll[-1]) - 1

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-download-notification")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": directory
    })

    # Открываем браузер и переходим по ссылке
    browser = webdriver.Chrome(options=chrome_options)
    url = "https://sssinstagram.com/ru" 

    browser.implicitly_wait(10)
    browser.get(url)
    wait = WebDriverWait(browser, 10)
    wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")

    # Вставляем в input нашу ссылку на пост
    input_field = browser.find_element(By.XPATH, "//input[@name='id']")
    input_text = urll
    input_field.send_keys(input_text)
    
    # Нажимаем на кнопку
    button = browser.find_element(By.XPATH, "//button[@id='submit']")
    button.click()

    if len(browser.window_handles) > 1:
        browser.switch_to.window(browser.window_handles[1])
        browser.close()
        browser.switch_to.window(browser.window_handles[0])

    # Ждем, пока на странице не будет прогружено видео
    wait = WebDriverWait(browser, 15)  
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='response']")))

    buttons = browser.find_elements(By.XPATH, "//div[@class='download-wrapper']")[index]

    buttons.click()
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        files = [f for f in os.listdir(directory) if f.lower().endswith('.mp4')]
    
        if files:
            break

    browser.quit()