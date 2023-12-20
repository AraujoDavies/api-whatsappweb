# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from splinter import Browser
# from webdriver_manager.chrome import ChromeDriverManager
# from datetime import datetime
# from selenium.webdriver import ActionChains, Keys


# def chromewebdriver(headless=False) -> webdriver:
#     """
#     Sets chrome options for Selenium.
#     Chrome options for headless browser is enabled.

#     Args:
#         headless (_bool_): run in background. Default value is False

#     Returns:
#         chromedriver browser - splinter
#     """
#     chrome_options = Options()
#     if headless is True:
#         chrome_options.add_argument('--headless')
#         chrome_options.add_argument('--no-sandbox')
#         chrome_options.add_argument('--disable-dev-shm-usage')
#         # optins above is to fix message => whatsapp work with google chrome 60+
#         chrome_options.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
#         chrome_prefs = {}
#         chrome_options.experimental_options['prefs'] = chrome_prefs
#         chrome_prefs['profile.default_content_settings'] = {
#             'images': 2
#         }   # não carregar imagens

#     profile='/app/ec2/profile1'
#     chrome_options.add_argument(f"user-data-dir={profile}")

#     service = Service(ChromeDriverManager().install())
#     # driver = webdriver.Chrome(options=chrome_options, service=service)
#     driver = Browser('chrome', options=chrome_options, service=service)

#     return driver


# # teste zapzap-automation
# def get_login_code(driver):
#     url='https://web.whatsapp.com/'

#     driver.visit(url)

#     btn_conectar_com_numero = '//span[@role="button"]'
#     driver.is_element_present_by_xpath(btn_conectar_com_numero, wait_time=15)
#     driver.find_by_xpath(btn_conectar_com_numero).first.click()

#     input_whastsapp_number = '//input[@aria-label="Insira seu número de telefone."]'
#     input_whastsapp_number = '//input[@aria-label="Type your phone number."]'
#     driver.is_element_present_by_xpath(input_whastsapp_number, wait_time=15)

#     input_whastsapp_number_sel = driver.driver.find_element('xpath', input_whastsapp_number)
#     input_whastsapp_number = driver.find_by_xpath(input_whastsapp_number).first

#     ac = ActionChains(driver.driver)
#     ac.move_to_element(input_whastsapp_number_sel)
#     ac.click()
#     ac.key_down(Keys.CONTROL)
#     ac.key_down('A')
#     ac.key_up('A')
#     ac.key_up(Keys.CONTROL)
#     ac.key_down(Keys.BACKSPACE)
#     ac.key_up(Keys.BACKSPACE)
#     ac.perform()
#     input_whastsapp_number.fill('+5511930628076')

#     btn_avancar = '//div[@role="button"]'
#     driver.find_by_xpath(btn_avancar).first.click()

#     code_to_login = '//div[@aria-details="link-device-phone-number-code-screen-instructions"]//span'
#     letters = driver.find_by_xpath(code_to_login)
#     code_string = [letter.text for letter in letters]
#     code = ''
#     for some_letter in code_string:
#         code += some_letter

#     return code


# def get_print_screen(driver):
#     filename = f'prt_{str(datetime.now().timestamp()).split(".")[0]}.png'
#     filename = driver.driver.save_screenshot(filename)
#     return filename


# driver = chromewebdriver(headless=True)
# url='https://web.whatsapp.com/'
# driver.visit(url)
# # driver = chromewebdriver()
