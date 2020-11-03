import dload
from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver
import time

driver = webdriver.Chrome('chromedriver') # 웹드라이버 파일의 경로
# driver.get("https://search.daum.net/search?nil_suggest=btn&w=img&DA=SBC&q=%EB%B0%B1%EC%98%88%EB%A6%B0")
driver.get("https://www.google.com/search?q=%EB%B0%B1%EC%98%88%EB%A6%B0&tbm=isch&ved=2ahUKEwj1kpa935LsAhXWAKYKHd40DpcQ2-cCegQIABAA&oq=%EB%B0%B1%EC%98%88%EB%A6%B0&gs_lcp=CgNpbWcQDFAAWABg960haABwAHgAgAEAiAEAkgEAmAEAqgELZ3dzLXdpei1pbWc&sclient=img&ei=anR1X_W1PNaBmAXe6bi4CQ&bih=754&biw=1536#imgrc=C2dDh9CQmg0DfM")
time.sleep(5) # 5초 동안 페이지 로딩 기다리기

req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')


thumbnails = soup.select("#islrg > div.islrc > div > a.wXeWr.islib.nfEiy.mM5pbd > div.bRMDJf.islir > img")

i = 1
for thumbnail in thumbnails:
    # img = thumbnail['src']
    # dload.save(img,f"img/{i}.jpg")
    # i += 1
    img = None
    if thumbnail.has_attr('src'):
        img = thumbnail['src']
    elif thumbnail.has_attr('data-src'):
        img = thumbnail['data-src']

    if "data:image" in img:
        data_uri = img
        with request.urlopen(data_uri) as response:
            data = response.read()
        with open(f"imgs_homework/{i}.png", "wb") as f:
                f.write(data)

    else:
        dload.save(img, f"imgs_homework/{i}.jpg")

    # print(img)
    # dload.save(img, f"img/{i}.jpg")
    i += 1

driver.quit() # 끝나면 닫아주기