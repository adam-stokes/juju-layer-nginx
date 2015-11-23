from charms.reactive import (
    set_state,
    is_state,
    hook
)

from charmhelpers.core import hookenv
from charmhelpers.fetch import apt_install
import os

config = hookenv.config()


# HOOKS -----------------------------------------------------------------------
@hook('install')
def install_nginx():
    """ Install nginx
    """
    hookenv.status_set('maintenance', 'Installing NGINX')

    # Install nginx-full
    if is_state('nginx.available'):
        return

    apt_install(['nginx-full'])
    if os.path.exists('/etc/nginx/sites-enabled/default'):
        os.remove('/etc/nginx/sites-enabled/default')

    set_state('nginx.available')
    hookenv.status_set('active', 'NGINX Installed.')

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
