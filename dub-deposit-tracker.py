from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import re
from datetime import datetime, date, time, timedelta
import math
import time

#Load app settings
import settings
pauseTime = settings.pauseTime
JOBS_PER_PAGE = 50.0


#*************************************
def doLogin (aUsername, aPassword, browser, login_url):
    print "Logging In to Dubsado"
    browser.get(login_url) #navigate to login page

    #WAIT UNTIL ELEMENTS ARE VISIBLE
    try:
        ready = WebDriverWait(browser, pauseTime).until(EC.element_to_be_clickable((By.ID, 'email')))

        browser.find_element_by_id('email').send_keys(aUsername)

        browser.find_element_by_id('password').send_keys(aPassword)

        browser.find_element_by_xpath("//button[text()='Log In']").click()

    except:
        print "Trouble Loading DUBSADO login page."
    #*************************************

#*************************************
def doTallyPage (money_amounts, deposits_tally, private_events_gross, gross_tally, number_tallied_jobs):
    for job_status in money_amounts:
        if job_status.text:
            both_moneys = job_status.text.split(" / ")
            deposit = both_moneys[0].replace("$","").replace(",","")
            deposit_i = int(deposit)
            total_i = int(both_moneys[1].replace("$","").replace(",",""))
            remainder_i = total_i - deposit_i
        else:
            deposit_i = total_i = remainder_i = 0

        deposits_tally += deposit_i
        gross_tally += total_i

        if deposit_i:
            private_events_gross += total_i




    number_tallied_jobs += len(money_amounts)

    return (deposits_tally, private_events_gross, gross_tally, number_tallied_jobs)
        # print "DEPOSIT PAID: " + str(deposit_i)
        # print "REMAINDER DUE: " + str(remainder_i)
        # print "JOB TOTAL: " + str(total_i)


    #*************************************



# START - CLEAR TEXT OUTPUT
for i in range(5):
    print "\n."

print "\n\n________________________________________"
print "_________DUBSADO DEPOSIT TRACKER________"
print "________________________________________\n"



# LOAD PYTHON FILES
import send_email


# BE SURE TO UPDATE YOUR SETTINGS.PY FILE WITH CREDENTIALS (DELETE THE .EXAMPLE WHEN FIRST SETTING IT UP)
import settings
headless = settings.headless


# SET OPTIONS AND MAKE A BROWSER WINDOW
options = webdriver.ChromeOptions()
# incognito window
#options.add_argument("--incognito")
if headless:
    options.add_argument('headless')
# to maximize window: #options.add_argument("--kiosk")
browser = webdriver.Chrome(chrome_options = options)


# LOAD CREDENTIALS AND LOG IN IF NEEDED
password = settings.login['dubsado_password']
username = settings.login['dubsado_username']
currentProjects_url = settings.login['currentProjectsDubsado_url']
login_url = settings.login['loginDubsado_url']


#try to start at projects page
# !!! NEED TO ADD COOKIES TO MAINTAIN LOGIN
browser.get(currentProjects_url)
if browser.current_url != currentProjects_url:
    try:
        print "Not Logged In."
        doLogin(username, password, browser, login_url)

    except:
        print "Trouble Logging In to Dubsado"

    #SELECT BRAND
    try:
        ready = WebDriverWait(browser, pauseTime).until(EC.element_to_be_clickable((By.CLASS_NAME, 'brand-logo')))
        #NEED TO CLICK FIRST BRAND
        brand_buttons = browser.find_elements_by_class_name('brand-logo')
        brand_buttons[0].click()
        print "Selecting First Brand: " + brand_buttons[0].get_attribute("alt")
    except:
        print "Trouble Loading BRAND SELECTION"


#VISIT CURRENT PROJECTS PAGE
#try:
#ready = WebDriverWait(browser, pauseTime).until(EC.visibility_of_element_located((By.ID, 'calendar-overview')))

if browser.current_url != currentProjects_url:
    try:
        browser.get(currentProjects_url)
    except:
        print "Trouble Loading CURRENT PROJECTS page."



#TALLY MONEY FROM DISPLAYED PROJECTS
ready = WebDriverWait(browser, pauseTime).until(EC.visibility_of_element_located((By.XPATH, "//a[@ng-switch-when='prev']")))
deposits_tally = gross_tally = private_events_gross = number_tallied_jobs = 0
job_counts = browser.find_elements_by_xpath(("//div[@class='funnel-count-number ng-binding']"))
number_current_jobs = float(job_counts[2].text)
number_of_pages = int(math.ceil(number_current_jobs / JOBS_PER_PAGE))

# prevButton = browser.find_element_by_xpath("//a[@ng-switch-when='prev']")

for page in range(0,number_of_pages):
    ready = WebDriverWait(browser, pauseTime).until(EC.visibility_of_element_located((By.XPATH, "//a[@ng-switch-when='prev']")))
    money_amounts = browser.find_elements_by_xpath("//i[@ng-show='project.invoice.items.length']")
    tallies = doTallyPage (money_amounts, deposits_tally, private_events_gross, gross_tally, number_tallied_jobs)
    deposits_tally = tallies[0]
    private_events_gross = tallies[1]
    gross_tally = tallies[2]
    number_tallied_jobs = tallies[3]
    nextButton = browser.find_element_by_xpath("//a[@ng-switch-when='next']")
    nextButton.click()
    time.sleep(3)


print str(number_tallied_jobs) + " current jobs on " + str(number_of_pages) + " pages."
print "$" + str(deposits_tally) + " DEPOSITS COLLECTED ON CURRENT JOBS"
print "$" + str(gross_tally-deposits_tally) + " REMAINDER PAYMENTS DUE ON CURRENT JOBS"
print "_____________________________"
print "$" + str(gross_tally) + " GROSS - ALL CURRENT JOBS ( INCL $" + str(private_events_gross) + " FROM CONTRACTED PRIVATE EVENTS)"
percent_privates = int(100 * float(private_events_gross)/float(gross_tally))
print str(percent_privates) + "% OF GROSS FROM CONTRACTED EVENTS"
print "______________________"
print "______________________"
print "______________________"




# close the browser window
browser.quit()


#*************************************
