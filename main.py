"""
# Author Zeyu Li
# A short script for checking if the dates available for GRE General Test
# V1.0
"""
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText

from selenium import webdriver

try:
    driver = webdriver.Chrome("/Users/lizeyu/Desktop/Dev/chromedriver")
    driver.get("https://mygre.ets.org/greweb/login/login.jsp")

    #login
    username_ele = driver.find_element_by_name("username")
    password_ele = driver.find_element_by_name("password")

    username_ele.send_keys("your username")
    password_ele.send_keys("your password")

    password_ele.submit()

    # book test
    book_btn = driver.find_element_by_class_name("btn-eReg")
    book_btn.click()

    # enter booking info
    test_name = driver.find_element_by_class_name("k-input")
    test_dropdown = driver.find_element_by_class_name("k-header")
    test_dropdown.click()

    # wait for XML change from display:none to block so selenium can interact with
    time.sleep(2)
    option = driver.find_element_by_xpath("//*[@id='testId_listbox']/li[2]")
    option.click()

    driver.execute_script("arguments[0].value = 'GRE General Test';", test_name)
    driver.execute_script("arguments[0].innerText = 'GRE General Test'", test_name)
    location = driver.find_element_by_id("location")
    location.send_keys("Toronto")

    find_btn = driver.find_element_by_id("findTestCenterButton")
    find_btn.click()
    # wait for load
    time.sleep(2)

    # check if date available
    try:
        date_wanted = driver.find_element_by_xpath("//*[@id='byDateCalendarPlusMonth']/table/tbody/tr[3]/td[7]/a/div")
        if date_wanted.get_attribute("class") == "availableDate":
            print("The date is available")
            content = ""

            # send notification to this email address when find one
            target = "Custom target"
            msg = MIMEText(content, "plain", "utf-8")
            msg["Subject"] = Header("Find seats for GRE General Test")
            msg["From"] = Header("Custom header")
            msg["To"] = Header(target)

            mailhost = "your mail host"
            usermail = "your email name"
            password = "your email password"

            try:
                server = smtplib.SMTP("smtp.gmail.com:587", timeout=30)
                server.ehlo()
                server.starttls()
                server.login(usermail, password)
                server.sendmail(usermail, [target],
                                msg.as_string())
                server.quit()
                print("Email successfully sent!")
            except Exception as e:
                print(str(e))
    except:
        print("The date is not available")
except:
    print("Some thing went wrong, please check")
finally:
    driver.close()

