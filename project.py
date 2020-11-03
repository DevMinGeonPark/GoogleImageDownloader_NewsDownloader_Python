from bs4 import BeautifulSoup
from selenium import webdriver
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from openpyxl import Workbook

driver = webdriver.Chrome('chromedriver')

wb = Workbook()
ws1 = wb.active
ws1.title = "articles"
ws1.append(["제목", "링크", "신문사", "썸네일"])

url = f"https://search.naver.com/search.naver?&where=news&query=추석"

driver.get(url)
req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')

articles = soup.select("#main_pack > div.news.mynews.section._prs_nws > ul > li")

for article in articles:
    title = article.select_one("dl > dt > a").text
    url = article.select_one("dl > dt > a")['href']
    comp = article.select_one("dl > dd.txt_inline > span._sp_each_source").text.split(' ')[0].replace('언론사','')
    thumbnail = article.select_one("div > a")['href']
    ws1.append([title,url,comp,thumbnail])

wb.save(filename='articles.xlsx')
driver.quit()

# 보내는 사람 정보
me = "testmin7985@gmail.com"
my_password = "pwd" #임의의 패스워드

# 로그인하기
s = smtplib.SMTP_SSL('smtp.gmail.com')
s.login(me, my_password)

# 받는 사람 정보
you = "testmin7985@naver.com"

# 메일 기본 정보 설정
msg = MIMEMultipart('alternative')
msg['Subject'] = "To day News"
msg['From'] = me
msg['To'] = you

# 메일 내용 쓰기
content = "ok"
part2 = MIMEText(content, 'plain')
msg.attach(part2)

# 파일 첨부하기
part = MIMEBase('application', "octet-stream")
with open("articles.xlsx", 'rb') as file:
    part.set_payload(file.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment", filename="articles.xlsx")
msg.attach(part)

# 메일 보내고 서버 끄기
s.sendmail(me, you, msg.as_string())
s.quit()