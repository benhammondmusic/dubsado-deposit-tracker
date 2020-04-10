from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import re
from datetime import datetime, date, time, timedelta

#Load app settings
import settings
pauseTime = settings.pauseTime


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
def doTallyPage (browser):
    money_amounts = browser.find_elements_by_xpath("//i[@ng-show='project.invoice.items.length']")
    print str(len(money_amounts)) + " jobs tallied."


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
    browser.get(currentProjects_url)
    print "Loading " + currentProjects_url

#except:
#    print "Trouble Loading CURRENT PROJECTS page."



#TALLY MONEY FROM DISPLAYED PROJECTS
#try:
ready = WebDriverWait(browser, pauseTime).until(EC.visibility_of_element_located((By.XPATH, "//a[@ng-switch-when='prev']")))


prevButton = browser.find_element_by_xpath("//a[@ng-switch-when='prev']")
nextButton = browser.find_element_by_xpath("//a[@ng-switch-when='next']")


doTallyPage (browser)

#except:
#    print "Trouble TALLYING CURRENT PROJECTS ON THIS PAGE."








print "Done"

print "______________________"
print "______________________"
print "______________________"




# close the browser window
browser.quit()


#*************************************
