"""
Created on 18.11.2019

@author: Florian Strahberger

TestCase: initial setup (Create the "User-Number-One" or "Super Admin" via the very first user registration)
WalkThrough (test_ini_1 - test_ini_4):
 1. create database-tables for meta-db & 5 project-databases
 2. register a Super-User, the "User-Number-One" (will have mandatory administration permission everywhere in the CCS)
 3. insert the email-provider (we use sendgrid, else customizing is needed) & project-manager for slot1
 4. insert email-provider & project-manager for slot2, slot3, slot4 & slot5
This: create / register a Super-User:
 1. Direct call of [IP]/login/register.php
 2. Insert values
Yield: A Super-User for the CCS, the "User-Number-One" is created
Not: no functions are tested here, this is an automated preparation step (not only for testing, but for setting-up the CCS)

Requires to work:
 1. An installed instance of the CCS, manually installed or via docker (eg via: "$docker-compose up --build")
 2. Successfully ran the nttest_ini_1_createTables.py for creating the database-tables
 3. Correct setting of the IP of the CCS within the Conf/test_configVars.py configuration file
"""

import pytest
from selenium import webdriver
import time
from Conf import test_configVars

cfg = test_configVars
from Pages import RegisterCls


@pytest.fixture()
def prep_superAdminReg():
    global driver
    driver = webdriver.Chrome()
    yield
    driver.close()
    driver.quit()
    print(
        "Test & initial-setup for Super-User / User-Number-One registration Walk-Through completed.")


def test_superAdminReg(prep_superAdminReg):
    reg = RegisterCls.Register(driver)
    usrName = cfg.usrNumberOneName
    usrEmail = cfg.usrNumberOneEmail
    usrPW = cfg.usrNumberOnePW
    usrPGPKey = cfg.usrNumberOnesPublicPGPkey

    driver.get(cfg.ccsIP + "/login/register.php")
    time.sleep(4)
    assert "C.C.S. :: NEW USER REGISTRATION" in driver.title
    # driver.implicitly_wait(8)
    driver.maximize_window()

    reg.enter_username(usrName)
    reg.enter_email(usrEmail)
    reg.enter_pw(usrPW)
    reg.enter_pubkey(usrPGPKey)
    reg.click_regbtn()
    # user-number-one registration redirects to the ccs_management
    # for setting-up the email-provider & initial project(s)
    # via: "header ('Location: ../ccs_projects-management.php');" in login/reg_exec.php for this case
    time.sleep(6)
    assert "CCS: PROJECTS-TABLE-INITIAL-MANAGEMENT" in driver.title
