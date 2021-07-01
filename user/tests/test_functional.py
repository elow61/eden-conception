""" All tests with Selenium for the user views application """
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from user.models import User
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


class RegisterTests(StaticLiveServerTestCase):
    """ Class to test the form register account """

    def setUp(self):
        self.selenium = webdriver.Chrome(
            ChromeDriverManager().install(),
            chrome_options=chrome_options
        )
        self.wait = WebDriverWait(self.selenium, 1000)
        super(RegisterTests, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(RegisterTests, self).tearDown()

    def define_elements(self):
        username_input = self.selenium.find_element_by_id('id_username')
        email_input = self.selenium.find_element_by_id('id_email')
        first_name_input = self.selenium.find_element_by_id('id_first_name')
        last_name_input = self.selenium.find_element_by_id('id_last_name')
        password1_input = self.selenium.find_element_by_id('id_password1')
        password2_input = self.selenium.find_element_by_id('id_password2')

        username_input.send_keys('email@test.com')
        email_input.send_keys('email@test.com')
        first_name_input.send_keys('test_first_name')
        last_name_input.send_keys('test_last_name')
        password1_input.send_keys('test_password_61')
        password2_input.send_keys('test_password_61')

    def test_register_click(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/register/'))
        submission_button = self.selenium.find_element_by_id("id_signup")
        self.define_elements()

        # Wait until the response is received
        ActionChains(self.selenium).click(submission_button).perform()

        time.sleep(2)
        redirection_url = self.selenium.current_url
        self.assertEqual(self.live_server_url + '/dashboard/', redirection_url)

    def test_register_keyboard(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/register/'))
        password2_input = self.selenium.find_element_by_id('id_password2')
        self.define_elements()

        password2_input.send_keys(Keys.ENTER)
        time.sleep(2)
        redirection_url = self.selenium.current_url
        self.assertEqual(self.live_server_url + '/dashboard/', redirection_url)
