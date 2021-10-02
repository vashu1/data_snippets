# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, os

class HuntingLogin(unittest.TestCase):
    def setUp(self):
        None
        
    def startDriver(self):
        #selenium_url = 'http://selenium1.tb.arbor.net:4444/wd/hub'
        #dc = webdriver.DesiredCapabilities.FIREFOX
        #self.driver = webdriver.Remote(command_executor = selenium_url,  desired_capabilities = dc)
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://bith03.vm.arbor.net"
        self.verificationErrors = []
        self.accept_next_alert = True
        return self.driver
    
    def test_hunting_login(self):
        sum = 0
        repeat = 3
        for _ in range(repeat):
            sum += self.hunting_login()
        print "AVG= " + str(int(round(sum / repeat)))
            
    def hunting_login(self):
        driver = self.startDriver()
        
        start = time.time()
        
        driver.get(self.base_url + "/")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("Quafina")
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("admin")
        driver.find_element_by_name("commit").click()
        time.sleep(20)
        driver.find_element_by_link_text("Hunting").click()

        driver.find_element_by_xpath("(//input[@type='checkbox'])[15]").click()
        driver.find_element_by_css_selector("div.block.enable > label > span").click()
        
        wait_time = 5
        time.sleep(wait_time)

        driver.find_element_by_css_selector("span.UserPanel__firstName___V3_wl").click()
        driver.find_element_by_link_text("Log Out").click()
        
        spent_time = (time.time() - start - wait_time) * 1000
        print "TIME= " + str(int(round(spent_time)))
        
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
        return spent_time


    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        None

if __name__ == "__main__":
    unittest.main()
