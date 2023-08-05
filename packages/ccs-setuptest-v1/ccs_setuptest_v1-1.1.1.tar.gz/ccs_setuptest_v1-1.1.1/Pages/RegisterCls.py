
# die class LoginPage mit den "user defined functions" = def fuer die Einzelnen Interaktionen der verfuegbaren Elemente
class Register():

    def __init__(self, driver):


        self.driver = driver

        self.username_edit_id = "name"
        self.email_edit_id = "email"
        self.pw_edit_id = "pass"
        self.pubkey_edit_id = "pgpKey"
        self.enter_btn_id = "btnBlue"
        self.checkbox_id = "agree"
        self.eula_link = "eulalink"


    def enter_username(self, username):
        self.driver.find_element_by_id(self.username_edit_id).clear()
        self.driver.find_element_by_id(self.username_edit_id).send_keys(username)

    def enter_email(self, email):
        self.driver.find_element_by_id(self.email_edit_id).clear()
        self.driver.find_element_by_id(self.email_edit_id).send_keys(email)

    def enter_pubkey(self, pubkey):
        self.driver.find_element_by_id(self.pubkey_edit_id).clear()
        self.driver.find_element_by_id(self.pubkey_edit_id).send_keys(pubkey)

    def enter_pw(self, password):
        self.driver.find_element_by_id(self.pw_edit_id).clear()
        self.driver.find_element_by_id(self.pw_edit_id).send_keys(password)

    def click_regbtn(self):
        self.driver.find_element_by_id(self.enter_btn_id).click()

    def click_eulaCheckBox(self):
        self.driver.find_element_by_id(self.checkbox_id).click()

    def click_EulaLink(self):
        self.driver.find_element_by_id(self.eula_link).click()

