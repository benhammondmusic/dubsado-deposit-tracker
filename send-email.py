# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#Load app settings
import settings


### EMAIL THE XLS FILE WITH GIGS TO BandsInTown SPECIAL BULK UPLOAD ADDRESS
#*************************************
def send_email ():

    #clear the text output
    for i in range(5):
        print "\n."

    gmail_password = settings.login['gmail_password']
    me = settings.login['gmail_username']

    print "\n\n_________________________"
    print "_______EMAIL REPORT______"
    print "_________________________\n"

    # instance of MIMEMultipart
    print 'Assembling the email...'

    msg = MIMEMultipart()
    msg['Subject'] = 'Dubsado Projects: Deposit Report'
    msg['From'] = me
    msg['To'] = me
    msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # string to store the body of the mail
    body = "..."

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    print 'Contacting Gmail Server...',
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    print 'Securely...',
    # start TLS for security
    s.starttls()

    print 'Logging In...'
    # Authentication
    s.login(me, gmail_password)

    print 'Adding Email Message...'
    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    print 'Sending from {} to {}...'.format(me, me)
    s.sendmail(me, me, text)


    # terminating the session
    print 'Closing email...'
    s.quit()
    print "______________________"
    print "______________________"
    print "______________________"
    return;
    #*************************************
