class Threadview():

    def __init__(self, driver):

        self.driver = driver
        # all buttons admin-user-view:
        self.useradmin_btn = "a.myButtonRed"
        self.wbsadmin_btn = "a.myButton"
        self.cWeek_btn = "a.myButtonPink"
        self.tView_btn = "a.myButtonAzure"
        self.mySight_btn = "a.myButtonOrange"
        self.myProfile_btn = "a.myButtonYelow"
        self.cBoard_btn = "a.myButtonBlu"
        self.cData_btn = "a.myButtonGrey"
        self.logout_btn = "a.outButton"

        self.subject_id = "topic"
        self.textarea_id = "mssgbox"
        self.absenden_btn_id = "absenden"
        # example for direct answer link:
        self.dirAnslink_xpath = "//a[contains(.,'Automated Testing-Show-related discussion']"


    # click all buttons admin-user-view:
    def click_usradminBtn(self):
        self.driver.find_element_by_css_selector(self.useradmin_btn).click()

    def click_wbsadminBtn(self):
        self.driver.find_element_by_css_selector(self.wbsadmin_btn).click()

    def click_cWeekBtn(self):
        self.driver.find_element_by_css_selector(self.cWeek_btn).click()

    def click_tViewBtn(self):
        self.driver.find_element_by_css_selector(self.tView_btn).click()

    def click_mySightBtn(self):
        self.driver.find_element_by_css_selector(self.mySight_btn).click()

    def click_myProfileBtn(self):
        self.driver.find_element_by_css_selector(self.myProfile_btn).click()

    def click_cBoardBtn(self):
        self.driver.find_element_by_css_selector(self.cBoard_btn).click()

    def click_cDataBtn(self):
        self.driver.find_element_by_css_selector(self.cData_btn).click()

    def click_logoutBtn(self):
        self.driver.find_element_by_css_selector(self.logout_btn).click()

    # generalized cflx-selector via id-parameter:
    def click_cflx_by_id(self, cflxId):
        self.driver.find_element_by_id(cflxId).click()

    def click_cflx_submit_btn(self, cflxBtnId):
        self.driver.find_element_by_id(cflxBtnId).click()
        # btn: id="usessbtn" /qr /im /ap
    def insert_post_subject(self, subjectTxt):
        self.driver.find_element_by_id(self.subject_id).clear()
        self.driver.find_element_by_id(self.subject_id).send_keys(subjectTxt)

# 	<textarea id='mssgbox' name="mssgbox" class="mssgtxtarea" rows="10" cols="166"></textarea>
    # textarea_id = "mssgbox"
    def insert_post_factualMsg(self, factualMssg):
        self.driver.find_element_by_id(self.textarea_id).clear()
        self.driver.find_element_by_id(self.textarea_id).send_keys(factualMssg)

    def click_absenden_btn(self):
        self.driver.find_element_by_id(self.absenden_btn_id).click()

    # start direct Answer section (directAns.php page is using same class as threadview.php page):
    # generalized via id-Parameter: dirAnsId (eg: newDirAns6, nxtDirAns7, via topic-link: TDirAns6)
    def click_directAns_btn(self, dirAnsId):
        self.driver.find_element_by_id(dirAnsId).click()
    def click_directAns_link(self, linkTxt):
        self.driver.find_element_by_link_text(linkTxt).click()

    def click_dirAns_byxpathlinktext(self,ahreflinktext):
       # self.driver.find_element_by_xpath("//a[contains(.,'"+ahreflinktext+"')]").click()
       # self.driver.find_element_by_xpath("//a[text()='**"+ahreflinktext+"**']").click()
       # self.driver.find_element_by_xpath("//a[text(.,'**"+ahreflinktext+"**')]").click()
        self.driver.find_element_by_xpath("//a[contains(.,'"+ahreflinktext+"')]").click()

    # individual cflx-message via textarea:
    def insert_CFLX_textarea(self, txtBoxId, cflxMessage):
        self.driver.find_element_by_id(txtBoxId).clear()
        self.driver.find_element_by_id(txtBoxId).send_keys(cflxMessage)
        # eg: post.insert_CFLX_textarea("QRTextBox", "You were asking, what we think about using this digital workplace tool")

    # generalized posting-selector via div-id-parameter <div id="4">:
    def click_posting_by_id(self, postingDivId):
        self.driver.find_element_by_id(postingDivId).click()
     # click h2 element by contains in element text:
    def click_elementcontains(self, h2txt):
        self.driver.find_element_by_xpath("//a[contains(.,'"+h2txt+"')]").click()
    def click_elementById(self, elemid):
        self.driver.find_element_by_id(elemid).click()
    def clicktab(self):
        from selenium.webdriver.common.keys import Keys
        self.driver.find_element_by_tag_name('body').send_keys(Keys.TAB)
        #self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')

    def click_esc(self):
        from selenium.webdriver.common.keys import Keys
        self.driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
    # post factual information:
# v1:
# <textarea id="mssgbox" name="mssgbox" class="mssgtxtarea" rows="10" cols="133" aria-hidden="true" style="display: none;"></textarea>

# ---
# das tinyMCE element via chrome kopiert (um einiges css verkuertzt) wie folgt:
# <html><head>
# <style id="mceDefaultStyles" type="text/css">.mce-content-body div.mce-resizehandle {position: absolute;border: 1px solid black;box-sizing: box-sizing;background: #FFF;width: (... css zeugs)
# .mce-content-body .mce-offscreen-selection {position: absolute;left: -9999999999px;}.mce-content-body *[contentEditable=false] {cursor: default;}.mce-content-body *[contentEditable=true] {cursor: text;}
# </style>
#
# <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
# <link type="text/css" rel="stylesheet" href="https://localhost/project1/tinymce/skins/lightgray/content.min.css"></head>

# <body id="tinymce" class="mce-content-body " data-id="mssgbox" contenteditable="true" spellcheck="false">
# <p><br data-mce-bogus="1"></p></body></html>

## evtl wie am bsp wie folgt:
# https://seleniummaster.com/sitecontent/index.php/selenium-web-driver-menu/selenium-test-automation-with-python/333-selenium-python-webdriver-tinymce-text-input

    #define MCE Frame

    def insert_post_factualMsg2(self, factualMssg):
        mce_frame = self.driver.find_element_by_id('mce_0_ifr')
        #Switch to the mce frame
        self.driver.switch_to_frame(mce_frame)
        #define mce body
        mce_edit = self.driver.find_element_by_xpath("//body[@id='tinymce']")
        self.time.sleep(5)
        #clear mce body
        mce_edit.clear()
        self.time.sleep(5)
        mce_edit.send_keys(factualMssg)

# versuch mit xPath ueber click auf [B] (bold) -> cursor in der textarea:
#//*[@id="mceu_3"]/button/i

    def click_mce_bold(self):
        self.driver.find_element_by_xpath("//*[@id='mceu_3']/button/i").click()
       # active_ele = self.driver.switch_to.active_element
       # active_ele.send_keys("bla bla message")
    def click_mce_bullets(self):
        self.driver.find_element_by_xpath("//*[@id='mceu_9']/button/i").click()


