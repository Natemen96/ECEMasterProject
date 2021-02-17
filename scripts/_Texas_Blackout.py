# import requests
# import csv
# from bs4 import BeautifulSoup

# from selenium import webdriver as web
# from selenium.webdriver.common.action_chains import ActionChains
# import time
# from selenium.webdriver.support.ui import WebDriverWait as wait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
from datetime import datetime


# class betterActionChains(ActionChains):
#     def move_to_orgin(self, to_element, xoffset =0 , yoffset =0):
#         """
#         Moving the mouse to an offset from current mouse position.

#         :Args:
#          - xoffset: X offset to move to, as a positive or negative integer.
#          - yoffset: Y offset to move to, as a positive or negative integer.
#         """
#         if self._driver.w3c:
#             self.w3c_actions.pointer_action.move_to_location(0 + xoffset, 0 + yoffset)
#             self.w3c_actions.key_action.pause()
#         else:
#             self._actions.append(lambda: self._driver.execute(
#                 Command.MOVE_TO, {
#                     'xoffset': int(xoffset),
#                     'yoffset': int(yoffset)}))
#         return self

# # URL = 'https://www.monster.com/jobs/search/?q=Software-Developer&where=Australia'
# URL = 'https://poweroutage.us/area/state/texas'
# page = requests.get(URL)
# soup = BeautifulSoup(page.content, 'html.parser')
# # results = soup.find(id='ResultsContainer')
# results = soup.find(id='CountyName')
# # print(results.prettify())

# driver = web.Chrome(executable_path='ECEMasterProject\scripts\chromedriver.exe')
# driver.maximize_window()

# Ids = [1510]

# driver.get('https://poweroutage.us/area/state/texas')
# driver.get('https://poweroutage.us/area/county/+Ids')
# time.sleep(5)

# <div id="mappopup" class="PopUpBox" style="display: none; left: 344px; top: 589px; margin-left: -184px; margin-top: -40px;">
#     <text id="CountyName"></text><br>
#     <text id="CountyTracked"></text><br>
#     <text id="CountyOut"></text>
# </div>

# print('Below is data')
# data = driver.find_element_by_xpath('//body/div[2]/div[7]/div[1]/div[2]/div[2]/canvas[1]')

# data.size = 

# data.size['x'] = 29
# data.size['y'] = 221
# hov = ActionChains(driver)
# hov.move_to_element(data).perform()
# print(data.size)
# print(data.location)
# print(type(data.size))
# height = data.size['height']
# width = data.size['width']
# print(width, height)



# for i in range(0,width,50):
#     for j in range(0,height,50):
#         hov = ActionChains(driver).move_to_element_with_offset(data,i,j)
#         hov.perform()
#         time.sleep(2)
#         data_in_the_bubble = driver.find_element_by_xpath("//text[@id='CountyName']")
#         hover_data = data_in_the_bubble.get_attribute("innerHTML")
#         print(i,j)
#         print(hover_data)

# driver.close()
print(datetime.now())