
class Index():

    def __init__(self, driver):

    # actual settings/ identifyiers of the selectors

        self.driver = driver
        self.projectNr_edit_id = "projectNr"
        self.name_edit_id = "name"
        self.password_edit_id = "pass"
        self.enter_btn_id = "btnBlue"

        self.info_icon_class = '//a[@class="infotext"]'
        self.pencil_icon_class = '//a[@class="pencilext"]'

        self.info_link_id = "infolink"
        self.pencil_link_id ="pencillink"

    def enter_projectNr(self, projectNumber):
        self.driver.find_element_by_id(self.projectNr_edit_id).clear()
        self.driver.find_element_by_id(self.projectNr_edit_id).send_keys(projectNumber)


    def enter_name(self, name):
        self.driver.find_element_by_id(self.name_edit_id).clear()
        self.driver.find_element_by_id(self.name_edit_id).send_keys(name)


    def enter_password(self, passw):
        self.driver.find_element_by_id(self.password_edit_id).clear()
        self.driver.find_element_by_id(self.password_edit_id).send_keys(passw)


    def click_ENTERbtn(self):
        self.driver.find_element_by_id(self.enter_btn_id).click()


    def click_pencilIcon(self):
        self.driver.find_element_by_xpath(self.pencil_icon_class).click()


    def click_infoIcon(self):
        self.driver.find_element_by_xpath(self.info_icon_class).click()

    def click_pencilLink(self):
        self.driver.find_element_by_id(self.pencil_link_id).click()

    def click_infolLink(self):
        self.driver.find_element_by_id(self.info_link_id).click()

    #  assert "C.C.S. :: Entry" in driver.title
