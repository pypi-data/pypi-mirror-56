import time
from selenium import webdriver


class GetHtml:
    """Class that receives login, password and path to ChromeDriver.exe as parameters and has a method that do the search in MAM
    and returns the HTML resulting of the search
    """
    password: str

    def __init__(self, login, passw, driverPath):
        self.driver = webdriver.Chrome(driverPath)  # Optional argument, if not specified will search path.
        self.login = login
        self.password=passw
        # Login
        self.driver.get('https://www.myanonamouse.net/login.php');
        time.sleep(1)  # Let the user actually see something!
        search_box = self.driver.find_element_by_name('email')
        search_box.send_keys(self.login)
        search_box2 = self.driver.find_element_by_name('password')
        search_box2.send_keys(self.password)
        search_box2.submit( )

    def search(self, keyword):
        search_box3 = self.driver.find_element_by_name('tor[text]')
        search_box3.send_keys(keyword)
        search_box3.submit()
        time.sleep(2)
        html = self.driver.page_source
        return html

    def stop(self):
        self.driver.quit( )