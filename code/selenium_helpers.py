import logging

from selenium.webdriver import ActionChains, Keys


def clean_input_field(driver, input_element) -> bool:
    """
    Click in element, press CTRL+A and BACKSPACE.

    Args:
        driver: selenium web driver

        input_element (_seleniumWebElement_): input field, shoud be selenium web element, where we will click to press CTRL+A and BACKSPACE.

    Return:
        process_run (_bool_): True | False
    """
    try:
        ac = ActionChains(driver)
        ac.move_to_element(input_element)
        ac.click()
        ac.key_down(Keys.CONTROL)
        ac.key_down('A')
        ac.key_up('A')
        ac.key_up(Keys.CONTROL)
        ac.key_down(Keys.BACKSPACE)
        ac.key_up(Keys.BACKSPACE)
        ac.perform()
        return True
    except Exception as error:
        logging.critical(error)
        return False
