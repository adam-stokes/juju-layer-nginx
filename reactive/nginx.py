from charms.reactive import (
    set_state,
    when_not,
    when
)

from charmhelpers.core import hookenv
from charms import apt
import os

config = hookenv.config()


# handlers --------------------------------------------------------------------
@when_not('nginx.available')
def install_nginx():
    """ Install nginx
    """
    apt.queue_install(['nginx-full'])
    if os.path.exists('/etc/nginx/sites-enabled/default'):
        os.remove('/etc/nginx/sites-enabled/default')


@when('apt.installed.nginx')
@when_not('nginx.available')
def nginx_ready():
    hookenv.status_set('active', 'NGINX is ready')
    set_state('nginx.available')

# Example website.available reaction ------------------------------------------
"""
This example reaction for an application layer which consumes this nginx layer.
If left here then this reaction may overwrite your top-level reaction depending
on service names, ie., both nginx and ghost have the same reaction method,
however, nginx will execute since it's a higher precedence.

@when('nginx.available', 'website.available')
def configure_website(website):
    website.configure(port=config['port'])
"""
