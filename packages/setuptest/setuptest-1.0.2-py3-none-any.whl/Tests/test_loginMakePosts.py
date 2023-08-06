"""
Created on 18.11.2019

@author: Florian Strahberger

TestCase: create posts in WBS-Elements ( create a first post % direct answer for every wbs-level )
        - this is a simple automation for filling the C-BOARD with posts (useful for developing a new styling)" )
        - this test is not available within the default setup-tests (in most cases, it is not useful)
WalkThrough:
 1. login as Super Admin / User-Number-One
 2. Go to the threadview.php of the wbs-element by clicking its default-ini-thread
 3. Make a post
 4. Create a direct answer for that post
 5. iterate 2,3,4 through all levels of the default ini-threads

     L1 element = Project-Level (the project name & purpose) ist the form prior the wbscreator:
 1."Automated Testing-Show" -> "A state-of-the-art test- and example walkthrough is performed"

     L2 elements:
 1.2 "Test Layout & Design" -> "Testing framework is selected and a draft is created"

     L3 elements:
 1.2.1 "Page Object Model" -> "First Page-Classes and Page-TestCases are ready to run"

     L4 element:
 1.2.1.1 "Test Management" -> "Testing work and workflow is well integrated (ci)"

     L5 element:
 1.2.1.1.1 "Continuous Integration of QA" -> "QA & Testing-Tasks are well integrated into the development cycle"

     L6 element:
 1.2.1.1.1.1 "CI Tools Selection Concepts" -> "A set of concepts for selcting CI-tools is selected"

     L7 element:
 1.2.1.1.1.1.1 "CI tools portfolio & workflow" -> "A set of CI-tools is available & test-automation is triggered automatically"


Requires to work:
 1. An installed instance of the CCS, manually installed or via docker (your "$docker-compose up --build")
 2. Via pytest or manually performed the RunSetups/ test_ini_1 - test_ini_4 setup scripts
 3. Via pytest ran the test_loginCreateProjectCreateWBS.py (for generating the wbs-elements with its initial-threads)
"""
import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
from Conf import test_configVars

cfg = test_configVars
from Pages import OverviewCls, IndexCls
from Pages import ThreadviewCls


@pytest.fixture()
def prep_makePosts():
    global driver
    driver = webdriver.Chrome()
    yield
    driver.close()
    driver.quit()
    print(
        "A set of Postings & DirectAnswers -One for every wbs-level- was hopefully completed successfully.")

def test_makePosts(prep_makePosts):

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
    ## project1 login performed -> redirects to overview.php
    # now click a thread (identified by linkt-text) to open the threadview.php (in overview.php):
    time.sleep(1)
    ovSelectThread = OverviewCls.Overview(driver)
    # start iteration through all 7 levels -------------------------------------------------------

    linktext1 = "Automated Testing-Show-related discussion"
    n = 0
    while n < 7:
        n += 1
        if n == 1:
            linktext1 = "Automated Testing-Show-related discussion"
            subject1 = "This is the Level1 Posting-Test"
            subject2 = "A direct-answer-test for the Level1 Posting-Test"
        if n == 2:
            linktext1 = "Test Layout & Design-related discussion"
            subject1 = "This is the Level2 Posting-Test"
            subject2 = "A direct-answer-test for the Level2 Posting-Test"
        if n == 3:
            linktext1 = "Page Object Model-related discussion"
            subject1 = "This is the Level3 Posting-Test"
            subject2 = "A direct-answer-test for the Level3 Posting-Test"
        if n == 4:
            linktext1 = "Test Management-related discussion"
            subject1 = "This is the Level4 Posting-Test"
            subject2 = "A direct-answer-test for the Level4 Posting-Test"
        if n == 5:
            linktext1 = "Continuous Integration of QA-related discussion"
            subject1 = "This is the Level5 Posting-Test"
            subject2 = "A direct-answer-test for the Level5 Posting-Test"
        if n == 6:
            linktext1 = "CI Tools Selection Concepts-related discussion"
            subject1 = "This is the Level6 Posting-Test"
            subject2 = "A direct-answer-test for the Level6 Posting-Test"
        if n == 7:
            linktext1 = "CI tools portfolio & workflow-related discussion"
            subject1 = "This is the Level7 Posting-Test"
            subject2 = "A direct-answer-test for the Level7 Posting-Test"
        # incremental sizing-up the scrolling down of the page - with every iteration:
        # start at: window.scrollTo(0,250)
        # with an increase of 130:
        scroll = 250 + 130 * n
        driver.execute_script("window.scrollTo(0, scroll)")
        time.sleep(2)

        # from C-BOARD select iteration-related thread by linktest _> opens threadview.php:
        ovSelectThread.click_thread_by_linktext(linktext1)
        time.sleep(1)
        assert "C-BOARD: CFLX enhanced communication -> advanced collaboration" in driver.title

        # # START posting-operations in threadview.php
        post = ThreadviewCls.Threadview(driver)

        # USE CFLX:
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

        # post.select_cflx & click use&select btn
        CFLX_hover("Status Statement")
        post.click_cflx_by_id("ss1")
        post.click_cflx_submit_btn("usessbtn")
        time.sleep(2)

        CFLX_hover("I-Message")
        post.click_cflx_by_id("im1")
        post.click_cflx_submit_btn("useimbtn")
        time.sleep(2)

        CFLX_hover("Appeal")
        post.click_cflx_by_id("ap1")
        post.click_cflx_submit_btn("useapbtn")
        time.sleep(2)
        # perform a mouse-move to release the dropdown:
        mouse_move(-200, -33) # !it seems, that here a context or right-click is performed somehow...
        # enter subject of first posting:
        post.insert_post_subject(subject1)
        time.sleep(1)
        # try get rid of the now open right-click-menu:
        # try ESC button click:
        post.click_esc()
        # post.clicktab()

        # integrated mce-icon-test: bold icon im mce (& then sendkeys 'posting-string' to actual position):
        actions = ActionChains(driver)

        post.click_mce_bold()
        actions.send_keys('Hello - posting-content is repetitive for all levels - '+ subject1 +'! \n')
        post.click_mce_bold()#unbold

        actions.send_keys("""Team-working in a team without face-to-face communication is different - so we decided to take advantage of this world-innovative CFLX-solution (the 'Clarity-Flags' from the dropdown-menu"). There is an initial set of CFLX-Statements available to quick-start & getting acquainted to this concept of clear, candor communication, but you can (and should) modify & use your own added statements to meet your personal style and preferences of communication. Using the CFLX is mandatory: You cannot make a posting without making the 'Clarity-Statements'.  
...We made the amazing observation, that the user's spoken communication tends to adapt to this principle of making clear statements. """)

        actions.send_keys("""
No more reading between the lines
clear, logged statements of good questions and helping answers...
... will lead in better results, higher performance, and a candor spirit of 'WE' despite the existing regional and cultural distances!
        
        """)


        actions.send_keys("""
One note to the attachments:
You can add attachments -like a standardized Task-Risk-Assessment or a standardized Task-Test-2do or Task-DoR and DoD- and these will be assigned to the WBS-ID automatically then.
There is a build-in version-control via adding a time-stamp automatically: if you change the file & re-add it, always the latest version will be shown in the C-DATA then - but older versions will remain on the database, can be reactivated by selecting it, modify if neccessary, and upload it again without changing the name of the file.
(within the postings, the version of the attachment will always remain in the version the user posted it, of course...)""")
       # post.click_mce_bold() # un-bold
        actions.perform()

        time.sleep(3)
        post.click_absenden_btn()
        # => ini-post is created, direct-Answer link (& button) available,
        # -> we click link by link name (button would be by a changing thread-id) => redirects to directAns.php:
        # post.click_directAns_link(subject1) # linktext == the subject of the posting
        post.click_dirAns_byxpathlinktext(subject1)
        time.sleep(2)
        assert "C-BOARD: direct Answer" in driver.title
        # ---------------------------------------------------------------------------------
        # start with a click on the h2 head element:
        post.clicktab()
        # driver.find_element_by_id("diransheader").click()
#       # post.click_elementById("diransheader")
        # perform a mouse move and click:
        #mouse_move(-200, -33)
        # mnove to bottom of page - to get in reach of elements:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
       # post.click_elementcontains("C-BOARD :: D I R E C T - A N S W E R S")
        # now proceed with the CFLX - QR instead of SS:
        CFLX_hover("Question Repeat")
        post.click_cflx_by_id("qr1")
        post.click_cflx_by_id("useqrbtn")
      #  post.click_cflx_submit_btn("useqrbtn")
        time.sleep(2)

        CFLX_hover("I-Message")
        post.click_cflx_by_id("im1")
        post.click_cflx_submit_btn("useimbtn")
        time.sleep(2)

        CFLX_hover("Appeal")
        post.click_cflx_by_id("ap1")
        post.click_cflx_submit_btn("useapbtn")
        time.sleep(2)
        # perform a mouse-move to release the dropdown:
        mouse_move(-200, -33)
       # post.insert_post_subject(subject1)
        time.sleep(1)

        # create a direct-answer Posting:
        post.click_mce_bold() # make it bold
        actions2 = ActionChains(driver)
        actions2.send_keys(subject2 + '! \n')
     #   actions2.perform()

        post.click_mce_bold()  # un-bold
        actions2.send_keys("""giving direct-answers is an additional option to create sub-threads within the threads: all answers to the direct-answer can be viewed within an extra thread. The CFLX-functionality is available in the direct answers as well.
Better understanding for man AND machine is the result.
The communication-data collected from your digital-workplace-solution - combined with the data of your ERP-system is the biggest source of data-creation available.
        
If data is the new oil, then storing and further processing of this data is of crucial importance and will be the basis of:
     + ai-backed project-forecasting & suggestions for optimizations long before problems do occur,
    + ai-backed assignment of tasks and roles with the globally available human resources,
    + ai-provided suggestions of solutions found in prior projects containing tasks with a comparable problem and context.

As a result, our most precious resource, the human resource, can be utilized within the optimal level of its means:
    + Not too high - and not too low, on an individual scope,
    + Always supplying the worker with tasks containing a well balanced mix of learning and production.
        
Based on the continuous monitoring of communication (CCS) & the stage of completion of the deliverables (ERP),
the ai is capable to evaluate and in making suggestions and hints for 
    + Enabling a steady improvement of the workers skills,
    + Improving the productivity in general.
              
A high quality source of data and a global network of knowledge-workers will be the biggest source of competitive advantage. That is what the CCS was made for: Helping you to develop a CYbernetic COllaboration NETwork by delivering well-structured, context-enriched data.
        
       
Another argument for using a monitoring, digital workspace solution for project collaboration:""")
      #  actions2.perform()

        post.click_mce_bold()#bold
        actions2.send_keys("""
==> What do you think: is the written form of communication more reliable than the spoken one?""")
        post.click_mce_bold() #un-bold

        actions2.perform()

        time.sleep(3)
        post.click_absenden_btn()
        # => direct-answer-post is created,
        # -> we need now return to the c-board and enter the next initial-posting and direct answer:
        # scroll up & click c-board button:
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollTo(0, 50)")
        time.sleep(2)
        post.click_cBoardBtn()
        time.sleep(2)
        assert "C-BOARD: enhanced communication -> advanced collaboration" in driver.title

    # after iteration is done, scroll down the page in steps (in overview.php):
    driver.execute_script("window.scrollTo(0, 50)")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 300)")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 600)")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 900)")
    time.sleep(6)
    # scroll up & logout:
    driver.execute_script("window.scrollTo(0, 50)")
    ovSelectThread.click_logoutBtn()
    time.sleep(4)
    assert "C.C.S. :: Entry" in driver.title
