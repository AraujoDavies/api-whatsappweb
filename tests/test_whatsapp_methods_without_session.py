from os import getenv

import pytest


@pytest.mark.withoutsess
def test_if_app_instanciate_is_success(test_zap):
    assert 'whatsweb_interactions.WhatsWebAPI' in str(type(test_zap))


@pytest.mark.withoutsess
def test_if_save_screenshot_works_without_browser(test_zap):
    assert test_zap.save_screenshot() == 'Chrome is closed'


@pytest.mark.withoutsess
def test_if_app_open_browser_is_success(test_zap):
    assert test_zap.run_browser() == 'Started with success.'


@pytest.mark.withoutsess
def test_if_is_possible_open_two_instances(test_zap):
    assert (
        test_zap.run_browser()
        == 'Instance is running. Kill it before continue'
    )


@pytest.mark.withoutsess
def test_if_return_search_bar_not_found_in_qrcode_screen(test_zap):
    assert test_zap.find_chat('Sla') == 'Search bar not found.'


@pytest.mark.withoutsess
def test_if_save_screenshot_works(test_zap):
    test_zap.driver[0].visit('https://docs.python.org/3/')
    assert test_zap.save_screenshot() == True


"""DEACTIVED THIS FEATURE"""
# @pytest.mark.withoutsess
# def test_if_login_code_is_returned_with_success(test_zap):
#     return_data = test_zap.get_login_code(getenv('VALID_PHONE_NUMBER'))
#     print(return_data)
#     assert len(return_data) == 9


# @pytest.mark.withoutsess
# def test_if_login_code_is_returned_with_success_in_invalid_number_cases(
#     test_zap,
# ):
#     assert test_zap.get_login_code(getenv('INVALID_PHONE_NUMBER')) == ''
"""DEACTIVED THIS FEATURE"""


@pytest.mark.withoutsess
def test_if_app_kill_browser_is_success(test_zap):
    assert test_zap.kill_browser() == 'Browser killed'
