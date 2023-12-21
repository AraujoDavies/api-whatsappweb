from datetime import datetime
from os import getenv

from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


class WhatsWebAPI:
    """
    This class contains all whatsapp web actions that project will do.
    """

    def __init__(self, user_id: int = 0, profile: str = 'NA', headless=True):
        """
        Class Vars.

        Args:
            user_id (_int_): ID to identify user and save logs.

            profile (_str_): Where data is saved to keep Whatsapp working all the time.

            headless (_bool_): True if browser will running in background or False if you want to see browser open (in servers without visual interface, we always set True in this value).

        """
        self.headless = headless
        self.profile = profile
        self.user_id = user_id
        self.driver_state = 'Not started'
        self.driver = []

    def run_browser(self) -> str:
        """
        Open browser to start interactions.

        return:
            driver_state (_str_): How browser's found.

        Examples:
            >>> app = WhatsWebAPI()
            <whatsweb_interactions.WhatsWebAPI at 0x1231c879f50>
            >>> app.run_browser()
            'Started with success.'

        """
        if len(self.driver) >= 1:   # if have one running
            self.driver_state = 'Instance is running. Kill it before continue'
            return self.driver_state

        try:
            headless = self.headless
            profile = self.profile

            browser_options = Options()
            if headless is True:
                browser_options.add_argument('--headless')
                browser_options.add_argument('--no-sandbox')
                browser_options.add_argument('--disable-dev-shm-usage')
                # optins above is to fix message => whatsapp work with google chrome 60+
                browser_options.add_argument(
                    'user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
                )
                browser_prefs = {}
                browser_options.experimental_options['prefs'] = browser_prefs
                browser_prefs['profile.default_content_settings'] = {
                    'images': 2
                }   # não carregar imagens

            if profile != 'NA':
                browser_options.add_argument(f'user-data-dir={profile}')

            service = Service(ChromeDriverManager().install())

            driver = Browser(
                'chrome', options=browser_options, service=service
            )
            self.driver.append(driver)

            self.driver_state = 'Started with success.'

        except Exception as error:
            self.driver_state = 'RUN BROWSER ERROR:' + error

        finally:
            return self.driver_state

    def kill_browser(self):
        """
        Close an open browser.

        Return:
            driver_state (_str_): How browser's found.

        Examples:
            >>> app = WhatsWebAPI()
            <whatsweb_interactions.WhatsWebAPI at 0x1231c879f50>
            >>> app.run_browser()
            'Started with success.'
            >>> app.kill_browser()
            'Browser killed'
        """
        try:
            driver = self.driver[0]
            driver.quit()
            self.driver.clear()
            self.driver_state = 'Browser killed'

        except Exception as error:
            self.driver_state = 'KILL BROWSER ERROR' + error

        finally:
            return self.driver_state

    def save_screenshot(self) -> str | bool | Exception:
        """
        Get some screenshot of the browser.

        Return:
            screenshot_state | Exception

        Example:
            >>> app.driver[0].visit('https://www.google.com')
            >>> app.save_screenshot()
            True
        """
        try:
            if len(self.driver) != 1:
                return 'Chrome is closed'
            driver = self.driver[0]
            user_id = self.user_id
            filename = f'user_{user_id}_date_{str(datetime.now().timestamp()).split(".")[0]}.png'
            screenshot_state = driver.driver.save_screenshot(filename)
            return screenshot_state
        except Exception as error:
            return error

    def get_login_code(
        self, phone_number: str, url: str = 'https://web.whatsapp.com/'
    ) -> str | Exception:
        """
        Get login code using a phone number.

        Args:
            phone_number (_str_): [countrycode][areacode][number]

            url (_str_): default value is 'https://web.whatsapp.com/'

        Return:
            code to login | Exception

        Examples:
            >>> app = WhatsWebAPI()
            <whatsweb_interactions.WhatsWebAPI at 0x1231c879f50>
            >>> app.get_login_code('5511987654321')
            a code like: 'P8FD-8K92'
            >>> app.get_login_code()
            a code like: 'B7Z3-DDX9'
        """
        try:
            driver = self.driver[0]

            driver.visit(url)

            btn_conectar_com_numero = '//span[@role="button"]'
            driver.is_element_present_by_xpath(
                btn_conectar_com_numero, wait_time=15
            )
            driver.find_by_xpath(btn_conectar_com_numero).first.click()

            input_whastsapp_number = (
                '//input[@aria-label="Type your phone number."]'
            )
            input_whastsapp_number = (
                '//input[@aria-label="Insira seu número de telefone."]'
            )
            driver.is_element_present_by_xpath(
                input_whastsapp_number, wait_time=15
            )

            input_whastsapp_number_sel = driver.driver.find_element(
                'xpath', input_whastsapp_number
            )
            input_whastsapp_number = driver.find_by_xpath(
                input_whastsapp_number
            ).first

            ac = ActionChains(driver.driver)
            ac.move_to_element(input_whastsapp_number_sel)
            ac.click()
            ac.key_down(Keys.CONTROL)
            ac.key_down('A')
            ac.key_up('A')
            ac.key_up(Keys.CONTROL)
            ac.key_down(Keys.BACKSPACE)
            ac.key_up(Keys.BACKSPACE)
            ac.perform()
            input_whastsapp_number.fill('+' + phone_number)

            btn_avancar = '//div[@role="button"]'
            driver.find_by_xpath(btn_avancar).first.click()

            code_to_login = '//div[@aria-details="link-device-phone-number-code-screen-instructions"]//span'
            letters = driver.find_by_xpath(code_to_login)
            code_string = [letter.text for letter in letters]
            code = ''
            for some_letter in code_string:
                code += some_letter

            return code
        except Exception as error:
            return error
