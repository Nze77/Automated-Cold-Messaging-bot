from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import numpy as np
import pandas as pd
from pywhatkit import sendwhatmsg_instantly as snd
import pyautogui

# Opening maps and searching the local business
driver = webdriver.Chrome()
ac = ActionChains(driver)
driver.get("https://www.google.com/maps")
search = driver.find_element(By.XPATH, '//input[@class="fontBodyMedium searchboxinput xiQnY "]')
search.send_keys("Cafe's in Borivali west") # My personal fav niche as an ex-freelance graphic designer
search.send_keys(Keys.RETURN)
time.sleep(7)
names = []
numbers = []
def validnumber(k): # we need to check if its a valid number which will have a linked whatsapp. increases Data quality and basically no need for data cleaning
    chaltay = set("0123456789 +")
    for char in k:
        if char not in chaltay:
            return False
    if int(k[1]) < 7:
        return False
    return True

menu = driver.find_element(By.XPATH, '//div[@class="m6QErb DxyBCb kA9KIf dS8AEf XiKgde ecceSd"]')
ac.move_to_element(menu).perform()
time.sleep(2) #added for video can be removed
#scroll to get more results in a single run, can be increased for mass messaging
for rj in range(1,4):
    scroll_amount = 10000
    driver.execute_script(f"arguments[0].scrollTop += {scroll_amount};", menu)

for i in range(1,11): #actually scrapping and creating arrays with names and numbers
    current_name = ""
    xpath_temp = f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[{2*i+1}]/div/a'
    cafes = driver.find_element(By.XPATH, xpath_temp) 
    ac.click(cafes).perform()
    time.sleep(5)
    name = driver.find_elements(By.XPATH, '//h1[@class="DUwDvf lfPIob"]')
    for p in name:
        current_name = p.text
    number = driver.find_elements(By.XPATH, '//div[@class="Io6YTe fontBodyMedium kR99db "]')
    for j in number:
        if validnumber(j.text):
            names.append(current_name)
            numbers.append("+91"+f"{j.text[1:6]}"+f"{j.text[7:12]}")


# for the csv file.
df = pd.DataFrame({'Names':names,
                   'Numbers':numbers})
df.to_csv("test1.csv", index=False) 

#sending the automated msg. (PS: I am not a copywriter so ignore the basic script XD )
for mm in range(len(names)):
    message = "Hey "+f"{names[mm]}"+", I am Aryan, I am a graphic designer. I was wondering if you guys need any help with graphic designing."
    snd(numbers[mm], message)
    pyautogui.hotkey('ctrl', 'w')
print("Done, Make sure to Check out Aryan Pawaskar on LinkedIn.")
driver.close()
