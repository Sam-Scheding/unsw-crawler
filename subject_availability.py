from bs4 import BeautifulSoup
import requests
import smtplib
from email.message import EmailMessage
import time

courses = ['COMP3900']

# Set these before use
username = None
password = None


def init():

    if username is None, or password is None:
        print('You need to set up your email account first, so you can receive emails')
        exit()
def crawl():

    base_url = 'http://timetable.unsw.edu.au/2019/{}.html'

    for course in courses:

        url = base_url.format(course)
        html = requests.get(url).content
        # print(html)
        soup = BeautifulSoup(html, 'html.parser')
        semesters = soup.findAll("tr", {"class": "rowLowlight"})
        tds = semesters[0].findAll('td') # get all table rows for semester 1
        enroled, capacity = tds[-2].contents[0].split('/')

        if int(enroled) < int(capacity):
            send_email(course)
            print(course, 'has openings!')
        time.sleep(100)

def send_email(course):

    msg = EmailMessage()
    msg.set_content("{} Has availabilities!".format(course))

    me = username
    you = username
    msg['Subject'] = 'You can enrol in {}'.format(course)
    msg['From'] = me
    msg['To'] = you

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    #Next, log in to the server
    server.login(username, password)
    server.send_message(msg)
    server.quit()
    print('Success!')


if __name__ == '__main__':
    init()
    crawl()
