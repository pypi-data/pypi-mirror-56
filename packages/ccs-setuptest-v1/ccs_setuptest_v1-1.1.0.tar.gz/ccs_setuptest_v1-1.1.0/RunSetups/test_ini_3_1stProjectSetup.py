'''
Created on 18.11.2019

@author: Florian Strahberger

TestCase: initial setup (email-provider & project-manager, in general & for a first project)
WalkThrough (test_ini_1 - test_ini_4):
 1. create database-tables for meta-db & 5 project-databases
 2. register a Super-User, the "User-Number-One" (will have mandatory administration permission everywhere in the CCS)
 3. insert the email-provider (we use sendgrid, else customizing is needed) & project-manager for slot1
 4. insert email-provider & project-manager for slot2, slot3, slot4 & slot5
This: email-provider & project-manager, in general & for slot1 is set:
 1. Direct call of [IP]/ccs_projects-management.php
 2. Performing inserts of email-provider & project-manager for the project in slot 1
Yield: email-provider for CCS-wide transactional emails is set;
        email-provider & project-manager for 1st project / slot1 is available.
        Email-provider of 1st project will be used for CCS-wide transactional emails (eg: all user-registration-emails), too;
Not: no email functionalities or any functions are tested here, this is an automated preparation step (not only for testing)

Requires to work:
 1. Successfully ran nttest_ini_1_createTables.py (databases & tables)
 2.Working settings in the Conf/test_configVars.py (User-Number-One & email-provider values)
'''
import pytest
from selenium import webdriver
import time
from Conf import test_configVars

cfg = test_configVars
from Pages import ccs_projectsManagementCls

@pytest.fixture()
def prep_project1Setup():
    global driver
    driver = webdriver.Chrome()
    yield
    driver.close()
    driver.quit()
    print(
        "Test & initial-setup Walk-Through for setting-up the very first project (project-manager & sendgrid API-Key for email-provider)."
    )

def test_project1Setup(prep_project1Setup):
    mang = ccs_projectsManagementCls.ccs_projectsManagementCls(driver)
    #  here: no login needed (empty db-table yet) -> direct call of ccs_projects-management.php is possible for access:
    driver.get(cfg.ccsIP + "/ccs_projects-management.php")
    time.sleep(4)
    driver.maximize_window()
    assert "CCS: PROJECTS-TABLE-INITIAL-MANAGEMENT" in driver.title
    #  project slot 1 project number one user-number-one:
    mang.ini_enter_projectNr(cfg.firstProjectNumber)
    mang.ini_enter_adminEMail(cfg.usrNumberOneEmail)
    mang.ini_enter_adminEMailPGPkey(cfg.usrNumberOnesPublicPGPkey)
    mang.ini_enter_providerName("apikey")
    mang.ini_enter_providerPass(cfg.sendgridAPIkey)
    mang.ini_enter_providerPort("465")
    mang.ini_enter_providerHost("smtp.sendgrid.net")
    mang.ini_enter_providerEnc("ssl")
    mang.ini_click_SetTheseValuesbtn()  # will redirect to index.php
    time.sleep(2)
    assert "C.C.S. :: Entry" in driver.title
    time.sleep(3)
    #  first project is created - we can use this for testing the initial project-registration, login & further tests
