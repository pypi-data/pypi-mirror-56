# from the class Register - modify accordingly (project1/login/register.php)
class ProjectRegister():

    def __init__(self, driver):


        self.driver = driver

        self.enter_btn_id = "btnBlue"
        self.sheets_icon_class = '//a[@class="sheetstext"]'


    def click_regbtn(self):
        self.driver.find_element_by_id(self.enter_btn_id).click()

    def click_icon(self):
        self.driver.find_element_by_id(self.sheets_icon_class).click()