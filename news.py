from openpyxl import Workbook
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome('chromedriver')


url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query=추석"

driver.get(url)
req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')

articles = soup.select("#main_pack > div.news.mynews.section._prs_nws > ul > li")

wb = Workbook()
ws1 = wb.active
ws1.title = "articles"
ws1.append(["제목", "링크", "신문사"])


for article in articles:
    title = article.select_one("dl > dt > a").text
    url = article.select_one("dl > dt > a")['href']
    comp = article.select_one("dl > dd.txt_inline > span._sp_each_source").text.split(' ')[0].replace('언론사','')
    ws1.append([title,url,comp])

wb.save(filename='articles.xlsx')
driver.quit()

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


# 보내는 사람 정보
me = "보내는사람@gmail.com"
my_password = "비밀번호"

# 로그인하기
s = smtplib.SMTP_SSL('smtp.gmail.com')
s.login(me, my_password)

# 받는 사람 정보
you = "받는사람@아무_도메인"

# 메일 기본 정보 설정
msg = MIMEMultipart('alternative')
msg['Subject'] = "제목"
msg['From'] = me
msg['To'] = you

# 메일 내용 쓰기
content = "메일 내용"
part2 = MIMEText(content, 'plain')
msg.attach(part2)

# 파일 첨부하기
part = MIMEBase('application', "octet-stream")
with open("파일 이름", 'rb') as file:
    part.set_payload(file.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment", filename="첨부파일 이름")
msg.attach(part)

# 메일 보내고 서버 끄기
s.sendmail(me, you, msg.as_string())
s.quit()