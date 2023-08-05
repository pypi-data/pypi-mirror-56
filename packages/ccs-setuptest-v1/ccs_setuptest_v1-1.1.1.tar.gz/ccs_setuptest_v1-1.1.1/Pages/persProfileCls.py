class persProfile():

    def __init__(self, driver):

        self.driver = driver
        self.cBoard_btn = "a.myButtonBlu"
        self.myFirstName_edit_id = "fname"
        self.myLastName_edit_id = "lname"
        self.myPhoneNo_edit_id = "phone"
        self.myTimeZone_edit_id = "tzone"
        self.myEmailAddress_edit_id = "email"
        # TRY XPATH for [submit changes]btns:
        self.mainDataSubmit_btn = "//button[@type='submit' and @value='change main data']"
        # //*[@id="perspreferences"]/button
        self.preferencesDataSubmit_btn = "//*[@id='perspreferences']/button"
        self.miscDataSubmit_btn = "//*[@id='misc']/button"

        self.myRole_edit_id = "position"
        self.mySkills_edit_id = "skills"
        self.myNearness_edit_id = "nearness"
        self.myRisk_edit_id = "risk"
        self.myComment_edit_id = "comment"
        self.myInterests_edit_id = "interestedin"
        self.myLinklist_edit_id = "linklist"
        # cflx-section:
        self.SScflx_dropdown = "li.flagSS"
# YOUR MAIN DATA SECTION:
    def enter_myFirstName(self, myFirstName):
        self.driver.find_element_by_id(self.myFirstName_edit_id).clear()
        self.driver.find_element_by_id(self.myFirstName_edit_id).send_keys(myFirstName)

    def enter_myLastName(self, myLastName):
        self.driver.find_element_by_id(self.myLastName_edit_id).clear()
        self.driver.find_element_by_id(self.myLastName_edit_id).send_keys(myLastName)

    def enter_myPhoneNo(self, myPhoneNo):
        self.driver.find_element_by_id(self.myPhoneNo_edit_id).clear()
        self.driver.find_element_by_id(self.myPhoneNo_edit_id).send_keys(myPhoneNo)

    def enter_myTimeZone(self, myTimeZone):
        self.driver.find_element_by_id(self.myTimeZone_edit_id).clear()
        self.driver.find_element_by_id(self.myTimeZone_edit_id).send_keys(myTimeZone)

    def enter_myEmailAddress(self, myEmailAddress):
        self.driver.find_element_by_id(self.myEmailAddress_edit_id).clear()
        self.driver.find_element_by_id(self.myEmailAddress_edit_id).send_keys(myEmailAddress)

# <button type="submit" value="change main data">submit changes</button>
    def click_mainDataSubmitBtn(self):
        self.driver.find_element_by_xpath(self.mainDataSubmit_btn).click()
    # driver.find_element_by_xpath("//input[@name='buttonName' and @value='3.2']")
# YOUR PREFERENCES SECTION:

    def enter_myRole(self, myRole):
        self.driver.find_element_by_id(self.myRole_edit_id).clear()
        self.driver.find_element_by_id(self.myRole_edit_id).send_keys(myRole)

    def enter_mySkills(self, mySkills):
        self.driver.find_element_by_id(self.mySkills_edit_id).clear()
        self.driver.find_element_by_id(self.mySkills_edit_id).send_keys(mySkills)

    def enter_myNearness(self, myNearness):
        self.driver.find_element_by_id(self.myNearness_edit_id).clear()
        self.driver.find_element_by_id(self.myNearness_edit_id).send_keys(myNearness)

    def enter_myRisk(self, myRisk):
        self.driver.find_element_by_id(self.myRisk_edit_id).clear()
        self.driver.find_element_by_id(self.myRisk_edit_id).send_keys(myRisk)

    def enter_myComment(self, myComment):
        self.driver.find_element_by_id(self.myComment_edit_id).clear()
        self.driver.find_element_by_id(self.myComment_edit_id).send_keys(myComment)

    def click_preferencesDataSubmitBtn(self):
        self.driver.find_element_by_xpath(self.preferencesDataSubmit_btn).click()

# # MISCELLANEOUS

    def enter_myLinklist(self, myLinklist):
        self.driver.find_element_by_id(self.myLinklist_edit_id).clear()
        self.driver.find_element_by_id(self.myLinklist_edit_id).send_keys(myLinklist)

    def enter_myInterests(self, myInterests):
        self.driver.find_element_by_id(self.myInterests_edit_id).clear()
        self.driver.find_element_by_id(self.myInterests_edit_id).send_keys(myInterests)

    def click_miscDataSubmitBtn(self):
        self.driver.find_element_by_xpath(self.miscDataSubmit_btn).click()

    def click_areaTable(self, area):
        self.driver.find_element_by_id(area).click()
# ids: bigContainmentTable
    # contains 5 sub-tables: mainAreaTable, preferencesAreaTable, miscAreaTable, pgpAreaTable, cflxAreaTable
    def misuse_pgpTextarea(self, infotext):
        self.driver.find_element_by_id("pgpKey").clear()
        self.driver.find_element_by_id("pgpKey").send_keys(infotext)
# # CFLX STORAGE
# # for all 4 CFLX each:
# # # a) modify-add existing (1. dropdown click -> 2. make change in add new field 3. click add2db_btn);
# # # b) adding new ones (1. edit_fierld 2. click btn)
# # # c) delete them  (1. dropdown click -> 2. DELETE-IT_btn 3. dropdown click -> assert-check !exist prior selected


    def click_ss_dropdown(self):
        self.driver.find_element_by_css_selector(self.SScflx_dropdown).click()

    # generalized cflx-selector via id-parameter:
    def click_cflx_by_id(self, cflxId):
        self.driver.find_element_by_id(cflxId).click()
    # generalized cflx-selector via link-text:
    def click_cflx_by_linktext(self, cflxTxt):
        self.driver.find_element_by_link_text(cflxTxt).click()

    # insert new CFLX (ss,qr,im,ap) via edit-field:
    def insert_new_cflx(self, input_id, newCflxText):
        self.driver.find_element_by_id(input_id).clear()
        self.driver.find_element_by_id(input_id).send_keys(newCflxText)

    def click_add_to_database_btn(self, btn_id):
        self.driver.find_element_by_id(btn_id).click()
    # sssubmit, qrsubmit, ...

    def click_delete_it_btn(self, btn_id):
        self.driver.find_element_by_id(btn_id).click()
    # del_statstat_btn, del_qr_btn, ...

    def click_cBoard_btn(self):
        self.driver.find_element_by_css_selector(self.cBoard_btn).click()