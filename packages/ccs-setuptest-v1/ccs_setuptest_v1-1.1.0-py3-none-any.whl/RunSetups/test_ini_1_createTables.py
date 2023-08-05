"""
Created on 18.11.2019

@author: Florian Strahberger

TestCase: initial setup ( create database-tables for meta-db & 5 project-databases
        - the next step after your "$docker-compose up --build" )
WalkThrough (test_ini_1 - test_ini_4):
 1. create database-tables for meta-db & 5 project-databases
 2. register a Super-User, the "User-Number-One" (will have mandatory administration permission everywhere in the CCS)
 3. insert the email-provider (we use sendgrid, else customizing is needed) & project-manager for slot1
 4. insert email-provider & project-manager for slot2, slot3, slot4 & slot5
This: create database-tables for meta-db & 5 project-databases:
 1. Direct calls of [IP]/zubringer/create5MetaDBTables.php & [IP]/1-5/zubringer/create8Tables.php
Yield: database-tables for the ccs-wide usage (like user-data & project-slot-information) plus
        database-tables for the first 5 projects (project-specific data like wbs-elements, threads, posts, attachment-links...)
Not: no functions are tested here, this is an automated preparation step (not only for testing, but for setting-up the CCS)

Requires to work:
 1. An installed instance of the CCS, manually installed or via docker (your "$docker-compose up --build")
 2. Correct setting of the IP of the CCS within the Conf/test_configVars.py configuration file
"""

import pytest
from selenium import webdriver
import time
from Conf import test_configVars

cfg = test_configVars


@pytest.fixture()
def prep_iniCreate6tables():
    global driver
    driver = webdriver.Chrome()
    yield
    driver.close()
    driver.quit()
    print(
        "Initial-setup with the creation of the 6 database-tables (1x metaDB, 5x projectDBs) completed.")

def test_iniCreate6tables(prep_iniCreate6tables):
    # call initially the db-table-creators for metaDB + 5 projectDBs:
    # meta db:
    driver.get(cfg.ccsIP + "/zubringer/create5MetaDBTables.php")
    time.sleep(2)
    # driver.implicitly_wait(8)
    assert driver.page_source.find("Created reg Table (5 of 5 for MetaDB).")
    # project 1 db:
    driver.get(cfg.ccsIP + "/1/zubringer/create8Tables.php")
    time.sleep(2)
    # driver.implicitly_wait(8)
    assert driver.page_source.find("Table (8 of 8 tables")
    # project 2 db:
    driver.get(cfg.ccsIP + "/2/zubringer/create8Tables.php")
    time.sleep(2)
    # driver.implicitly_wait(8)
    assert driver.page_source.find("Table (8 of 8 tables")
    # project 3 db:
    driver.get(cfg.ccsIP + "/3/zubringer/create8Tables.php")
    time.sleep(2)
    # driver.implicitly_wait(8)
    assert driver.page_source.find("Table (8 of 8 tables")
    # project 4 db:
    driver.get(cfg.ccsIP + "/4/zubringer/create8Tables.php")
    time.sleep(2)
    # driver.implicitly_wait(8)
    assert driver.page_source.find("Table (8 of 8 tables")
    # project 5 db:
    driver.get(cfg.ccsIP + "/5/zubringer/create8Tables.php")
    time.sleep(2)
    # driver.implicitly_wait(8)
    assert driver.page_source.find("Table (8 of 8 tables")

