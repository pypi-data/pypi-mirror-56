
class ccs_projectsManagementCls():

    def __init__(self, driver):

    # actual settings/ identifyiers of the selectors

    # initial walk through (first access, no entries in db-projects-table) elements:
        self.driver = driver
        self.projectNr_edit_id = "projectnumber"
        self.projectAdmEmail_edit_id = "adminemail"
        self.projectAdmEmailPGP_txtarea_id = "pgpkey"
        self.emailprovidername_edit_id = "pname"
        self.emailproviderPass_edit_id = "ppass"
        self.emailproviderPort_edit_id = "pport"
        self.emailproviderHost_edit_id = "phost"
        self.emailproviderEnc_edit_id = "penc"

        self.setThese_btn_id = "btnGreen"
        self.gate_btn_id = "gateBtn"
        self.logOut_btn_id = "logOut"
     # update-btns (dynamic ids - index counting up:
        self.update_btn1_id ="updateBtn1"
    # ini walkthrough elements end

    # initial walk through (first access, no entries in db-projects-table) functions:
    def ini_enter_projectNr(self, projectNumber):
        self.driver.find_element_by_id(self.projectNr_edit_id).clear()
        self.driver.find_element_by_id(self.projectNr_edit_id).send_keys(projectNumber)

    def ini_enter_adminEMail(self, email):
        self.driver.find_element_by_id(self.projectAdmEmail_edit_id).clear()
        self.driver.find_element_by_id(self.projectAdmEmail_edit_id).send_keys(email)

    def ini_enter_adminEMailPGPkey(self, key):
        self.driver.find_element_by_id(self.projectAdmEmailPGP_txtarea_id).clear()
        self.driver.find_element_by_id(self.projectAdmEmailPGP_txtarea_id).send_keys(key)
    def ini_enter_providerName(self, pname):
        self.driver.find_element_by_id(self.emailprovidername_edit_id).clear()
        self.driver.find_element_by_id(self.emailprovidername_edit_id).send_keys(pname)

    def ini_enter_providerPass(self, ppass):
        self.driver.find_element_by_id(self.emailproviderPass_edit_id).clear()
        self.driver.find_element_by_id(self.emailproviderPass_edit_id).send_keys(ppass)

    def ini_enter_providerPort(self, port):
        self.driver.find_element_by_id(self.emailproviderPort_edit_id).clear()
        self.driver.find_element_by_id(self.emailproviderPort_edit_id).send_keys(port)

    def ini_enter_providerHost(self, host):
        self.driver.find_element_by_id(self.emailproviderHost_edit_id).clear()
        self.driver.find_element_by_id(self.emailproviderHost_edit_id).send_keys(host)

    def ini_enter_providerEnc(self, enc):
        self.driver.find_element_by_id(self.emailproviderEnc_edit_id).clear()
        self.driver.find_element_by_id(self.emailproviderEnc_edit_id).send_keys(enc)

    def ini_click_SetTheseValuesbtn(self):
        self.driver.find_element_by_id(self.setThese_btn_id).click()

    def ini_click_Gatebtn(self):
        self.driver.find_element_by_id(self.gate_btn_id).click()

    def ini_click_logOutbtn(self):
        self.driver.find_element_by_id(self.logOut_btn_id).click()
    # ini walkthrough elements end

    def ini_click_updateBtn1(self):
        self.driver.find_element_by_id(self.update_btn1_id).click()
    # click_updateBtnGeneral: parameter like: click_updateBtnGeneral("updateBtn1") check - maybe the self is too much here..
    def click_updateBtnGeneral(self,updateBtn_n):
        self.driver.find_element_by_id(updateBtn_n).click()