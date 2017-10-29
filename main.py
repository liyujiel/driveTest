import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys

from time import sleep
from datetime import datetime
import json


import smtplib
sender = "garretmoon@gmail.com"
password = "ljg711112"
reciver = "potalexto@gmail.com"
SUBJECT = "test email"


def find_available_date(jsonContent):
    prtLst = []
    for dayDict in jsonContent:
        if dayDict.get('description') != 'UNAVAILABLE' and dayDict.get('description') != 'FULL' :
            prtLst.append(dayDict)
    return prtLst

def getJsonAvailableContent(browser):
    sleep(5)
    browser.find_element_by_id("tab-1").click()
    sleep(5)
    content = browser.find_element_by_tag_name("pre").text
    jsonContent = json.loads(content)['availableBookingDates']
    return jsonContent

Omonth = month = int(input("month: ")) #datetime.today().month
Oyear = year = int(input("year: ")) #datetime.today().year
examType = str(input("G2/G: ")).upper()

browser = webdriver.Firefox()

browser.get("https://drivetest.ca/book-a-road-test/booking.html#/verify-driver")
handle1 = browser.window_handles
# print(handle1)

sleep(1)
browser.find_element_by_id("licenceNumber").send_keys("H90067890995906")
browser.find_element_by_id("licenceExpiryDate").send_keys("20211228")

sleep(30)

#browser.find_element_by_id("regSubmitBtn").click()

sleep(5)

browser.find_element_by_link_text("Book a New Road Test").click()

sleep(5)
btnName = examType+"btn"
browser.find_element_by_id(btnName).click()

sleep(5)

browser.find_element_by_class_name("booking-submit").click()

sleep(5)
browser.find_element_by_xpath("//*[@id='9583']").click()

sleep(5)

#browser.find_element_by_link_text("Continue").click()
browser.find_element_by_class_name("booking-submit").click()
sleep(5)



# browser.find_element_by_class_name("booking-submit").click()

jsonUrlTemp = ("https://drivetest.ca/booking/v1/booking/12694?month={month}&year={year}")

openCommand ="window.open('"+jsonUrlTemp.format(month=str(month),year=str(year))+"')"

browser.execute_script(openCommand)

handles = browser.window_handles
browser.switch_to_window(handles[-1])


jsonContent = getJsonAvailableContent(browser)

dateLst = find_available_date(jsonContent)




while dateLst == []:
    if month < 12:
        month += 1 
    elif month == 12:
        month = 1 
        year += 1
    url = jsonUrlTemp.format(month=str(month),year=str(year))
    browser.get(url)
    sleep(3)
    jsonContent = getJsonAvailableContent(browser)
    dateLst = find_available_date(jsonContent)

print(month)
print(dateLst)
day0 = dateLst[0]['day']
dayXpath = "//*[@title='{day}']".format(day=day0)


browser.switch_to_window(handles[0])
while(month != Omonth or year != Oyear):
    if month > 12:
        Omonth = 1
        Oyear += 1
    browser.find_element_by_class_name("ion-chevron-right").click()  
    Omonth += 1
    
browser.find_element_by_xpath(dayXpath).click()    
browser.find_element_by_xpath("//*[@id='calendarSubmit']/button").click()

msg = "month: " + str(month) + " dateLst: " + str(dateLst)

BODY = '\r\n'.join(['To: %s' % reciver,
                    'From: %s' % sender,
                    'Subject: %s' % SUBJECT,
                    '', msg])



try:
    mail = smtplib.SMTP("smtp.gmail.com:587")
    mail.ehlo()
    mail.starttls()
    mail.login(sender,password)
    mail.sendmail(sender, reciver, BODY)         
    print("Successfully sent email")
except:
    print("Error: unable to send email")

mail.quit()

# first_result = ui.WebDriverWait(browser, 15).until(lambda browser: browser.find_element_by_class_name('rc'))
# first_link = first_result.find_element_by_tag_name('div')


# elem = browser.find_element_by_name('p')  # Find the search box
# elem.send_keys('seleniumhq' + Keys.RETURN)

#browser.quit()