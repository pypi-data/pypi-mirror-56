class OnlineAssessment():

    def __init__(self, driver):

        self.driver = driver
        # all buttons admin-user-view:
        self.cMail_btn = "a.myButtonBlu"
        self.run_btn_xPath = "// *[ @ id = 'testbutton']"
        self.nearness_span_xPath = "//*[@id='nearnessaxis']"
        self.risk_span_xPath = "//*[@id='riskaxis']"
        self.btn_id_1 = "f1n3"

    # die radio-btns im einzelnen f1 bis f24 -> id= f1n1 bis f24n6 :
    # # <input  type = "radio" name = "f1" value = "2" id = "f1n2" >
    # # xpath, zB: //*[@id="f2n5"]


    # generalized radio-btn select:
    def select_radio_btn(self, btn_id):
        self.driver.find_element_by_id(btn_id).click()
    # usage example for non-programming testers:
    # selftest.select_radio_btn("f1n3")
    # selftest.select_radio_btn("f2n5")
    # selftest.select_radio_btn("f3n5")
    # selftest.select_radio_btn("f4n5")
    # selftest.select_radio_btn("f5n2")
    # selftest.select_radio_btn("f6n5")
    # ...

    # usage with some programming-skills, sth like:
    # ValUse = array([1,5,5,5,2,5,5,5,3,2,6,5,3,4,2,5,2,4,5,3,4,6,6,6])
    # for [f_1 bis f_24]:
    # for (i=1; i <= 24; i++) select_radio_btn("f"i"n"ValUse[i-1]")


    # click run test button
    def click_RunTest_Btn(self):
        self.driver.find_element_by_xpath(self.run_btn_xPath).click()


    # get values of the test-result:
# # nearness:
# <span id="nearnessaxis" style="color: rgb(8, 8, 152); font-weight: 700; border-style: solid; border-width: 3px; padding:5px;">-0.50</span>
# //*[@id="nearnessaxis"]


# # risk:
# <span id="riskaxis" style="color: rgb(179, 8, 8); font-weight: 700; border-style: solid; border-width: 3px; padding:5px;">2.33</span>
# //*[@id="riskaxis"]

# example to get .text of <span>:
# for elem in browser.find_elements_by_xpath('.//span[@class = "gbts"]'):
#    print elem.text
# analog:
    def get_nearness_value(self):
       # global nearnessValue
        nearnessValue = self.driver.find_element_by_xpath(self.nearness_span_xPath).text
      #  print(nearnessValue)
        return nearnessValue

    def get_risk_value(self):
      #  global riskValue
        riskValue = self.driver.find_element_by_xpath(self.risk_span_xPath).text
       # print(riskValue)
        return riskValue
