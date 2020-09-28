from selenium import webdriver
import time
browser = webdriver.Chrome(executable_path='C:\selenium\chromedriver.exe')
browser.get("https://typecast.ai/create-v2")
time.sleep(0.5)
print(browser.window_handles)


# 팝업
# print(browser.current_url)
# print(browser.window_handles)
# 탭 활성화
# browser.switch_to.window(browser.window_handles[1])
with open(path + "/typecast.txt", 'r', encoding='utf-8') as typecast:
    cont = typecast.readlines()
    id = cont[0].strip()
    pw = cont[1].strip()
browser.find_element_by_id("email").send_keys(id)
browser.find_element_by_id("password").send_keys(pw)
browser.find_elements_by_tag_name("button")[0].click()
print("실행완료")

time.sleep(10)
#browser.find_element_by_tag_name('img').click()
from bs4 import BeautifulSoup
soup = BeautifulSoup(browser.page_source)
print(soup.find_all('div', class_='menu-list-item menu-list-item-normal')[3])
browser.find_element_by_class_name('ProseMirror').send_keys("dfgdgd")
share_btn = browser.find_elements_by_class_name('menu-list-item')[3]
browser.execute_script('arguments[0].click();', share_btn)
print("클릭 성공")
time.sleep(10)
soup = BeautifulSoup(browser.page_source)
url = soup.find('div', class_='code-background').get_text()
print(url)
browser.close()

