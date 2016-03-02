from fabric.api import env, task
from envassert import detect, file, port, process, service, user
from hot.utils.test import get_artifacts, http_check
import socket

@task
def check():
    env.platform_family = detect.detect()

    assert file.exists('/var/www/vhosts/example.com/httpdocs/xmlrpc.php'),\
        'xmlrpc.php did not exist'

    assert port.is_listening(80), 'port 80/nginx is not listening'

    if (env.platform_family == "rhel"):
        assert process.is_up('nginx'), 'nginx is not running'
        assert process.is_up('php-fpm'), 'php-fpm is not running'
        assert service.is_enabled('nginx'), 'nginx is not enabled'
        assert service.is_enabled('php-fpm'), 'php-fpm is not enabled'
    elif (env.platform_family == 'debian'):
        assert process.is_up('nginx'), 'nginx is not running'
        assert process.is_up('php5-fpm'), 'php-fpm is not running'
        assert service.is_enabled('nginx'), 'nginx is not enabled'
        assert service.is_enabled('php5-fpm'), 'php-fpm is not enabled'

    if ("secondary" not in socket.gethostname()):
        assert service.is_enabled('lsyncd'), 'lsyncd is not enabled'


    assert http_check('http://localhost/', 'Powered by WordPress')

@task
def artifacts():
    env.platform_family = detect.detect()
    artifacts = ['/var/log/messages',
                 '/var/log/syslog',
                 '/var/log/cloud-init.log',
                 '/var/log/cloud-init-output.log']
    get_artifacts(artifacts=artifacts)
