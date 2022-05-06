from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


class SeleniumTest(LiveServerTestCase):

    def setUp(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.driver, 10)
        # self.driver = webdriver.Chrome("C:/Users/FailHarder/Desktop/chromedriver.exe", chrome_options=options)

        self.email = "test@test.fr"
        self.password = "monpassword85"

        self.search_path = "/search"
        self.stats_path = "/stats"
        self.login_path = "/accounts/login/"
        self.registrer_path = "/accounts/registrer"

        self.home_page_title = "Home - Leurres VS Stats"
        self.stats_page_title = "Stats - Leurres VS Stats"
        self.login_page_title = "Login - Leurres VS Stats"
        self.registrer_page_title = "Registrer - Leurres VS Stats"
        self.search_page_title = "Search - Leurres VS Stats"
        self.next = "?next="

        self.github_url = "https://github.com/FaillHarder/P13--Leurres-vs-Stats"

        self.first_carousel_h1 = "Vous ne savez pas quel leurre choisir?"
        self.second_carousel_h1 = "Nos statistiques"
        self.third_carousel_h1 = "Contribuez à améliorer nos Stats"
        return super().setUp()

    def tearDown(self):
        self.driver.quit()
        return super().tearDown()

    def fill_and_valid_registrer_form(self):
        # create email
        email = self.driver.find_element(By.NAME, "email")
        email.send_keys(self.email)
        # create password
        password1 = self.driver.find_element(By.NAME, "password1")
        password1.send_keys(self.password)
        password2 = self.driver.find_element(By.NAME, "password2")
        password2.send_keys(self.password)
        # click validate form
        self.driver.find_element(By.NAME, "submit-registrer").click()

    def create_account(self):
        self.driver.get(f"{self.live_server_url}{self.registrer_path}")
        self.fill_and_valid_registrer_form()

    def login_user(self):
        email = self.driver.find_element(By.NAME, "email")
        email.send_keys(self.email)
        password1 = self.driver.find_element(By.NAME, "password")
        password1.send_keys(self.password)
        # validate form
        self.driver.find_element(By.NAME, "submit-login").click()

    def test_home_page(self):
        self.driver.get(self.live_server_url)
        self.assertEqual(self.driver.title, self.home_page_title)

    def test_home_carousel(self):
        self.driver.get(self.live_server_url)
        first_carousel_h1 = self.driver.find_element(By.ID, "first-h1")
        self.assertTrue(first_carousel_h1, self.first_carousel_h1)
        # click next arrow
        next = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "carousel-control-next")))
        next.click()
        second_carousel_h1 = self.wait.until(EC.visibility_of_element_located((By.ID, "second-h1")))
        second_carousel_h1 = self.driver.find_element(By.ID, "second-h1")
        self.assertTrue(second_carousel_h1.text, self.second_carousel_h1)
        time.sleep(1)
        # click next arrow
        next2 = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "carousel-control-next")))
        next2.click()
        third_carousel_h1 = self.wait.until(EC.visibility_of_element_located((By.ID, "third-h1")))
        third_carousel_h1 = self.driver.find_element(By.ID, "third-h1")
        self.assertTrue(third_carousel_h1.text, self.third_carousel_h1)

    def test_footer_link_github(self):
        self.driver.get(self.live_server_url)
        self.wait.until(EC.element_to_be_clickable((By.NAME, "link-github"))).click()
        self.wait.until(EC.url_changes(self.github_url))
        self.assertTrue(self.driver.current_url, self.github_url)

    def test_navbar_links(self):
        self.driver.get(self.live_server_url)
        # test_stats_link
        self.wait.until(EC.element_to_be_clickable((By.NAME, "stats_link"))).click()
        self.assertTrue(self.driver.title, self.stats_page_title)
        self.assertTrue(self.driver.current_url, f"{self.live_server_url}{self.stats_path}")
        # test_home_link
        self.wait.until(EC.element_to_be_clickable((By.NAME, "home"))).click()
        self.assertTrue(self.driver.title, self.home_page_title)
        self.assertTrue(self.driver.current_url, self.live_server_url)
        # test_login_link
        self.wait.until(EC.element_to_be_clickable((By.NAME, "login"))).click()
        self.assertTrue(self.driver.title, self.login_page_title)
        self.assertTrue(self.driver.current_url, f"{self.live_server_url}{self.login_path}")

    def test_login_user_with_bad_credential(self):
        self.driver.get(f"{self.live_server_url}{self.login_path}")
        # this login user return error message because user is not created
        self.login_user()
        # error message
        self.wait.until(EC.visibility_of_element_located((By.NAME, "error")))
        error_message = self.driver.find_element(By.NAME, "error")
        self.assertEqual(error_message.text, "Email ou mot de passe invalide.")

    def test_create_account(self):
        self.driver.get(self.live_server_url)
        # click login icon
        self.wait.until(EC.element_to_be_clickable((By.NAME, "login"))).click()
        self.assertTrue(self.driver.title, self.login_page_title)
        self.assertTrue(self.driver.current_url, f"{self.live_server_url}{self.login_path}")
        # click create account
        self.driver.find_element_by_link_text("Créer un compte").click()
        self.assertTrue(self.driver.title, self.registrer_page_title)
        self.assertTrue(self.driver.current_url, f"{self.live_server_url}{self.registrer_path}")
        # create account
        self.fill_and_valid_registrer_form()
        self.wait.until(EC.url_changes(self.live_server_url))
        # redirct home
        self.assertTrue(self.driver.current_url, self.live_server_url)
        # icon logout is displayed
        logout_icon = self.wait.until(EC.element_to_be_clickable((By.NAME, "logout")))
        self.assertTrue(logout_icon.is_displayed())

    def test_login_user(self):
        self.driver.get(f"{self.live_server_url}{self.registrer_path}")
        self.create_account()
        # logout user
        self.wait.until(EC.element_to_be_clickable((By.NAME, "logout"))).click()
        # click login
        self.wait.until(EC.element_to_be_clickable((By.NAME, "login"))).click()
        self.login_user()
        # the profile icon is displayed if the user is connected
        profiel_icon = self.wait.until(EC.element_to_be_clickable((By.NAME, "profile")))
        self.assertTrue(profiel_icon.is_displayed())

    def test_search_link_redirect_login(self):
        # create account and disconect user
        self.create_account()
        self.wait.until(EC.element_to_be_clickable((By.NAME, "logout"))).click()
        # start test
        self.wait.until(EC.element_to_be_clickable((By.NAME, "search"))).click()
        # redirect login
        self.wait.until(EC.url_changes(f"{self.live_server_url}{self.next}{self.search_path}"))
        self.assertTrue(self.driver.current_url, f"{self.live_server_url}{self.next}{self.search_path}")
        # login user
        self.login_user()
        self.assertTrue(self.driver.current_url, f"{self.live_server_url}{self.search_path}")
        self.assertTrue(self.driver.title, self.search_page_title)


if __name__ == "main":
    SeleniumTest()
