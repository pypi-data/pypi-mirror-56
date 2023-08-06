class Overview():

    def __init__(self, driver):

        self.driver = driver
        # all buttons admin-user-view:
        self.useradmin_btn = "a.myButtonRed"
        self.wbsadmin_btn = "a.myButton"
        self.cWeek_btn = "a.myButtonPink"
        self.tView_btn = "a.myButtonAzure"
        self.mySight_btn = "a.myButtonOrange"
        self.myProfile_btn = "a.myButtonYelow"
        self.cMail_btn = "a.myButtonBlu"
        self.cData_btn = "a.myButtonGrey"
        self.logout_btn = "a.outButton"

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

    def click_cMailBtn(self):
        self.driver.find_element_by_css_selector(self.cMail_btn).click()

    def click_cDataBtn(self):
        self.driver.find_element_by_css_selector(self.cData_btn).click()

    def click_logoutBtn(self):
        self.driver.find_element_by_css_selector(self.logout_btn).click()

    #nxt: defined functions for the clicking the created thread-links & clicking the [+new] btns

    # # # start: WBS-Elemet1 (=darkblue-project-level)
    #  <a href = "threadview.php?ID=1"
    #  style = "color: #5959FF; text-decoration: none;" >Automated Testing-Show - related discussion</a>
    # # ==> select "by_link_text" oder "xPath":
    # # xPath: / html / body / span / div / div / table[2] / tbody / tr / td / div / div[1] / a

    # generalized thread-selector via link-text:
    def click_thread_by_linktext(self, threadTxt):
        self.driver.find_element_by_link_text(threadTxt).click()

    def click_elem_by_tagetUrl(self, linkurl):
        self.driver.find_element_by_xpath('//a[@href="'+linkurl+'"]').click()