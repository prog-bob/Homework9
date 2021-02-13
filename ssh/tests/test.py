
# перезагрузка сервера opencart с последующей проверкой, что opencart доступен,
def test_shutdown_opencart(ssh, admin_page):
    ssh.exec_command('docker exec -it vl_opencart_1 bash -c "apachectl -k graceful"')
    admin_page.login('demo', 'demo')
    assert admin_page.driver.title == 'Dashboard'


# рестарт основных сервисов для opencart с последующей проверкой, что сервис доступен.
def test_restart_services(ssh, admin_page):
    ssh.exec_command('docker exec -it vl_opencart_1 bash -c "sudo systemctl restart apache2.service"')
    admin_page.login('demo', 'demo')
    assert admin_page.driver.title == 'Dashboard'
