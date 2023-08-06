"""
Created on 18.11.2019

@author: Florian Strahberger

TestCase: example project setup ( create a first project, create an example wbs
        - this is a showup-test, showing how to create a new project and create a work-breakdown-structure" )
        - this test is not called automatically via pytest (not starting or ending with test_ or _test),
          but is a help which can be started manually
WalkThrough:
 1. login as Super Admin / User-Number-One
 2. Go to the wbs-management page and create a project (= first wbs-element) with the subject "Collaborative Testing"
 3. Create a set of other wbs-elements to break down the project as follows:

     L1 element = Project-Level (the project name & purpose) ist the form prior the wbscreator:
 1."Automated Testing-Show" -> "A state-of-the-art test- and example walkthrough is performed"

     L2 elements:
 1.2 "Test Layout & Design" -> "Testing framework is selected and a draft is created"
 1.1 "Testing Technology"  -> "Technology is selected and made available to start working"
 1.3 "Test Walk-Through" -> "The subjects & pages for the Happy Path are selected"

     L3 elements:
 1.1.1 "Selenium Webdriver" -> "Requirements for usage on Ubuntu are listed"
 1.1.2 "PyCharm IDE" -> "IDE for Python is prepared to work with Selenium"
 1.2.1 "Page Object Model" -> "First Page-Classes and Page-TestCases are ready to run"
 1.3.1 "Test Preparation Steps" -> "Manual Clicking-Through and documenting the steps"
 1.3.2 "Building Test-Automation" -> "Python code of classes and test-steps of TCs is created"
 1.3.3 "Test the Test" -> "Test-Automation is well tested and ready to be added to the suite"

     L4 element:
 1.2.1.1 "Test Management" -> "Testing work and workflow is well integrated (ci)"
 1.2.1.2 "Test Collaboration" -> "Digital-Workspace-Suite is running & global team introduced"

     L5 element:
 1.2.1.1.1 "Continuous Integration of QA" -> "QA & Testing-Tasks are well integrated into the development cycle"

     L6 element:
 1.2.1.1.1.1 "CI Tools Selection Concepts" -> "A set of concepts for selcting CI-tools is selected"

     L7 element:
 1.2.1.1.1.1.1 "CI tools portfolio & workflow" -> "A set of CI-tools is available & test-automation is triggered automatically"


Requires to work:
 1. An installed instance of the CCS, manually installed or via docker (your "$docker-compose up --build")
 2. Via pytest or manually performed the RunSetups/ test_ini_1 - test_ini_4 setup scripts
"""
import pytest
from selenium import webdriver
import time
from Conf import test_configVars

cfg = test_configVars
from Pages import OverviewCls, newWBSelementCls, IndexCls


@pytest.fixture()
def prep_createProjectandWBS():
    global driver
    driver = webdriver.Chrome()
    yield
    driver.close()
    driver.quit()
    print(
        "The create-a-project-and-its-WBS WalkThrough ")

def test_createProjectandWBS(prep_createProjectandWBS):

    driver.get(cfg.ccsIP)
    driver.implicitly_wait(4)
    driver.maximize_window()
    assert "C.C.S. :: Entry" in driver.title
    HPlogin = IndexCls.Index(driver)
    HPlogin.enter_name(cfg.usrNumberOneName)
    HPlogin.enter_projectNr(cfg.firstProjectNumber)
    HPlogin.enter_password(cfg.usrNumberOnePW)
    HPlogin.click_ENTERbtn()
    # now click the wbs-admin btn (in overview.php):
    ## project1 login performed -> redirects to overview.php
    ovClickWbsBtn = OverviewCls.Overview(driver)
    ovClickWbsBtn.click_wbsadminBtn()
    driver.implicitly_wait(8)
    driver.maximize_window()

    createProject = newWBSelementCls.newWBSelement(driver)
    driver.implicitly_wait(4)
    time.sleep(2)
    createProject.enter_projectname("Automated Testing-Show")
    time.sleep(3)
    createProject.enter_projectdescr("A state-of-the-art test- and example walkthrough is performed")
    time.sleep(1)
    createProject.enter_projectnr("1")
    time.sleep(1)
    createProject.click_createBtn()
    ## part one is done - project (=WBS-Level1) is created
    driver.implicitly_wait(4)
    assert "TREE STRUCTURE GENERATOR :: WBS STRUCTURED DISCUSSION BOARD" in driver.title
    # showInfo = newWBSelementCls.newWBSelement(driver)
    # showInfo.mouseover_infoSpan()
    # time.sleep(5)
    # show info WBS end
    # # now start with creation of the WBS-tree:
    clickParentElement = newWBSelementCls.newWBSelement(driver)
    clickParentElement.click_parentWbsBar("wbsL1", "1 Automated Testing-Show")
    time.sleep(2)

    createChildElement = newWBSelementCls.newWBSelement(driver)
    createChildElement.enter_wbsnr("1.1")
    createChildElement.enter_wbsname("Testing Technology")
    createChildElement.enter_wbsdescr("Technology is selected and made available to start working")
    time.sleep(3)
    createChildElement.click_createBtn()
    time.sleep(2)
    # 1.2 "Test Layout & Design" -> "Testing framework is selected and a draft is created"
    clickParentElement = newWBSelementCls.newWBSelement(driver)
    clickParentElement.click_parentWbsBar("wbsL1", "1 Automated Testing-Show")
    time.sleep(2)
    ## now insert new child-element 1.2:
    createChildElement = newWBSelementCls.newWBSelement(driver)
    createChildElement.enter_wbsnr("1.2")
    createChildElement.enter_wbsname("Test Layout & Design")
    createChildElement.enter_wbsdescr("Testing framework is selected and a draft is created")
    time.sleep(3)
    createChildElement.click_createBtn()
    time.sleep(2)
    # 1.3 "Test Walk-Through" -> "The subjects & pages for the Happy Path are selected"
    clickParentElement = newWBSelementCls.newWBSelement(driver)
    clickParentElement.click_parentWbsBar("wbsL1", "1 Automated Testing-Show")
    time.sleep(2)
    ## now insert new child-element 1.3:
    createChildElement = newWBSelementCls.newWBSelement(driver)
    createChildElement.enter_wbsnr("1.3")
    createChildElement.enter_wbsname("Test Walk-Through")
    createChildElement.enter_wbsdescr("The subjects & pages for the Happy Path are selected")
    time.sleep(3)
    createChildElement.click_createBtn()
    time.sleep(2)
    # L3 elements:
    # 1.1.1 "Selenium Webdriver" -> "Requirements for usage on Ubuntu are listed"
    clickParentElement = newWBSelementCls.newWBSelement(driver)
    clickParentElement.click_parentWbsBar("wbsL2", "1.1 Testing Technology")
    time.sleep(2)
    ## now insert new child-element 1.1.1:
    createChildElement = newWBSelementCls.newWBSelement(driver)
    createChildElement.enter_wbsnr("1.1.1")
    createChildElement.enter_wbsname("Selenium Webdriver")
    createChildElement.enter_wbsdescr("Requirements for usage on Ubuntu are listed")
    time.sleep(3)
    createChildElement.click_createBtn()
    time.sleep(2)

    # 1.1.2 "PyCharm IDE" -> "IDE for Python is prepared to work with Selenium"
    clickParentElement = newWBSelementCls.newWBSelement(driver)
    clickParentElement.click_parentWbsBar("wbsL2", "1.1 Testing Technology")
    time.sleep(2)
    ## now insert new child-element 1.1.2:
    createChildElement = newWBSelementCls.newWBSelement(driver)
    createChildElement.enter_wbsnr("1.1.2")
    createChildElement.enter_wbsname("PyCharm IDE")
    createChildElement.enter_wbsdescr("IDE for Python is prepared to work with Selenium")
    time.sleep(3)
    createChildElement.click_createBtn()
    time.sleep(2)

    # 1.2.1 "Page Object Model" -> "First Page-Classes and Page-TestCases are ready to run"
    clickParentElement = newWBSelementCls.newWBSelement(driver)
    clickParentElement.click_parentWbsBar("wbsL2", "1.2 Test Layout & Design")
    time.sleep(2)
    ## now insert new child-element 1.2.1:
    createChildElement = newWBSelementCls.newWBSelement(driver)
    createChildElement.enter_wbsnr("1.2.1")
    createChildElement.enter_wbsname("Page Object Model")
    createChildElement.enter_wbsdescr("First Page-Classes and Page-TestCases are ready to run")
    time.sleep(3)
    createChildElement.click_createBtn()
    time.sleep(2)

    # 1.3.1 "Test Preparation Steps" -> "Manual Clicking-Through and documenting the steps"
    clickParentElement = newWBSelementCls.newWBSelement(driver)
    clickParentElement.click_parentWbsBar("wbsL2", "1.3 Test Walk-Through")
    time.sleep(2)
    ## now insert new child-element 1.3.1:
    createChildElement = newWBSelementCls.newWBSelement(driver)
    createChildElement.enter_wbsnr("1.3.1")
    createChildElement.enter_wbsname("Test Preparation Steps")
    createChildElement.enter_wbsdescr("Manual Clicking-Through and documenting the steps")
    time.sleep(3)
    createChildElement.click_createBtn()
    time.sleep(2)

    # 1.3.2 "Building Test-Automation" -> "Python code of classes and test-steps of TCs is created"
    clickParentElement = newWBSelementCls.newWBSelement(driver)
    clickParentElement.click_parentWbsBar("wbsL2", "1.3 Test Walk-Through")
    time.sleep(2)
    ## now insert new child-element 1.3.2:
    createChildElement = newWBSelementCls.newWBSelement(driver)
    createChildElement.enter_wbsnr("1.3.2")
    createChildElement.enter_wbsname("Building Test-Automation")
    createChildElement.enter_wbsdescr("Python code of classes and test-steps of TCs is created")
    time.sleep(3)
    createChildElement.click_createBtn()
    time.sleep(2)

    # 1.3.3 "Test the Test" -> "Test-Automation is well tested and ready to be added to the suite"
    clickParentElement = newWBSelementCls.newWBSelement(driver)
    clickParentElement.click_parentWbsBar("wbsL2", "1.3 Test Walk-Through")
    time.sleep(2)
    ## now insert new child-element 1.3.3:
    createChildElement = newWBSelementCls.newWBSelement(driver)
    createChildElement.enter_wbsnr("1.3.3")
    createChildElement.enter_wbsname("Test the Test")
    createChildElement.enter_wbsdescr("Test-Automation is well tested and ready to be added to the suite")
    time.sleep(3)
    createChildElement.click_createBtn()
    time.sleep(2)

    # 1.2.1.1 "Test Management" -> "Testing work and workflow is well integrated (ci)"
    clickParentElement = newWBSelementCls.newWBSelement(driver)
    clickParentElement.click_parentWbsBar("wbsL3", "1.2.1 Page Object Model")
    time.sleep(2)
    ## now insert new child-element 1.2.1.1:
    createChildElement = newWBSelementCls.newWBSelement(driver)
    createChildElement.enter_wbsnr("1.2.1.1")
    createChildElement.enter_wbsname("Test Management")
    createChildElement.enter_wbsdescr("Testing work and workflow is well integrated (ci)")
    time.sleep(3)
    createChildElement.click_createBtn()
    time.sleep(2)

    # 1.2.1.2 "Test Collaboration" -> "Digital-Workspace-Suite is running & global team introduced"
    clickParentElement = newWBSelementCls.newWBSelement(driver)
    clickParentElement.click_parentWbsBar("wbsL3", "1.2.1 Page Object Model")
    time.sleep(2)
    ## now insert new child-element 1.2.1.2:
    createChildElement = newWBSelementCls.newWBSelement(driver)
    createChildElement.enter_wbsnr("1.2.1.2")
    createChildElement.enter_wbsname("Test Collaboration")
    createChildElement.enter_wbsdescr("Digital-Workspace-Suite is running & global team introduced")
    time.sleep(3)
    createChildElement.click_createBtn()
    time.sleep(2)
    # 1.2.1.2 "Test Collaboration" -> "Digital-Workspace-Suite is running & global team introduced"

  # L5 element:
    clickParentElement = newWBSelementCls.newWBSelement(driver)
    clickParentElement.click_parentWbsBar("wbsL4", "1.2.1.1 Test Management")
    time.sleep(2)
    ## now insert new child-element 1.2.1.1.1:
    createChildElement = newWBSelementCls.newWBSelement(driver)
    createChildElement.enter_wbsnr("1.2.1.1.1")
    createChildElement.enter_wbsname("Continuous Integration of QA")
    createChildElement.enter_wbsdescr("QA & Testing-Tasks are well integrated into the development cycle")
    time.sleep(3)
    createChildElement.click_createBtn()
    time.sleep(2)
    ## L6 element:
    clickParentElement = newWBSelementCls.newWBSelement(driver)
    clickParentElement.click_parentWbsBar("wbsL5", "1.2.1.1.1 Continuous Integration of QA")
    time.sleep(2)
    ## now insert new child-element 1.2.1.1.1.1:
    createChildElement = newWBSelementCls.newWBSelement(driver)
    createChildElement.enter_wbsnr("1.2.1.1.1.1")
    createChildElement.enter_wbsname("CI Tools Selection Concepts")
    createChildElement.enter_wbsdescr("A set of concepts for selcting CI-tools is selected")
    time.sleep(3)
    createChildElement.click_createBtn()
    time.sleep(2)
    ## L7 element:
    clickParentElement = newWBSelementCls.newWBSelement(driver)
    clickParentElement.click_parentWbsBar("wbsL6", "1.2.1.1.1.1 CI Tools Selection Concepts")
    time.sleep(2)
    ## now insert new child-element 1.2.1.1.1.1.1:
    createChildElement = newWBSelementCls.newWBSelement(driver)
    createChildElement.enter_wbsnr("1.2.1.1.1.1.1")
    createChildElement.enter_wbsname("CI tools portfolio & workflow")
    createChildElement.enter_wbsdescr("A set of CI-tools is available & test-automation is triggered automatically")
    time.sleep(3)
    createChildElement.click_createBtn()
    time.sleep(2)
    ##


# # initial WBS created -> show C-BOARD (btn click 4 redirect):
    clickCBoard_Btn = newWBSelementCls.newWBSelement(driver)
    clickCBoard_Btn.click_cboardBtn()
    time.sleep(7)

    # # make user profile settings:
    ovClickPersProfileBtn = OverviewCls.Overview(driver)
    ovClickPersProfileBtn.click_myProfileBtn()
    time.sleep(2)

    time.sleep(12)
    # # # The Walk-Through:
    # A) Preparation:  Perform the database-table-creation -> the final installation-step
    # B) Workflow:
    # # User registration Steps
    # # Initial User Activation Steps for a project
    # # User Login -> auto redirects to overview.php (yet empty C-BOARD page)
    # # OverviewTC_1 (only btn click wbscreator)
    # # wbscreatorTC a) building Project b) building the WBS & click C-BOARD btn

    # # OverviewTC_2 (click UserProfile btn)
    ## persProfileTC(perform some inserts - maybe open riemannThomann test, check click the test, use the results)
    ## click C-BOARD btn
    ## enter some posts into one wbs-forum as an example (with directAnsw.php)
    ## show the C-WEEK
    ## logout
    ## open the sendgrid user registration page (maybe with an afiliate code ..)
