from app.adddata.models import Lure, Color, SkyState, WaterState

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

import time


class SeleniumTest(LiveServerTestCase):

    def setUp(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(chrome_options=options)
        # self.driver = webdriver.Chrome("C:/Users/FailHarder/Desktop/chromedriver.exe", chrome_options=options)
        self.wait = WebDriverWait(self.driver, 10)

        self.lure = Lure.objects.create(name="stickbait")
        self.color_lure = Color.objects.create(name="ayu")
        self.sky_state = SkyState.objects.create(name="ensoleillé")
        self.water_state = WaterState.objects.create(name="clair")
        self.water_state2 = WaterState.objects.create(name="trouble")

        self.email = "test@test.fr"
        self.password = "monpassword85"

        self.search_path = "/search"
        self.stats_path = "/stats"
        self.login_path = "/accounts/login/"
        self.registrer_path = "/accounts/registrer"
        self.profile_path = "/accounts/profile/"
        self.profile_edit_path = "/accounts/profile/edit"
        self.my_catch_path = "/accounts/my_catch/"
        # /accounts/my_catch/edit/{id catchfish}/
        self.my_catch_edit_path = "/accounts/my_catch/edit/1/"
        # /accounts/my_catch/delete/{id catchfish}/
        self.my_catch_delete_path = "/accounts/my_catch/delete/1/"

        self.home_page_title = "Home - Leurres VS Stats"
        self.stats_page_title = "Stats - Leurres VS Stats"
        self.login_page_title = "Login - Leurres VS Stats"
        self.registrer_page_title = "Registrer - Leurres VS Stats"
        self.search_page_title = "Search - Leurres VS Stats"
        self.profile_page_title = "Profile - Leurres VS Stats"
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

    def test_login_user_with_bad_credential(self):
        self.driver.get(f"{self.live_server_url}{self.login_path}")
        # this login user return error message because user is not created
        self.login_user()
        self.wait.until(EC.visibility_of_element_located((By.NAME, "error")))
        error_message = self.driver.find_element(By.NAME, "error")
        self.assertEqual(error_message.text, "Email ou mot de passe invalide.")

    def test_create_account(self):
        self.driver.get(self.live_server_url)
        # click login icon
        time.sleep(1)
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
        self.create_account()
        # logout user
        self.wait.until(EC.element_to_be_clickable((By.NAME, "logout"))).click()
        # click login
        self.wait.until(EC.element_to_be_clickable((By.NAME, "login"))).click()
        self.login_user()
        # the profile icon is displayed if the user is connected
        profiel_icon = self.wait.until(EC.element_to_be_clickable((By.NAME, "profile")))
        self.assertTrue(profiel_icon.is_displayed())

    def test_search_page(self):
        self.create_account()
        self.wait.until(EC.element_to_be_clickable((By.NAME, "search"))).click()
        self.assertTrue(self.driver.current_url, f"{self.live_server_url}{self.search_path}")
        self.assertTrue(self.driver.title, self.search_page_title)

    def test_profile_page(self):
        self.create_account()
        self.wait.until(EC.element_to_be_clickable((By.NAME, "profile"))).click()
        self.assertTrue(self.driver.current_url, f"{self.live_server_url}{self.profile_path}")
        self.assertTrue(self.driver.title, self.profile_page_title)
        pseudo = self.driver.find_element(By.NAME, "pseudo")
        name = self.driver.find_element(By.NAME, "name")
        first_name = self.driver.find_element(By.NAME, "first_name")
        self.assertTrue(pseudo.text, "Test")
        self.assertTrue(name.text, "")
        self.assertTrue(first_name.text, "")

        # edit profile
        self.driver.find_element(By.NAME, "edit_profile").click()
        self.assertTrue(self.driver.current_url, f"{self.live_server_url}{self.profile_edit_path}")
        pseudo = self.driver.find_element(By.NAME, "pseudo")
        name = self.driver.find_element(By.NAME, "name")
        first_name = self.driver.find_element(By.NAME, "first_name")
        pseudo.clear()
        pseudo.send_keys("Newpseudo")
        name.send_keys("NewName")
        first_name.send_keys("Newfirst_name")
        self.driver.find_element(By.NAME, "valider").click()

        # check new profile
        self.assertTrue(self.driver.current_url, f"{self.live_server_url}{self.profile_path}")
        pseudo = self.driver.find_element(By.NAME, "pseudo")
        name = self.driver.find_element(By.NAME, "name")
        first_name = self.driver.find_element(By.NAME, "first_name")
        self.assertTrue(pseudo.text, "Newpseudo")
        self.assertTrue(name.text, "NewName")
        self.assertTrue(first_name.text, "Newfirst_name")

    def test_add_edit_delete_catchfish(self):
        self.create_account()
        self.wait.until(EC.element_to_be_clickable((By.NAME, "profile"))).click()
        # check catchfish = 0
        catch_count_0 = self.driver.find_element(By.NAME, "catch_count")
        self.assertTrue(catch_count_0.text, "Nombre de prise : 0")
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Ajouter une prise"))).click()
        # choice lure
        lure_choise = self.wait.until(EC.element_to_be_clickable((By.ID, "id_lure")))
        lure_choise.click()
        Select(self.driver.find_element(By.NAME, "lure")).select_by_index(1)
        lure_choise.click()
        # choice color
        color_choise = self.driver.find_element(By.NAME, "color_lure")
        color_choise.click()
        Select(self.driver.find_element(By.NAME, "color_lure")).select_by_index(1)
        color_choise.click()
        # choice sky_state
        sky_choise = self.driver.find_element(By.NAME, "sky_state")
        sky_choise.click()
        Select(self.driver.find_element(By.NAME, "sky_state")).select_by_index(1)
        sky_choise.click()
        # water_choice
        water_choise = self.driver.find_element(By.NAME, "water_state")
        water_choise.click()
        Select(self.driver.find_element(By.NAME, "water_state")).select_by_index(1)
        water_choise.click()
        # valider
        self.driver.find_element(By.NAME, "valider").click()
        # return profile page
        self.assertTrue(self.driver.current_url, f"{self.live_server_url}{self.profile_path}")
        # check catchfish = 1
        catch_count_1 = self.driver.find_element(By.NAME, "catch_count")
        self.assertTrue(catch_count_1.text, "Nombre de prise : 1")

        # click my_catch link
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Afficher mes prises"))).click()
        self.assertTrue(self.driver.current_url, f"{self.live_server_url}{self.my_catch_path}")
        # check lure name into table
        lure = self.driver.find_element(By.XPATH, f'//th[text()="{self.lure.name.title()}"]')
        self.assertTrue(lure.text, f"{self.lure.name.title()}")
        # check color_lure into table
        color_lure = self.driver.find_element(By.XPATH, f'//td[text()="{self.color_lure.name.title()}"]')
        self.assertTrue(color_lure.text, f"{self.color_lure.name.title()}")
        # check condition into table
        sky_and_water_state = self.driver.find_element(
            By.XPATH,
            f'//td[text()="{self.sky_state.name.title()} / {self.water_state.name.title()}"]'
        )
        self.assertTrue(sky_and_water_state.text, f"{self.sky_state.name.title()} / {self.water_state.name.title()}")

        # test edit function
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Modifier"))).click()
        self.assertTrue(self.driver.current_url, f"{self.live_server_url}{self.my_catch_edit_path}")
        # change water_state
        water_choise = self.driver.find_element(By.NAME, "water_state")
        water_choise.click()
        Select(self.driver.find_element(By.NAME, "water_state")).select_by_index(2)
        self.driver.find_element(By.NAME, "edit").click()
        # return my_catch page
        self.assertTrue(self.driver.current_url, f"{self.live_server_url}{self.my_catch_path}")

        # check the water state have changed
        sky_and_water_state = self.driver.find_element(
            By.XPATH,
            f'//td[text()="{self.sky_state.name.title()} / {self.water_state2.name.title()}"]'
        )
        self.assertTrue(sky_and_water_state, f"{self.sky_state.name.title()} / {self.water_state2.name.title()}")

        # test delete function
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Supprimer"))).click()
        self.assertTrue(self.driver.current_url, f"{self.live_server_url}{self.my_catch_delete_path}")
        # click supprimer
        self.wait.until(EC.element_to_be_clickable((By.NAME, "delete"))).click()
        # redirect my_catch page
        self.assertTrue(self.driver.current_url, f"{self.live_server_url}{self.my_catch_path}")
        no_result = self.driver.find_element(By.XPATH, '//th[text()="Aucun résultat"]')
        self.assertTrue(no_result.text, "Aucun résultat")
        # click link return to profile
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Retour"))).click()
        self.assertTrue(self.driver.current_url, f"{self.live_server_url}{self.profile_path}")
