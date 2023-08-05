# HELLO & WELCOME to the setup-configuration file!

# A) If you do not know how it works: lines with
# <-- this hash-sign at the beginning are comments and do not have any effect to the program - these lines are only there to give you information.

# B) The values BETWEEN the "double quotes" are the ones you need to exchange 
# (the double quotes are needed - for the multi-line-value there are three at the beginning and three of them at the end)

# C) There are 11 values you can change - to get the Setuptest running, at least the value for the IP of the CCS (ccsIP) AND 
# the API-Key of the Sendgrid email-provider (sendgridAPIkey) are needed to be set, but I deeply suggest to you that you do set all 11 values correctly right now at the beginning!
# This test_configVars.py file is a normal text-file: Simply overwrite the values & SAVE it when done.

# Let's start with the values:

 
# 1.) IP of the CCS
# Enter the IP of your Server with https - or set to localhost if you're on localhost.
# the cheapest VPS hoster I could find is mvps, located in Cyprus (3 EUR/ month, 2GB RAM) - this is my personal provider as well. Just go to:
# https://www.mvps.net/?aff=6517 (yes, I do get a price-reduction for my own server if you use the link with this affiliate-id  -  but you cannot get it cheaper without it. So: I would appreciate it, if you'd support this project & help me to reduce the costs ...)
global ccsIP
#as an example for your server connected to the internet: ccsIP = "https://45.137.155.666"
#as an example if you have the CCS on your local machine: ccsIP = "https://localhost"
ccsIP = "not-set-yet"
#ccsIP = "https://localhost"

# 2.) SendGrid API-Key
# to ensure that the stakeholders do receive the emails sent from the CCS we decided
# to use SendGrid as our E-Mail-provider & prepared the backend exlusively. **
# Go to:
# https://sendgrid.com/free/
# and get a free account within a few clicks (no credit card needed)
global sendgridAPIkey
sendgridAPIkey = "SG.z123abc_DummyAPI4TestExampleAPIcomparable123.toThis4321Format-2be-exchanged-WithYours_xZst"

# 3.) 4.) 5.) 6.) 7.) the NUMBERS of your project you/your team-mates need to enter in the login-form
# You can set the project NUMBERS accordingly to your ERP's project numbers - or you simply count up  "1"  "2" "3" "4" "5"
# or keep it default "001", "002", "003", "004", "005".
# BUT: IT MUST BE NUMBERS (no alphanumerics, no separators like dots, commas, free spaces ..):
global firstProjectNumber
firstProjectNumber = "001"
global secondProjectNumber
secondProjectNumber = "002"
global thirdProjectNumber
thirdProjectNumber = "003"
global fourthProjectNumber
fourthProjectNumber = "004"
global fifthProjectNumber
fifthProjectNumber = "005"

# 8.) E-Mail address of Super-Admin / Application-Manager:
# Use an organizational E-Mail-Address here - all emails outgoing from the system (like password forgotten emails or
# registration-notifications for the CCS in general or for the single project: this email will be used as the sender.
# use sth like: PMO@yourOrg.com or project.management@yourOrg.com or good.collaboration@yourOrg.com
# If you do not have a "yourOrg.com" email with PGP-Encryption, we suggest you to use ctemplar.com
# https://ctemplar.com/ offers a FREE account - and is super secure (located on Iceland, guaranteed no logging or content analysis)
# at https://ctemplar.com/ you'll find your public PGP-Key for download at Settings -> "Addresses / signatures" at the bottom
# of the page. (klick on the "Download public key(4096 Bit)"-link, copy-n-paste / overwrite the last value at  #11.) below.
# ensure to keep the tripple double-quotes """YOUR-MULTILINE-PUBLIC-PGP-KEY""")
global usrNumberOneEmail
usrNumberOneEmail = "ccs.user@ctemplar.com"

# 9.) User-name of Super-Admin / Application-Manager:
global usrNumberOneName
usrNumberOneName = "Super Admin"

# 10.) Password of Super-Admin / Application-Manager:
global usrNumberOnePW
usrNumberOnePW = "MySuperPassword123"

# 11.) Public PGP-Key of Super-Admin / Application-Manager's E-Mail:
# below is the PUBLIC PGP-Key associated to the email-address above.
# BE AWARE: You will not be able to read any E-Mails if E-Mail-address & Key do not fit!
global usrNumberOnesPublicPGPkey
usrNumberOnesPublicPGPkey = """-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: OpenPGP.js v3.1.3
Comment: https://openpgpjs.org

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
/Waw4xKcNtns14Rcc/o=
=JIVU
-----END PGP PUBLIC KEY BLOCK-----"""

# ensure, that:
# A) the double-quotes (or for the public PGP-Key: 3 double-quotes) are set for every value
# B) You did save the file when finished!

# If done:
# 1.) minimize / close the file
# 2.) execute the setuptest from your terminal simply by typing setuptest.py 
# 3.) click [CONTINUE] - on the next page, scroll down & click the [INSTALL] button

# ** final note to the email-provider:
# It is possible to use your own provider, but some customizing would be needed to change this.
# If you need help (with the software as well as with your organizational, incremental transition into a virtual enterprise):
# you can send me an email & ask for availability.
