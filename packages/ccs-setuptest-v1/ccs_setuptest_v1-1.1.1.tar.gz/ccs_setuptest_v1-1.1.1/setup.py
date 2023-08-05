from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ccs_setuptest_v1',
    version='1.1.1',
    url='https://c-c-s.sourceforge.io/',
    author='Florian Strahberger',
    author_email='flori@ctemplar.com',
    description='The Selenium based setuptest for the CYBR CSCW-SUITE (CCS). 1.download: wget sourceforge.net/projects/c-c-s/files/latest/download  2.install-app: docker-compose up --build  3.get-test: pip3 install ccs-setuptest-v1 --user 4.setup-and-test(execute locally - install on server by typing in your command-line): ccs-setuptest.py',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="CYBR CSCW-SUITE,CCS,digital workplace,project management,digitalization,communication,collaboration,groupware, setup.install,test,selenium,pytest,chromedriver,setuptest",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(),
    install_requires=['atomicwrites==1.3.0', 'attrs==19.3.0', 'importlib-metadata==0.23', 'more-itertools==7.2.0', 'packaging==19.2', 'pluggy==0.13.0', 'py==1.8.0', 'pyparsing==2.4.2', 'pytest==5.2.2', 'selenium==3.141.0', 'six==1.12.0', 'urllib3==1.25.6', 'wcwidth==0.1.7', 'zipp==0.6.0'],
    entry_points={'console_scripts':[
        'setuptest.py=Start.ccssetuptest:starterclass.startclass',
        'ccs-setuptest.py=Start.ccssetuptest:starterclass.startclass']}
)
