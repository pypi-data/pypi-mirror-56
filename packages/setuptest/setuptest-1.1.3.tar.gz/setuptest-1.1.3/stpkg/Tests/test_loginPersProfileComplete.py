"""
Created on 18.11.2019

@author: Florian Strahberger

TestCase: example pers. profile setup & pers. WBS administration
        ( create a first personal profile as an example - and test the functionality of the CFLX in the persProfile area)
        - this is a showup-test, showing how to create a pers profile and test the CFLX CRUD-functionality
        - this test can be called automatically via pytest (is starting with _test)
WalkThrough:
 1. login as Super Admin / User-Number-One
 2. Go to the persProfile page and create a profile
 3. Go to the Riemann-Thomann page and perform a personality test
 4. Return to the persProfile to enter the assessment results
 5. Perform the CRUD operations at the CFLX area at the bottom of the page.

Requires to work:
 1. An installed instance of the CCS, manually installed or via docker (your "$docker-compose up --build")
 2. Via pytest or manually performed the RunSetups/ test_ini_1 - test_ini_4 setup scripts
"""
import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
from Conf import test_configVars

cfg = test_configVars
from Pages import OverviewCls, IndexCls, OnlineAssessmentCls
from Pages import persProfileCls


@pytest.fixture()
def prep_createPersProfile():
    global driver
    driver = webdriver.Chrome()
    yield
    driver.close()
    driver.quit()
    print(
        "Login, show & populate the pers. user-profile with values, perform a personality assessment and show the default CFLX.")

def test_createPersProfile(prep_createPersProfile):
    ## needs login first:
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
    # # make user profile settings:
    ovClickPersProfileBtn = OverviewCls.Overview(driver)
    ovClickPersProfileBtn.click_myProfileBtn()
    time.sleep(2)
    assert "C.C.S.: personal profile -> give trust, earn trust" in driver.title
    myData = persProfileCls.persProfile(driver)
    # MAIN DATA:
    myData.enter_myFirstName("Florian")
    myData.enter_myLastName("Strahberger")
    myData.enter_myPhoneNo("+49 163 253 13 76")
    myData.enter_myTimeZone("CET")
    myData.enter_myEmailAddress("florian.strahberger@cyconet.xyz")
    myData.click_mainDataSubmitBtn()
    # PREFERENCES:
    myData.enter_myRole("""+ Member of the Global Testing Staff, SCRUM-Master & Project-QA-Manager;
    + CCS-Application-Manager;
    + Group-Leader of the software testing team;
    + Owner of cyconet, the maker of the CYBR CSCW-SUITE.""")
    myData.enter_mySkills("""+ Business Engineering,
    + classical ProjectManagement,
    + ISTQB-certified software tester,
    + certified agile-tester,
    + some Software-Engineering""")
    # # a new instance (driverB) for the external assessment hier Einschub: RiemannThomannTest (2do: Umzug auf cyconet.xyz/Self-Assessment.php) -------------------------
    driverB = webdriver.Chrome()
    driverB.get(cfg.ccsIP + "/ass1.php")
    driverB.implicitly_wait(4)
    driverB.maximize_window()
    assert "RIEMANN-THOMANN TEST :: Online assessment of individual nearness and risk preferences" in driverB.title
    selftest = OnlineAssessmentCls.OnlineAssessment(driverB)
    # insert 24 values:
    Vals = [1, 5, 5, 5, 2, 5, 5, 5, 3, 2, 6, 5, 3, 4, 2, 5, 2, 4, 5, 3, 4, 6, 6, 6]
    for pos, val in enumerate(Vals, start=1):
        selftest.select_radio_btn("f{}n{}".format(pos, val))
    # click RUN TEST btn:
    selftest.click_RunTest_Btn()
    time.sleep(4)
    # get the Values for usage in the persProfile
    nearnessValue = selftest.get_nearness_value()
    riskValue = selftest.get_risk_value()
    driverB.close()
    #     def click_areaTable(self, area):
    #     # contains 5 sub-tables: mainAreaTable, preferencesAreaTable, miscAreaTable, pgpAreaTable, cflxAreaTable
    myData.click_areaTable("preferencesAreaTable")
    # the assessment-test is done here - only a call to the two result-value-functions is performed yet to insert these values into the persProfile now: ------------------
    # # proceed with persProfile, calling the functions for the values (evtl. a print or return there is needed then ..)
    myData.enter_myNearness(nearnessValue)
    myData.enter_myRisk(riskValue)
    myData.enter_myComment("""... after WW2 a young German soldier did escape from a prisoner of war camp
    and managed to flee over the Alps back to Germany,
    where he did find a hiding-place within a henhouse.
    My grandmother was responsible for the hens these days and did discover him.
     ...
    ...My other grandmother was displaced from Silesia because of the lost war,
    did meet my namegiver from Lower Bavaria and 
    they both moved to the district of Lindau at the Lake of Constance,
    where my namegiver did found a building company which later became my father's one.
    Spirit of adventure & entrepreneurship is in my blood, would be a conclusion and is subsuming my passion.""")
    time.sleep(3)
    myData.click_preferencesDataSubmitBtn()

    # # MISCELLANEOUS
    myData.click_areaTable("miscAreaTable")
    # click into the area to position page-selection:

    myData.enter_myLinklist("""maybe later aligator ... my cflx bot, my companies pages incl facebook,"
    https://www.project-syndicate.org
     <a href='https://www.project-syndicate.org'>linktest shouldnt work</a>""")
    myData.enter_myInterests("""Mountain Climbing, Cycling, Ski-Hiking, Chess, 
    and sometimes I go out and do have a beer or two 
    or I am just striving through the city seeking for some new experiences..""")
    myData.click_miscDataSubmitBtn()
    myData.click_areaTable("cflxAreaTable")
    myData.misuse_pgpTextarea("""Hello dear software-presentation-test viewer! You only need to make inserts into this field if you need to update your public PGP-Key - so, I do not click the UPLOAD button yet and proceed to the CFLX management area below. I hope you enjoy the show, so far ..\n"
                              - and yes: I am authentic.""")
    # # public PGP key field could be misused and asserted for correct error-,mssg on upload-try - like entering some description, speaking to the audience "hope you enjoy the test - and yes: I am authentic."
    time.sleep(12)

    # # start CFLX now -------------------------------

    # the dropdown-mouseover-function:
    def CFLX_hover(linktext):
        CFLXselected = driver.find_element_by_link_text(linktext)
        hoverElem = ActionChains(driver).move_to_element(CFLXselected)
        hoverElem.perform()

    # move mouse ActionChains -> move_by_offset
    # # https://selenium-python.readthedocs.io/api.html?highlight=mouse#selenium.webdriver.common.action_chains.ActionChains.move_by_offset
    def mouse_move(xoff, yoff):
        actions = ActionChains(driver)
        actions.move_by_offset(xoff, yoff).context_click().perform()

    # click into page-area:
    myData.click_ss_dropdown()
    # hover and select the default ss's cflx:
    CFLX_hover("Status Statements")
    myData.click_cflx_by_id("ss1")
    myData.click_cflx_by_id("ss2")
    myData.click_cflx_by_id("ss3")
    myData.click_cflx_by_id("ss4")
    # hover and select the default qr's cflx:
    CFLX_hover("Question Repeats")
    myData.click_cflx_by_id("qr1")
    myData.click_cflx_by_id("qr2")
    myData.click_cflx_by_id("qr3")
    myData.click_cflx_by_id("qr4")
    # hover and select the default im's cflx:
    CFLX_hover("I-Messages")
    myData.click_cflx_by_id("im1")
    myData.click_cflx_by_id("im2")
    myData.click_cflx_by_id("im3")
    myData.click_cflx_by_id("im4")
    # hover and select the default ap's cflx:
    CFLX_hover("Appeals")
    myData.click_cflx_by_id("ap1")
    myData.click_cflx_by_id("ap2")
    myData.click_cflx_by_id("ap3")
    myData.click_cflx_by_id("ap4")
    myData.click_areaTable("cflxAreaTable")
    # add new CFLX (ss,qr,im,ap):

    #     def insert_new_cflx(self, input_id, newCflxText):
    myData.insert_new_cflx("SSTextBox", "Managing personal Clarity-Statements is working fine")
    time.sleep(2)
    myData.click_add_to_database_btn("sssubmit")
    myData.insert_new_cflx("QRTextBox", "You were asking, if the users can manage their own, personalized CFLX here")
    time.sleep(2)
    myData.click_add_to_database_btn("qrsubmit")
    myData.insert_new_cflx("IMTextBox", "I think, it's a great idea to 'Test-n-Show' new applications like this")
    time.sleep(2)
    myData.click_add_to_database_btn("imsubmit")
    myData.insert_new_cflx("APTextBox",
                           "I want you to make yourself some thoughts where to adapt 'Test-n-Shows' for your apps")
    time.sleep(2)
    myData.click_add_to_database_btn("apsubmit")
    myData.click_areaTable("cflxAreaTable")
   # due to some false positives / inconsitent test-behavoir, the remove is commented out here.
    # # now hover and select the new - add a reading-time - and delete them and show deleted state then:
  #  CFLX_hover("Status Statements")
  #  time.sleep(2)
  #  myData.click_cflx_by_linktext("Managing personal Clarity-Statements is working fine")
  #  time.sleep(3)
  #  mouse_move(10, -44)
  #  myData.click_delete_it_btn("del_statstat_btn")
  # CFLX_hover("Status Statements")
  #  time.sleep(2)
  #  # # QR:
  #  CFLX_hover("Question Repeats")
  #  time.sleep(2)
  #  myData.click_cflx_by_linktext("You were asking, if the users can manage their own, personalized CFLX here")
  #  time.sleep(3)
  #  mouse_move(0, -66)
  #  myData.click_delete_it_btn("del_qr_btn")
  #  CFLX_hover("Question Repeats")
  #  time.sleep(2)
  #  # # IM:
  #  CFLX_hover("I-Messages")
  #  time.sleep(2)
  #  myData.click_cflx_by_linktext("I think, it's a great idea to 'Test-n-Show' new applications like this")
  #  time.sleep(3)
  #  mouse_move(0, -66)
  #  myData.click_delete_it_btn("del_im_btn")
  #  CFLX_hover("I-Messages")
  #  time.sleep(2)
  #  # # AP:
  #  CFLX_hover("Appeals")
  #  time.sleep(2)
  #  myData.click_cflx_by_linktext(
  #      "I want you to make yourself some thoughts where to adapt 'Test-n-Shows' for your apps")
  #  time.sleep(3)
  #  mouse_move(0, -66)
  #  myData.click_delete_it_btn("del_ap_btn")

    #CFLX_hover("Appeals")
    time.sleep(4)
    #myData.click_areaTable("cflxAreaTable")
    # done with pers profile (personality-test is still missing..)
    # click c-board button -> perform threadview.php operations now:
    myData.click_cBoard_btn()

    time.sleep(4)
    ## nxt: make some postings - and give explanations, ask questions, give direct answers ..

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
