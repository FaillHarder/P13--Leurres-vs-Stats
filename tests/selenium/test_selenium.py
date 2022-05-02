from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SeleniumTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        options = Options()
        options.headless = True
        cls.driver = webdriver.Chrome(chrome_options=options)
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()
        return super().tearDownClass()

    def test_home_page(self):
        self.driver.get(self.live_server_url)
        self.assertEqual(
            self.driver.title,
            "Home - Leurres VS Stats"
        )
