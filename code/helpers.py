import logging
import re

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


def paste_content(driver, el, content):
    """
    params:
        driver -> webdriver
        el -> webelement
        content -> mensagem
    """
    driver.execute_script(
        f"""
const text = `{content}`;
const dataTransfer = new DataTransfer();
dataTransfer.setData('text', text);
const event = new ClipboardEvent('paste', {{
  clipboardData: dataTransfer,
  bubbles: true
}});
arguments[0].dispatchEvent(event)
""",
        el,
    )


def validate_number(number: str):
    """
    Accept only character beetwen 0 and 9

    Args:
        number (str): some string - input by user.

    Returns:
        _bool_: True if only numbers or False if contain other character.

    Examples:
        >>> validate_number("123456")
        True
        >>> validate_number("987654")
        True
        >>> validate_number("abc123")
        False
        >>> validate_number("12 34 56")
        False
    """
    padrao = re.compile(r'^\d+$')
    return bool(padrao.match(number))


def send_message_by_selenium(driver, input_element, message: str) -> bool:
    """
    Send message by selenium event.

    Args:
        driver: selenium web driver

        input_element (_seleniumWebElement_): input field, shoud be selenium web element, where we will click to start to send message.

        message: some text.

    Return:
        process_run (_bool_): True | False
    """
    try:
        actions = ActionChains(driver)

        actions.move_to_element(input_element)
        message = message.replace('\n', '¨')
        for letra in message:
            if letra != '¨':
                actions.key_down(letra)
                actions.key_up(letra)
            else:
                actions.key_down(Keys.SHIFT)
                actions.key_down(Keys.ENTER)
                actions.key_up(Keys.ENTER)
                actions.key_up(Keys.SHIFT)

        actions.perform()
        return True
    except Exception as error:
        logging.critical(error)
        return False
