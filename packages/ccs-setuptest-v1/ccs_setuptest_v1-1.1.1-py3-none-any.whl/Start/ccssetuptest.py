#!/usr/bin/env python3
"""
Created on 15.11.2019

@author: Florian Strahberger

Usage: Start the "Setup-, Install- & Test-WalkThrough" by typing:

	python3 ccs-setuptest.py


This will:
A) give you the option to modify the setup variables used for the installation stored in the Conf/test_configVars.py
B) run the Installation & perform a "ShowUp-Test" with these values by running the 7 WalkThroughs mentioned below:

Context: The setuptest is made for automating the initial setup, so the following steps are covered:
 1. create database-tables for meta-db & 5 project-databases
 2. register a Super-User, the "User-Number-One" (will have mandatory administration permission everywhere in the CCS)
 3. insert the email-provider (we use sendgrid, else customizing is needed) & project-manager for slot1
 4. insert email-provider & project-manager for slot2, slot3, slot4 & slot5
 5. create a project and a wbs
 6. login and make some posts
 7. login and create a user-profile including the personality test

Requires to work:

Steps needed to be done before
 1. Installed an instance of the CCS, manually installed or via docker (your "$docker-compose up --build")
 2. a sendgrid-account with its API-Key at hand (application is working well with FREE accounts)
 3. In the Conf/test_configVars.py the correct values - from the IP, the sendgrid-Key, the admin's name, email,
  password, public pgp key for that email, project-Numbers.
  below is a list for the needed values:

 The following variables need to be set prior running the setup: (number after the variable is the RunSetups/ id of the setup-file(s) where the variable is needed for):
    ccsIP	(mandatory**)	1,2,3,4
    sendgridAPIkey		    3,4
    usrNumberOneName		    2,4
    usrNumberOnePW		    2,4
    usrNumberOneEmail		  2,3,4
    usrNumberOnesPublicPGPkey	  2,3,4
    firstProjectNumber		    3,4
    secondProjectNumber		      4
    thirdProjectNumber		      4
    fourthProjectNumber		      4
    fifthProjectNumber		      4

** only the ccsIP-value is really mandatory - IP of your server, or localhost if installed on your local machine.
However, for a better experience without receiving errors I really do recommend to make a https://sendgrid.com/free/ Registration & use a working API-Key
as well as using an E-Mail with a proper publicPGP-Key as well. (get one for free at https://ctemplar.com/ than: setting (gear-icon) -> "Addresses & signatures" -> scroll down & click the "Download public key(4096)" link)
"""
from Start import starterclass

if __name__ == "__main__":
    starterclass.startclass()

