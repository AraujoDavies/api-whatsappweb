import logging
from os import getenv, listdir, mkdir, remove, getcwd, sep
from time import sleep

from dotenv import load_dotenv
from helpers import clean_input_field, paste_content, send_message_by_selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()


class WhatsWebAPI:
    """
    This class contains all whatsapp web actions that project will do.
    """

    def __init__(self, user_phone_number: int = 0, headless=True):
        """
        Class Vars.

        Args:
            user_phone_number (_int_): ID to identify user and save logs.

            profile (_str_): Where data is saved to keep Whatsapp working all the time.

            headless (_bool_): True if browser will running in background or False if you want to see browser open (in servers without visual interface, we always set True in this value).

        """
        self.headless = headless
        self.profile = getcwd() + sep + 'profiles' + sep + str(user_phone_number)
        self.user_phone_number = user_phone_number
        self.driver_state = 'Not started'
        self.driver = []
        self.url = getenv('URL_WHATSAPP')
        try:
            mkdir(self.profile)
        except Exception as error:
            print(f'already exists or not located -> {self.profile}')

    def run_browser(self) -> str:
        """
        Open browser to start interactions.

        return:
            driver_state (_str_): How browser's found.

        Examples:
            >>> app = WhatsWebAPI()
            <whatsweb_interactions.WhatsWebAPI at 0x1231c879f50>
            >>> zap.run_browser()
            'Started with success.'

        """
        if len(self.driver) >= 1:   # if have one running
            self.driver_state = 'Instance is running. Kill it before continue'
            return self.driver_state

        try:
            headless = self.headless
            profile = self.profile

            browser_options = Options()
            browser_options.add_argument("--force-device-scale-factor=0.8")
            if headless is True:
                browser_options.add_argument('--headless')
                browser_options.add_argument('--no-sandbox')
                browser_options.add_argument('--disable-dev-shm-usage')
                # optins above is to fix message => whatsapp work with google chrome 60+
                # browser_options.add_argument(
                  #  'user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
                # )
                browser_prefs = {}
                browser_options.experimental_options['prefs'] = browser_prefs
                browser_prefs['profile.default_content_settings'] = {
                    'images': 2
                }   # não carregar imagens

            if profile != 'NA':
                browser_options.add_argument(f'user-data-dir={profile}')

            # service = Service(ChromeDriverManager().install())

            driver = Browser(
                'chrome', options=browser_options # , service=service
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
            >>> zap.run_browser()
            'Started with success.'
            >>> zap.kill_browser()
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
            >>> zap.driver[0].visit('https://www.google.com')
            >>> zap.save_screenshot()
            True
        """
        try:
            if len(self.driver) != 1:
                return 'Chrome is closed'
            driver = self.driver[0]
            user_phone_number = self.user_phone_number
            filename = f'user_{user_phone_number}.png'

            try:
                for file in listdir('./prints/'):
                    print(file)
                    if f'user_{user_phone_number}_' in file:
                        remove('./prints/' + file)
            except:
                mkdir('prints')

            screenshot_state = driver.driver.save_screenshot(
                './prints/' + filename
            )
            return screenshot_state
        except Exception as error:
            return error

    def find_chat(self, chat_name: str) -> str | Exception:
        """
        fill search bar input for find some chat to send message.

        Args:
            chat_name (_str_): name of the chat that message will send. (need to be equal)

        Return:
            Chat state | Exception

        Examples:
            >>> zap.get_login_code('5511987654321')
            Chat found. | Chat name not found.
        """
        driver = self.driver[0]
        # verifica se a barra está na tela
        search_bar = driver.is_element_present_by_xpath(
            getenv('CAIXA_DE_PESQUISA'),
            wait_time=5,
        )

        # caso sim prossiga
        if search_bar is False:   # Recarregue a página para continuar...
            url = self.url
            driver.visit(url)
            sleep(5)
            search_bar = driver.is_element_present_by_xpath(
                getenv('CAIXA_DE_PESQUISA'),
                wait_time=60,
            )
            if search_bar is False:   # se ainda é falso
                return 'Search bar not found.'

        search_bar_sel = driver.driver.find_element(
            'xpath',
            getenv('CAIXA_DE_PESQUISA'),
        )
        clean_input_field(driver=driver.driver, input_element=search_bar_sel)

        try:
            find_chat = driver.find_by_xpath(getenv('CAIXA_DE_PESQUISA')).first

            find_chat.fill(chat_name)

            chat = driver.find_by_xpath(f'//span[@title="{chat_name}"]')

            chat.click()

            return 'Chat found.'
        except Exception as error:
            # CHAT NOT FOUND
            logging.error(error)
            if 'no elements could be found with xpath "//span[@title=' in str(
                error
            ):
                return 'Chat name not found.'
            return error

    def send_message(
        self, message: str, ctrl_c: bool = False
    ) -> str | Exception:
        """
        Send messages in some chat.

        Args:
            ctrl_c (_bool_): Case want to send message using CTRL+S (JS event). Default value is False, messsage send by selenium event, this feature is reccomend is cases that message contains EMOJIS.

        Return:
            Message state | Exception

        Examples:
            >>> zap.send_message()
            'message sended'
        """
        try:
            driver = self.driver[0]
            input_message = driver.driver.find_element(
                'xpath', getenv('CAIXA_MENSAGEM')
            )   # //p[contains(@class, "selectable-text")]')

            clean_input_field(driver.driver, input_message)

            if ctrl_c is True:
                paste_content(driver.driver, input_message, message)
            else:
                try:
                    send_message_by_selenium(
                        driver.driver,
                        input_message,
                        message,
                    )
                except:
                    paste_content(driver.driver, input_message, message)

            try:
                fecha_link_preview = driver.find_by_xpath(
                    '//div[@data-testid="popup_panel"]//span[@data-testid="x"]'
                )
                fecha_link_preview.click()
            except:
                ...

            try:
                send_btn = driver.find_by_xpath(getenv('BOTAO_ENVIAR'))
                send_btn.click()
                return 'Message sended'
            except ElementDoesNotExist as e:
                return 'Message failed - input is empty'
        except Exception as error:
            return error


    def skip_errors(self) -> None:
        """Pula mensagens do whatsapp."""
        driver = self.driver[0]

        try:
            continuar = driver.find_by_text('Continuar').first # "o whats está de cara nova..."
            continuar.click()
            logging.warning('msg: "o whats está de cara nova..."')
        except:
            logging.warning('Não encontrou btn "continuar" para msg: "o whats está de cara nova..."')
            pass
        
        return None

    # def get_login_code(self, phone_number: str) -> str | Exception:
    #     """
    #     Get login code using a phone number.

    #     Args:
    #         phone_number (_str_): [countrycode][areacode][number]

    #     Return:
    #         code to login | Exception

    #     Examples:
    #         >>> app = WhatsWebAPI()
    #         <whatsweb_interactions.WhatsWebAPI at 0x1231c879f50>
    #         >>> zap.get_login_code('5511987654321')
    #         'P8FD-8K92'
    #         >>> zap.get_login_code('5511987654321')
    #         'B7Z3-DDX9'
    #     """
    #     try:
    #         driver = self.driver[0]
    #         url = self.url
    #         driver.visit(url)

    #         btn_conectar_com_numero = '//span[@role="button"]'
    #         driver.is_element_present_by_xpath(
    #             btn_conectar_com_numero, wait_time=15
    #         )
    #         driver.find_by_xpath(btn_conectar_com_numero).first.click()

    #         input_whastsapp_number = (
    #             '//input[@aria-label="Type your phone number."]'
    #         )
    #         input_whastsapp_number = (
    #             '//input[@aria-label="Insira seu número de telefone."]'
    #         )
    #         driver.is_element_present_by_xpath(
    #             input_whastsapp_number, wait_time=15
    #         )

    #         input_whastsapp_number_sel = driver.driver.find_element(
    #             'xpath', input_whastsapp_number
    #         )
    #         input_whastsapp_number = driver.find_by_xpath(
    #             input_whastsapp_number
    #         ).first

    #         result_clean_input = clean_input_field(
    #             driver=driver.driver, input_element=input_whastsapp_number_sel
    #         )

    #         if result_clean_input is False:
    #             # error to clean input
    #             return 'Fail to clean input field - see logging'

    #         input_whastsapp_number.fill('+' + phone_number)

    #         btn_avancar = '//div[@role="button"]'
    #         driver.find_by_xpath(btn_avancar).first.click()

    #         code_to_login = '//div[@aria-details="link-device-phone-number-code-screen-instructions"]//span'
    #         letters = driver.find_by_xpath(code_to_login)
    #         code_string = [letter.text for letter in letters]
    #         code = ''
    #         for some_letter in code_string:
    #             code += some_letter

    #         return code
    #     except Exception as error:
    #         return error


if __name__ == '__main__':
    zap = WhatsWebAPI(1)
    a = zap.run_browser()