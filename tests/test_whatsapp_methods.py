from os import getenv


def test_if_app_instanciate_is_success(test_app):
    assert 'whatsweb_interactions.WhatsWebAPI' in str(type(test_app))


def test_if_save_screenshot_works_without_browser(test_app):
    test_app.save_screenshot()   # printscreen before to use remove file IF
    assert test_app.save_screenshot() == 'Chrome is closed'


def test_if_app_open_browser_is_success(test_app):
    assert test_app.run_browser() == 'Started with success.'


def test_if_is_possible_open_two_instances(test_app):
    assert (
        test_app.run_browser()
        == 'Instance is running. Kill it before continue'
    )


def test_if_save_screenshot_works(test_app):
    test_app.driver[0].visit('https://docs.python.org/3/')
    assert test_app.save_screenshot() == True


def test_if_login_code_is_returned_with_success(test_app):
    return_data = test_app.get_login_code(getenv('VALID_PHONE_NUMBER'))
    print(return_data)
    assert len(return_data) == 9


def test_if_login_code_is_returned_with_success_in_invalid_number_cases(
    test_app,
):
    assert test_app.get_login_code(getenv('INVALID_PHONE_NUMBER')) == ''


def test_if_app_kill_browser_is_success(test_app):
    assert test_app.kill_browser() == 'Browser killed'


def test_if_chat_that_exists_is_find(test_app_on):
    test_app_on.run_browser()
    assert test_app_on.find_chat('Sla') == 'Chat found.'


def test_if_send_message_fail_in_cases_that_not_contain_any_message(
    test_app_on,
):
    assert test_app_on.send_message('') == 'Message failed - input is empty'


def test_if_send_message(test_app_on):
    assert test_app_on.send_message('Hello world!') == 'Message sended'


def test_if_send_message_with_emojis(test_app_on):
    assert test_app_on.send_message('💰🐯📚🎯💰🚀') == 'Message sended'


def test_if_send_message_with_emojis_using_ctrlc_parameter(test_app_on):
    assert test_app_on.send_message('💰🐯📚🎯💰🚀', True) == 'Message sended'


def test_if_chat_that_not_exists_is_find(test_app_on):
    assert test_app_on.find_chat('NOT_FOUND_CHAT') == 'Chat name not found.'
    test_app_on.kill_browser()
