#  The python-based setuptest for the CYBR CSCW-SUITE (CCS) Version 0.9.6
 (will use selenium & pytest. will require to be installed: python3 & ChromeDriver. Get ChromeDriver from: https://chromedriver.chromium.org/)

## prepare, install & usage:

## A) The short cli description (works for Linux-users - adapt accordingly if you are on Windows or Mac - or check the B) long version below)
 

* Be aware: you need to make the mandatory needed changes within the Conf/test_configVars.py file **before you make the installation!**

**a) download & unzip the setuptest.zip from sourceforge:**

    wget https://sourceforge.net/projects/c-c-s/files/setuptest.zip/download

 **unzp into the ccstest/ created directory:**

	python3 -m zipfile -e download ccstest

**b) modify the configuration-file "Conf/test_configVars.py":**

 *open the Conf/test_configVars.py file & make the needed modifications: (at least: set the correct IP)*

	nano ccstest/setuptest/Conf/test_configVars.py
**c) save & overwrite the test_configVars.py**  


**d) install the ccs-setuptest:**

	python3 setup.py install --user

**e) run the setup, install & test automation for the installed CYBR CSCW-SUITE (CCS) by typing:**

	setuptest.py

**f) execute the ccs-setuptest, check values & click the [INSTALL] btn**

=> Enjoy the test & setup-automation.
-----------------------------------------------

## B) the longer version:

### 1. prepare the setup (download, unzip, modify the Conf/test_configVars.py)

	https://sourceforge.net/projects/c-c-s/files/setuptest.zip/download

1. download, unzip & cd into the setuptest/

2. open the Conf/test_configVars.py with your text-editor (editor,nano,gedit,touch, whatever ...)

3. modify / exchange the dummy-values with those fitting to your own situation
(eg: enter the IP of your server where you have the CCS running, exchange the SendGrid API-Key, the email & its public PGP-Key)

save / override the yet modified test_configVars.py file

### 2. install
* you need the setuptools installed on your machine. Check / install via pip3:

	pip3 install setuptools --user

**If you are new to python & the usage of setuptools:**
if there is a setup.py within a python package, you simply can install it (based on the installed setuptools) with:

	python3 setup.py install --user

### 3. run the setup, install & test automation for the installed CYBR CSCW-SUITE (CCS) by typing:

	setuptest.py

### 4. execute the ccs-setuptest, check values & click the [INSTALL] btn**

=> Enjoy the test & setup-automation.
------------------------------------------------------------------------------------------------------------

## The setuptest will:
  * Open the Conf/test_configVars.py file, so you can modify the values (The IP of your CCS, the SendGrid API-Key, E-Mail-Address & publicPGP-Key ..)
  * Call the installation-script for creating the database-tables of your CCS
  * Make the automated setup for your first 5 projects
  * Will create a testing-project and simulate an admin who is creating a project, a WBS, creates a user-profile, testst the user's CFLX, starts to make a posting.

--------------------------------------------------------------------------------------------------------------

## If not done already: install the CCS on your server:
**Requirements: Linux & docker / docker-compose installed**

* from the terminal of your Linux-server / VPS (if you need one, then get one via: https://www.mvps.net/?aff=6517 - and support my server-costs)

    wget sourceforge.net/projects/c-c-s/files/latest/download


    docker-compose up --build

## Installation & Execution of this ccs-setuptest
Requires ChromeDriver & Chrome Web-Browser to be installed - ensure to have the correct versions which fit to each other!
Installation is easy - check the docs / tutorials for your local Operation System (Windows / Mac / Linux), then proceed and:


## Detailed usage of the ccs-setuptest

<1st page>
* The yellow [CONTINUE] button
will open the page displaying the actual setup-install values.

<2nd page>
* The yellow [SETUP] button will open the Conf/test_configVars.py file, so you can modify the values (The IP of your CCS, the SendGrid API-Key, E-Mail-Address & publicPGP-Key ..)

**make the changes, save & re-run with:**

    setuptest.py

<2nd page>
* The red [INSTALL] button (bottom of 2nd page) will perform the installation with the values
 & perform a fully automated show-up-test showing and explaining you the basic functionalities
 for setting-up the projects as well as how to use the application.

**NOTE: this will use the first slot of your CCS and populate it with an example project!**

This means, your per default available projects for your productive work will be reduced to 4,
unless you decide to fully delete the database-tables of projectdb1 database - and rebuild the tables by calling:
https://[IP or domain]/1/zubringer/create8Tables.php

### manually start & select the setup, installation & testing-scripts
At first, you need to make the settings by modifying the Conf/test_configVars.py file with the text-editor of your choice (nano, gedit, touch, editor) - then you can call the scripts via pytest


#### You can call the scripts manually - and only the selected one or ones from your terminal / console/ bash/ shell/ as well:

  *  for running all tests within the directory: pytest foldername/

eg for running all setups or running all tests:


    pytest RunSetups/
or:

    pytest Tests/


  *  for running a single test, cd to the test and type: pytest filename.py (see details below)

#### Setup-Scripts available:
**`cd RunSetups/`**

	pytest test_ini_1_createTables.py

	pytest test_ini_2_registerSuperadmin.py

	pytest test_ini_3_1stProjectSetup.py

	pytest test_ini_4_4ProjectsSetup.py

#### Walk-Through tests available (still in beta: will work, but might throw errors. Its a test-script issue then - not an application one!):
**`cd Tests/`**

	pytest test_loginCreateProjectCreateWBS.py

	pytest test_loginMakePosts.py 

	pytest test_loginPersProfileComplete.py
 

## if you need to make changes to the Conf/test_configVars.py afterwards

**YOU CANNOT SIMPLY CHANGE THE VALUES FROM WITHIN THE DOWNLOAD-FOLDER**
... the installation is moving the files which are executed to an other, Operation-System-dependend place.
After the installation, a change of the file - like performed via:

	nano ccstest/setuptest/Conf/test_configVars.py 

will have no effect.

### but you can simply uninstall, delete all the unzipped setuptest folders & start from a new unzip:

1. uninstall:

	pip3 uninstall ccs-setuptest-v1

2. remove all of the unzipped folders

3. unzip the downloaded setuptest.zip folder, and now you can make the changes of the Conf/test_configVars.py file

4. store the modified file

5. install the setuptest again via:

    	python3 setup.py install --user

6. execute via:

    setuptest.py

7. click [CONTINUE], check the -yet hopefully modified- values, scroll down & click [INSTALL]

enjoy the automation.



