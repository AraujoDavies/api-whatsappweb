def test_if_app_instanciate_is_success(test_app):
    assert 'whatsweb_interactions.WhatsWebAPI' in str(type(test_app))


def test_if_save_screenshot_works_without_browser(test_app):
    assert test_app.save_screenshot() == 'Chrome is closed'


def test_if_app_open_browser_is_success(test_app):
    assert test_app.run_browser() == 'Started with success.'


def test_if_is_possible_open_two_instances(test_app):
    assert (
        test_app.run_browser()
        == 'Instance is running. Kill it before continue'
    )


def test_if_save_screenshot_works(test_app):
    test_app.driver[0].visit('https://www.google.com')
    assert test_app.save_screenshot() == True


def test_if_app_kill_browser_is_success(test_app):
    assert test_app.kill_browser() == 'Browser killed'
