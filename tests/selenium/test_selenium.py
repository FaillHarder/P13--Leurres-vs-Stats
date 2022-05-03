from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


class SeleniumTest(StaticLiveServerTestCase):

    def setUp(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 10)

        self.home_page_title = "Home - Leurres VS Stats"
        self.github_url = "https://github.com/FaillHarder/P13--Leurres-vs-Stats"

        self.first_carousel_h1 = "Vous ne savez pas quel leurre choisir?"
        self.second_carousel_h1 = "Nos statistiques"
        self.third_carousel_h1 = "Contribuez à améliorer nos Stats"
        return super().setUp()

    def tearDown(self) -> None:
        self.driver.quit()
        return super().tearDown()

    def test_home_page_title(self):
        self.driver.get(self.live_server_url)
        self.assertEqual(
            self.driver.title,
            self.home_page_title
        )

    def test_home_carousel(self):
        self.driver.get(self.live_server_url)
        first_carousel_h1 = self.driver.find_element_by_id("first-h1")
        self.assertTrue(first_carousel_h1, self.first_carousel_h1)

        next = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "carousel-control-next")))
        next.click()
        second_carousel_h1 = self.wait.until(EC.visibility_of_element_located((By.ID, "second-h1")))
        second_carousel_h1 = self.driver.find_element_by_id("second-h1")
        self.assertTrue(second_carousel_h1.text, self.second_carousel_h1)
        time.sleep(1)

        next2 = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "carousel-control-next")))
        next2.click()
        third_carousel_h1 = self.wait.until(EC.visibility_of_element_located((By.ID, "third-h1")))
        third_carousel_h1 = self.driver.find_element_by_id("third-h1")
        self.assertTrue(third_carousel_h1.text, self.third_carousel_h1)

    def test_footer_link_github(self):
        self.driver.get(self.live_server_url)
        self.wait.until(EC.element_to_be_clickable((By.NAME, "link-github")))
        self.driver.find_element_by_name("link-github").click()
        time.sleep(1)
        self.assertTrue(self.driver.current_url, self.github_url)


if __name__ == "main":
    SeleniumTest()
