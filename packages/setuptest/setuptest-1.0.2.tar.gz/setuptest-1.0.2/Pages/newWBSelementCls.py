# the newWBSelementCls has two views: one initial with only a form with create new project btn
# and if project is created a WBS-creator layout with dropdown elements
#from selenium import webdriver
#driver = webdriver.Chrome()
#from selenium.webdriver.common.action_chains import ActionChains
#action = ActionChains(driver)
class newWBSelement():

    def __init__(self, driver):


        self.driver = driver

        self.projectname_edit_id = "pname"
        self.projectdescr_edit_id = "pdescr"
        self.projectnumber_edit_id = "pnumber"
        self.create_btn_id = "wbs_btn"
        self.info_span = "span.drag-hint"  ##tag.css-class
        self.cboard_btn = "a.myButtonBlu"
        self.wbsnumber_edit_id ="WBSid"
        self.wbsname_edit_id ="topic"
        self.wbsdescr_edit_id ="descr"

        self.wbsLevel_li_class ="li.wbsL1"



## initial: create the project:
    def enter_projectname(self, projectname):
        self.driver.find_element_by_id(self.projectname_edit_id).clear()
        self.driver.find_element_by_id(self.projectname_edit_id).send_keys(projectname)

    def enter_projectdescr(self, description):
        self.driver.find_element_by_id(self.projectdescr_edit_id).clear()
        self.driver.find_element_by_id(self.projectdescr_edit_id).send_keys(description)

    def enter_projectnr(self, projectnr):
        self.driver.find_element_by_id(self.projectnumber_edit_id).clear()
        self.driver.find_element_by_id(self.projectnumber_edit_id).send_keys(projectnr)
## create project end

## now: Create WBS elements start:
    ## colored-wbs-level-bars (a) click on bar b) click on a href with element-name-naming
    def click_parentWbsBar(self, wbsLevel, linktext):
        self.driver.find_element_by_class_name(wbsLevel).click()
        self.driver.find_element_by_link_text(linktext).click()

##test-try-semi-hc mit find_element_by_css_selector
    def click_parentWbsBar1(self, linktext):
        self.driver.find_element_by_css_selector(self.wbsLevel_li_class).click()
        self.driver.find_element_by_link_text(linktext).click()

   # self.driver.find_element_by_class_name("wbsL2").click()
   # self.driver.find_element_by_link_text("1.1 selenium 'd be the next big project here").click()
    ## form edit fields:
    def enter_wbsnr(self, wbsnr):
        self.driver.find_element_by_id(self.wbsnumber_edit_id).clear()
        self.driver.find_element_by_id(self.wbsnumber_edit_id).send_keys(wbsnr)

    def enter_wbsname(self, wbsname):
        self.driver.find_element_by_id(self.wbsname_edit_id).clear()
        self.driver.find_element_by_id(self.wbsname_edit_id).send_keys(wbsname)

    def enter_wbsdescr(self, wbsdescr):
        self.driver.find_element_by_id(self.wbsdescr_edit_id).clear()
        self.driver.find_element_by_id(self.wbsdescr_edit_id).send_keys(wbsdescr)
## new wbs-elements end
    def click_createBtn(self):
        self.driver.find_element_by_id(self.create_btn_id).click()

    def click_cboardBtn(self):
        self.driver.find_element_by_css_selector(self.cboard_btn).click()

    def click_InfoSpan(self):
        self.driver.find_element_by_css_selector(self.info_span).click()

# info: muss vermutl. noch angepasst werden - dies ist der info-span fuer den wbs-creator-teil (im eigentl. WBS-creator)
  #  def mouseover_infoSpan(self):
   #     self.driver.find_element_by_css_selector(self.info_span).click()
   #     showUpElem = self.driver.find_element_by_css_selector(self.info_span)
    #    action.move_to_element(showUpElem).perform()


##   self.info_span = "span.drag-hint" ##tag.css-class
##   self.driver.find_element_by_css_selector(self.info_span).click()

## showUpElem = driver.find_element_by_css_selector(self.info_span)
#	action.move_to_element(showUpElem).perform()