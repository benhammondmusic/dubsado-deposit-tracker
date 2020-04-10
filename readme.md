# Dubsado Deposit Tracker
Scan through ALL current projects and report back both the DEPOSITS COLLECTED and the REMAINDER PAYMENTS STILL OWED



FUTURE UPDATES/IDEAS:
- add email functionality
- option to auto-run program on a set time schedule so emails
- compare amounts to a specific bank account balance
- deal with multiple brands under one account
- generate a statement PDF, and email client total due, along with statement PDF and all invoice PDFs (many corporate clients have trouble opening the webpage invoices and need pdf copies)
- make an executable, ideally PWA style that could run from phone


PROBLEM: Dubsado is a great tool for artists to manage their clients and events, however it is lacking some functionality including the ability to see at a glance how much money an artist has collected in deposits across ALL jobs/clients. The problem was highlighted during the COVID-19 crisis when multiple clients cancelled and I wanted to be sure I had set aside the proper amount of money.

SOLUTION: Automate the process using Python.

PROCESS:
- Load up a web browser and log in to Dubsado (using USER supplied credentials in the settings.py file)
- Visit first brand
- Visit the Current Jobs page
- Tally across multiple pages if needed, including deposits collected, remainders paid/still owed


SETUP/OPERATION: User must complete the following tasks to operate program
- edit settings.py.example to store your usernames, passwords and brand names
- change that file name to settings.py

KNOWN ISSUES:
- had to use SLEEP timer to get DOM to refresh... need to fix
-
-
-
