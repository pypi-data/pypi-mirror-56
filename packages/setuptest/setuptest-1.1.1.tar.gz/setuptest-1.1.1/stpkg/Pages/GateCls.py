
class Gate():

    def __init__(self, driver):

    # actual settings/ identifyiers of the selectors

        self.driver = driver
        self.projectNr_edit_id = "projectNr"
        self.enter_btn_id = "btnBlue"

        self.info_icon_class = '//a[@class="infotext"]'
        self.pencil_icon_class = '//a[@class="pencilext"]'


    def enter_projectNr(self, projectNumber):
        self.driver.find_element_by_id(self.projectNr_edit_id).clear()
        self.driver.find_element_by_id(self.projectNr_edit_id).send_keys(projectNumber)


    def click_ENTERbtn(self):
        self.driver.find_element_by_id(self.enter_btn_id).click()


    def click_pencilIcon(self):
        self.driver.find_element_by_xpath(self.pencil_icon_class).click()


    def click_infoIcon(self):
        self.driver.find_element_by_xpath(self.info_icon_class).click()

    # gate.php asserts with:
    # assert "C-BOARD :: Entry" in driver.title
