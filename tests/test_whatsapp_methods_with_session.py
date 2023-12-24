import pytest


@pytest.mark.withsess
def test_if_chat_that_exists_is_find(test_zap_on):
    test_zap_on.run_browser()
    assert test_zap_on.find_chat('Sla') == 'Chat found.'


@pytest.mark.withsess
def test_if_send_message_fail_in_cases_that_not_contain_any_message(
    test_zap_on,
):
    assert test_zap_on.send_message('') == 'Message failed - input is empty'


@pytest.mark.withsess
def test_if_send_message(test_zap_on):
    assert test_zap_on.send_message('Hello world!') == 'Message sended'


@pytest.mark.withsess
def test_if_send_message_with_emojis(test_zap_on):
    assert test_zap_on.send_message('💰🐯📚🎯💰🚀') == 'Message sended'


@pytest.mark.withsess
def test_if_send_message_with_emojis_using_ctrlc_parameter(test_zap_on):
    assert test_zap_on.send_message('💰🐯📚🎯💰🚀', True) == 'Message sended'


@pytest.mark.withsess
def test_if_chat_that_not_exists_is_find(test_zap_on):
    assert test_zap_on.find_chat('NOT_FOUND_CHAT') == 'Chat name not found.'
    assert test_zap_on.kill_browser() == 'Browser killed'
