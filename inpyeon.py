from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from datetime import datetime
import time
import requests
#import time
URL = '##인편 보내려는 게시판 url##'
options = Options()
options.add_argument('headless')
options.add_argument('disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors')
driver2 = webdriver.Chrome(options=options)
driver2.get('http://www.google.com/')
print(driver2.title)

element = driver2.find_element_by_name('q')
element.send_keys("뉴스")
element.submit()
links = driver2.find_elements_by_tag_name('a')
driver2.find_element_by_link_text("뉴스").click()

divs = driver2.find_elements_by_tag_name("div")
for div in divs:
    if div.text == "도구":
        print("찾았음")
        div.click()
        break
divs = driver2.find_elements_by_tag_name("div")
for div in divs:
    if div.text == "최근 항목":
        print("찾았음")
        div.click()
        break
links = driver2.find_elements_by_tag_name("a")
for link in links:
    #print(link.text)
    if link.text == "지난 1일":
        print("찾았음")
        link.click()
        break
link_divs = driver2.find_elements_by_tag_name('g-card')
links = [div.find_elements_by_tag_name('a') for div in link_divs]

urlsAndtext = []
for link in links:
    if len(link) > 1:
        continue
    href = str(link[0].get_attribute('href'))
    link_text = link[0].text.replace('\n','')
    link_text = link_text[:link_text.find('Copyright')]

    if link_text != '':
        urlsAndtext.append((href, link_text))
#print(urlsAndtext)
driver2.quit()

contents = ''

for i in range(len(urlsAndtext)):
    try:
        html_doc = requests.get(urlsAndtext[i][0]).text
        soup = BeautifulSoup(html_doc,'html.parser')
        p_divs = soup.body.find_all('p')
        tmp = ''
        for p in p_divs:
            text = p.get_text(strip=True)
            if 'Copyright' in text or 'SNS' in text or ':' in text or '저작권' in text or '|' in text:
                continue
                
            if len(text) > 10:
                tmp += text
        contents += urlsAndtext[i][1]+'전\n' + tmp
    except:
        continue
#print(contents)

N = int(len(contents)/1150) + 1 
print(N)

pwd = "0919"
dateText = datetime.today().strftime("%Y년 %m월 %d일자 기사")

notFoundIndex = []
for i in range(N):
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    print(driver.title)
    #print(driver.find_element_by_class_name("wizbtn.large.ngray.normal.btnr"))
    driver.find_element_by_class_name("wizbtn.large.ngray.normal.btnr").click()
    #print(driver.page_source)

    driver.find_element_by_class_name("normal").click()
    driver.switch_to.window(driver.window_handles[1])
    #print(driver.page_source) 
    try:
        searchInput = driver.find_element_by_class_name('popSearchInput')
    except:
        try:
            searchInput = driver.find_element_by_id('keyword')
        except:
            print('searchInput 못찾음 ㅠ')
            notFoundIndex.append(i)
            continue
    
    #print(searchInput)
    searchInput.send_keys('##본인집주소##')
    searchInput.send_keys(Keys.RETURN)


    driver.find_element_by_id('roadAddrTd1').click()

    detailInput = driver.find_element_by_id('rtAddrDetail')
    detailInput.click()
    detailInput.send_keys('##세부주소##')
    #print(driver.page_source)

    links = driver.find_elements_by_tag_name('a')
    for link in links:
        if link.text == '주소입력':
            print('찾았음')
            link.click()
            break
    driver.switch_to.window(driver.window_handles[0])
    #print(driver.page_source)
    title = dateText
    innerText = '{} {}번째 페이지 입니다\n'.format(dateText, i+1)
    if i==N-1:
        innerText += contents[i*1150:]
    else:
        innerText += contents[i*1150:(i+1)*1150]
    driver.find_element_by_id("senderName").send_keys('##본인의 이름##')
    driver.find_element_by_id("relationship").send_keys('##관계##')
    driver.find_element_by_id("title").send_keys(dateText)
    driver.find_element_by_id("contents").send_keys(innerText)
    driver.find_element_by_id("password").send_keys(pwd)
    #print(driver.find_element_by_class_name('submit'))
    submit = driver.find_element_by_class_name('submit')
    submit.click()
    time.sleep(5)
    #print(driver.page_source) 
    driver.quit()
    
while len(notFoundIndex) > 0:
    for index in notFoundIndex:
        driver = webdriver.Chrome(options=options)
        driver.get(URL)
        print(driver.title)
        #print(driver.find_element_by_class_name("wizbtn.large.ngray.normal.btnr"))
        driver.find_element_by_class_name("wizbtn.large.ngray.normal.btnr").click()
        #print(driver.page_source)

        driver.find_element_by_class_name("normal").click()
        driver.switch_to.window(driver.window_handles[1])
        #print(driver.page_source) 
        try:
            searchInput = driver.find_element_by_class_name('popSearchInput')
        except:
            try:
                searchInput = driver.find_element_by_id('keyword')
            except:
                print('또 못찾음 ㅠㅠ')
                continue
        #print('전:', notFoundIndex)
        notFoundIndex.remove(index)
        #print('후:', notFoundIndex)

        #print(searchInput)
        searchInput.send_keys('##본인집주소##')
        searchInput.send_keys(Keys.RETURN)


        driver.find_element_by_id('roadAddrTd1').click()

        detailInput = driver.find_element_by_id('rtAddrDetail')
        detailInput.click()
        detailInput.send_keys('##세부주소##')
        #print(driver.page_source)

        links = driver.find_elements_by_tag_name('a')
        for link in links:
            if link.text == '주소입력':
                print('찾았음')
                link.click()
                break
        driver.switch_to.window(driver.window_handles[0])
        #print(driver.page_source)
        title = dateText
        innerText = '{} {}번째 페이지 입니다\n'.format(dateText, index+1)
        if index==N-1:
            innerText += contents[index*1150:]
        else:
            innerText += contents[index*1150:(index+1)*1150]
        driver.find_element_by_id("senderName").send_keys('##본인이름##')
        driver.find_element_by_id("relationship").send_keys('##관계##')
        driver.find_element_by_id("title").send_keys(dateText)
        driver.find_element_by_id("contents").send_keys(innerText)
        driver.find_element_by_id("password").send_keys(pwd)
        #print(driver.find_element_by_class_name('submit'))
        submit = driver.find_element_by_class_name('submit')
        submit.click()
        time.sleep(5)
        #print(driver.page_source)
        driver.quit()

