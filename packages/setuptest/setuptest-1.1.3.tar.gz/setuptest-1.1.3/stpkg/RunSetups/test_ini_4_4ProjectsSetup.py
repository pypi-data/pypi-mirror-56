"""
Created on 18.11.2019

@author: Florian Strahberger

TestCase: initial setup (database tables, email-provider & project-managers for slot 1,2,3,4 & 5)
WalkThrough (test_ini_1 - test_ini_4):
 1. create database-tables for meta-db & 5 project-databases
 2. register a Super-User, the "User-Number-One" (will have mandatory administration permission everywhere in the CCS)
 3. insert the email-provider (we use sendgrid, else customizing is needed) & project-manager for slot1
 4. insert email-provider & project-manager for slot2, slot3, slot4 & slot5
This step of initial Setup: email-provider & project-manager for slot 2-5 is set by iterating 4-times with:
 1. login into the last created project as Super-User (= "User-Number-One") with the credentials stored in the test_configVars.py file
 2. perform the project-registration needed for the first login-attempt into a project (this will INSERT project-permission into project's database)
 3. will redirect to the gate.php (enter the project-number & click enter)
 4  will redirect to the C-BOARD (verify via assert title)
 5. Perform a direct call of [IP]/ccs_projects-management.php
 6. Performing inserts of email-provider & project-manager for the projects in slots 2-5
Yield: email-provider & project-manager for the projects 2-5 is available & project-registration & login is tested as well
        (he/she will be informed for giving access to the newly registered team-mates of the specific projects then).
        NOTE: You can always change / update these settings later (like assigning a new project-manager of
        giving other project-NUMBERs for the slot-mappings or adding new sendgrid API-keys for different projects ...)
Not: no email functionalities or any functions are tested here, this is an automated preparation step (not only for testing,
but for automating the initial setup steps as well as showing how to perform these steps & get acquainted with the CCS)

Requires to work:
 1. Successfully ran nttest_ini_1_createTables.py (databases & tables)
 2. The User-Number-One must exist, registered with the credentials stored in the global vars of Config/test_configVars.py
 3. Working settings in the Conf/test_configVars.py (testManager vars & email-provider values)

 Page-Classes we use:
 1. IndexCls.Index (login-form on index.php)
 2. ccs_projectsManagementCls.ccs_projectsManagementCls (the CCS setup-tool, usually needs admin-permission:
  a) perform a normal login with the "User-Number-One"
  b) directly call the page via browser:  [IP]/ccs_projects-management.php
  BE AWARE: in case there is no entry/ for the very first project,
   this page can be called without any restriction from everybody for setting-up the very first project !!
"""

import pytest
from selenium import webdriver
import time
from Conf import test_configVars

cfg = test_configVars
from Pages import ccs_projectsManagementCls
from Pages import GateCls, ProjectRegisterCls, IndexCls


@pytest.fixture()
def prep_projectsSetup():
    global driver
    driver = webdriver.Chrome()
    yield
    driver.close()
    driver.quit()
    print(
        "Test & initial-setup WalkThrough for setting-up 4 more projects ("
        "with the Project-Numbers: ", cfg.secondProjectNumber, cfg.thirdProjectNumber, cfg.fourthProjectNumber, cfg.fifthProjectNumber, ") and their managers.")


def test_projectsSetup(prep_projectsSetup):
    mang = ccs_projectsManagementCls.ccs_projectsManagementCls(driver)
    indx = IndexCls.Index(driver)
    projreg = ProjectRegisterCls.ProjectRegister(driver)
    gate = GateCls.Gate(driver)
    # a) try login to last created project
    # b) perform project registration
    # c) login via gate (& assert C-BOARD page title)
    # d) direct call of ccs-management & make settings (set project's email-provider & project-manager)
    #  -> in next iteration we start with a check if project was created
    #  by performing a registration for & a login into that project

    # START 1: login to project 1 & perform project registration, then jump to ccs-management & setup project 2:
    # project 2 of 5:
    # for the first login we need to open the index.php manually - in later iterations is an automated redirect:
    driver.get(cfg.ccsIP + "/index.php")
    time.sleep(4)
    driver.maximize_window()
    assert "C.C.S. :: Entry" in driver.title
    time.sleep(4)
    indx.enter_projectNr(cfg.firstProjectNumber)
    indx.enter_name(cfg.usrNumberOneName)
    indx.enter_password(cfg.usrNumberOnePW)
    indx.click_ENTERbtn()
    # first login-attempt will lead to project-registration - do registration:
    time.sleep(4)
    assert "CCS - Project Registration" in driver.title
    projreg.click_regbtn()
    # performs registration (database & email operations) & redirects to the gate.php - so we wait 6 seconds:
    time.sleep(6)
    assert "CCS - a CYCONET.XYZ Solution :: Entry" in driver.title
    gate.enter_projectNr(cfg.firstProjectNumber)
    gate.click_ENTERbtn()
    # wait'n verify login into C-BOARD via assert title:
    time.sleep(4)
    assert "C-BOARD: enhanced communication -> advanced collaboration" in driver.title
    # b) ccs management setup projects 2 (of 5):
    driver.get(cfg.ccsIP + "/ccs_projects-management.php")
    time.sleep(4)
    assert "CCS: PROJECTS-TABLE-INITIAL-MANAGEMENT" in driver.title
    mang.ini_enter_projectNr(cfg.secondProjectNumber)
    mang.ini_enter_adminEMail(cfg.usrNumberOneEmail)
    mang.ini_enter_adminEMailPGPkey(cfg.usrNumberOnesPublicPGPkey)
    mang.ini_enter_providerName("apikey")
    mang.ini_enter_providerPass(cfg.sendgridAPIkey)
    mang.ini_enter_providerPort("465")
    mang.ini_enter_providerHost("smtp.sendgrid.net")
    mang.ini_enter_providerEnc("ssl")
    mang.ini_click_SetTheseValuesbtn()
    # redirects to index.php, so:

    # START 2: login to project 2 & perform project registration, then jump to ccs-management & setup project 3:
    # project 3 of 5:
    time.sleep(4)
    driver.maximize_window()
    assert "C.C.S. :: Entry" in driver.title
    time.sleep(4)
    indx.enter_projectNr(cfg.secondProjectNumber)
    indx.enter_name(cfg.usrNumberOneName)
    indx.enter_password(cfg.usrNumberOnePW)
    indx.click_ENTERbtn()
    # first login-attempt will lead to project-registration - do registration:
    time.sleep(4)
    assert "CCS - Project Registration" in driver.title
    projreg.click_regbtn()
    # performs registration (database & email operations) & redirects to the gate.php - so we wait 6 seconds:
    time.sleep(6)
  #  assert "CCS - a CYCONET.XYZ Solution :: Entry" in driver.title
    gate.enter_projectNr(cfg.secondProjectNumber)
    gate.click_ENTERbtn()
    # wait'n verify login into C-BOARD via assert title:
    time.sleep(4)
    assert "C-BOARD: enhanced communication -> advanced collaboration" in driver.title
    # b) ccs management setup projects 3 (of 5):
    driver.get(cfg.ccsIP + "/ccs_projects-management.php")
    time.sleep(4)
    assert "CCS: PROJECTS-TABLE-INITIAL-MANAGEMENT" in driver.title
    mang.ini_enter_projectNr(cfg.thirdProjectNumber)
    mang.ini_enter_adminEMail(cfg.usrNumberOneEmail)
    mang.ini_enter_adminEMailPGPkey(cfg.usrNumberOnesPublicPGPkey)
    mang.ini_enter_providerName("apikey")
    mang.ini_enter_providerPass(cfg.sendgridAPIkey)
    mang.ini_enter_providerPort("465")
    mang.ini_enter_providerHost("smtp.sendgrid.net")
    mang.ini_enter_providerEnc("ssl")
    mang.ini_click_SetTheseValuesbtn()
    # 3rd done - redirects to index.php, so:
# --- ok --

    # START 3: login to project 3 & perform project registration, then jump to ccs-management & setup project 4:
    # project 4 of 5:
    time.sleep(4)
    driver.maximize_window()
    assert "C.C.S. :: Entry" in driver.title
    time.sleep(4)
    indx.enter_projectNr(cfg.thirdProjectNumber)
    indx.enter_name(cfg.usrNumberOneName)
    indx.enter_password(cfg.usrNumberOnePW)
    indx.click_ENTERbtn()

    # first login-attempt will lead to project-registration - do registration:
    time.sleep(4)
    assert "CCS - Project Registration" in driver.title
    projreg.click_regbtn()

  # performs registration (database & email operations) & redirects to the gate.php - so we wait 6 seconds:
    time.sleep(6)
  #  assert "CCS - a CYCONET.XYZ Solution :: Entry" in driver.title
    gate.enter_projectNr(cfg.thirdProjectNumber)
    gate.click_ENTERbtn()

  # wait'n verify login into C-BOARD via assert title:
    time.sleep(4)
    assert "C-BOARD: enhanced communication -> advanced collaboration" in driver.title

 #b)ccs management setup projects 4 (of 5):
    driver.get(cfg.ccsIP + "/ccs_projects-management.php")
    time.sleep(4)
    assert "CCS: PROJECTS-TABLE-INITIAL-MANAGEMENT" in driver.title
    mang.ini_enter_projectNr(cfg.fourthProjectNumber)
    mang.ini_enter_adminEMail(cfg.usrNumberOneEmail)
    mang.ini_enter_adminEMailPGPkey(cfg.usrNumberOnesPublicPGPkey)
    mang.ini_enter_providerName("apikey")
    mang.ini_enter_providerPass(cfg.sendgridAPIkey)
    mang.ini_enter_providerPort("465")
    mang.ini_enter_providerHost("smtp.sendgrid.net")
    mang.ini_enter_providerEnc("ssl")
    mang.ini_click_SetTheseValuesbtn()
    # 4th done - redirects to index.php, so:

    # START 4: login to project 3 & perform project registration, then jump to ccs-management & setup project 4:
    # project 5 of 5:
    time.sleep(4)
    driver.maximize_window()
    assert "C.C.S. :: Entry" in driver.title
    time.sleep(4)
    indx.enter_projectNr(cfg.fourthProjectNumber)
    indx.enter_name(cfg.usrNumberOneName)
    indx.enter_password(cfg.usrNumberOnePW)
    indx.click_ENTERbtn()

    # first login-attempt will lead to project-registration - do registration:
    time.sleep(4)
    assert "CCS - Project Registration" in driver.title
    projreg.click_regbtn()

    # performs registration (database & email operations) & redirects to the gate.php - so we wait 6 seconds:
    time.sleep(6)
    #  assert "CCS - a CYCONET.XYZ Solution :: Entry" in driver.title
    gate.enter_projectNr(cfg.fourthProjectNumber)
    gate.click_ENTERbtn()

    # wait'n verify login into C-BOARD via assert title:
    time.sleep(4)
    assert "C-BOARD: enhanced communication -> advanced collaboration" in driver.title

    # b)ccs management setup projects 5 (of 5):
    driver.get(cfg.ccsIP + "/ccs_projects-management.php")
    time.sleep(4)
    assert "CCS: PROJECTS-TABLE-INITIAL-MANAGEMENT" in driver.title
    mang.ini_enter_projectNr(cfg.fifthProjectNumber)
    mang.ini_enter_adminEMail(cfg.usrNumberOneEmail)
    mang.ini_enter_adminEMailPGPkey(cfg.usrNumberOnesPublicPGPkey)
    mang.ini_enter_providerName("apikey")
    mang.ini_enter_providerPass(cfg.sendgridAPIkey)
    mang.ini_enter_providerPort("465")
    mang.ini_enter_providerHost("smtp.sendgrid.net")
    mang.ini_enter_providerEnc("ssl")
    mang.ini_click_SetTheseValuesbtn()
    # 5th done - redirects to index.php, so:

    # START final assertion: login to project 5 & perform project registration, login & check C-BOARD title:
    time.sleep(4)
    driver.maximize_window()
    assert "C.C.S. :: Entry" in driver.title
    time.sleep(4)
    indx.enter_projectNr(cfg.fifthProjectNumber)
    indx.enter_name(cfg.usrNumberOneName)
    indx.enter_password(cfg.usrNumberOnePW)
    indx.click_ENTERbtn()
# first login-attempt will lead to project-registration - do registration:
    time.sleep(4)
    assert "CCS - Project Registration" in driver.title
    projreg.click_regbtn()
    # performs registration (database & email operations) & redirects to the gate.php - so we wait 6 seconds:
    time.sleep(6)
 #   assert "CCS - a CYCONET.XYZ Solution :: Entry" in driver.title
    gate.enter_projectNr(cfg.fifthProjectNumber)
    gate.click_ENTERbtn()
    # wait'n verify login into C-BOARD via assert title:
    time.sleep(4)
    assert "C-BOARD: enhanced communication -> advanced collaboration" in driver.title
    time.sleep(4)
    # assertion of 5th project creation was performed

