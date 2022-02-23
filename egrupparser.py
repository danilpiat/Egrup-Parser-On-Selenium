from selenium import webdriver
from seleniumwire import webdriver
from fake_useragent import UserAgent
import fitz
import os
from selenium.webdriver.common.keys import Keys
import time
import threading
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


proxies = [('login', 'pass', '46.8.16.116:1050'),
           ('login', 'pass', '188.130.143.174:1050'),
           ('login', 'pass', '46.8.154.254:1050'),
           ('login', 'pass', '46.8.212.110:1050'),
           ('login', 'pass', '46.8.106.224:1050')]
a = []
f = open('f_60962080604a76d3.txt', 'r')
for line in f:
    a.append(int(line))
f.close()

b = []
for i in range(0,int(len(a)/5)):
    b.append(a[i])
c = []
for i in range(int(len(a)/5),int(len(a)/5*2)):
    c.append(a[i])
d = []
for i in range(int(len(a)/5*2),int(len(a)/5*3)):
    d.append(a[i])
e = []
for i in range(int(len(a)/5*3),int(len(a)/5*4)):
    e.append(a[i])
f = []
for i in range(int(len(a)/5*4),int(len(a)/5*5)):
    f.append(a[i])
g = []
g.append(b)
g.append(c)
g.append(d)
g.append(e)
g.append(f)


def use_proxy(num,mas):
    proxy_info = proxies[num]
    login = proxy_info[0]  # авторизация прокси
    password = proxy_info[1]
    proxy_adress_now = proxy_info[2]
    proxy_options = {
        "proxy": {
            "https": f"https://{login}:{password}@{proxy_adress_now}"
        },
        "User-Agent": UserAgent().chrome
    }
    options = webdriver.ChromeOptions()
    # Установить путь к хранилищу для загрузки файлов по умолчанию и запретить всплывающее окно загрузки
    prefs = {'download.default_directory': 'E:\\Danil\\egrupparser\\parsedfiles', 'profile.default_content_setting.popups': 0}
    options.add_experimental_option('prefs', prefs)

    browser = webdriver.Chrome(
        executable_path="E:\Danil\egrupparser\chromedriver.exe",
        seleniumwire_options=proxy_options,chrome_options=options
    )
    browser.get('https://egrul.nalog.ru/')

    for el in mas:
        try:
            textf = WebDriverWait(browser, 50).until(ec.element_to_be_clickable((By.ID, 'query')))
            textf.click()
            time.sleep(0.3)
            textf.send_keys(el)
            time.sleep(0.3)
            textf.send_keys(Keys.ENTER)
            time.sleep(2)
        except:
            print('1')
        try:
            time.sleep(0.2)
            bdow = browser.find_elements(By.TAG_NAME,'button')
            time.sleep(1)
            bdow[2].click()
            time.sleep(0.2)
        except:
            print('2')
        print(el)
        time.sleep(0.5)
        try:
            textdel = WebDriverWait(browser, 50).until(ec.element_to_be_clickable((By.ID, 'uni_text_0')))
            time.sleep(0.8)
            textdel.click()
            time.sleep(0.2)
        except:
            print('3')




if __name__ == '__main__':
    threads = []
    num_list=[0,1,2,3,4]
    for i in range(5):
        t = threading.Thread(target=use_proxy, args=(num_list[i],g[i]))
        t.start()
        threads.append(t)
    print("Main    : wait for the thread to finish")
    for t in threads:
        t.join()
    print("Main    : all done")

    inn_mas = []
    f = open('f_60962080604a76d3.txt', 'r')
    for line in f:
        inn_mas.append(line.split())
    f.close()

    for element in os.scandir("E:\\Danil\\egrupparser\\parsedfiles\\"):
        with fitz.open(element.path) as doc:
            text_all = []
            for page in doc.pages():
                text_all.append(page.getText())
            for i in inn_mas:
                for x in text_all:
                    if "ИНН юридического лица" + '\n' + i[0] in x:
                        for page in doc:
                            text = page.getText()
                            stext = text.split("\n")
                            el_index = 0
                            for el in stext:
                                el_index += 1
                                if el == 'Страна происхождения':
                                    i.append(stext[el_index])

    file = open("out.txt", 'w+', encoding="utf-8")
    for el in a:
        for ab in el:
            file.writelines(ab + ', ')
        file.writelines('\n')
    file.close()


