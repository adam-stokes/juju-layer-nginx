from charms.reactive import (
    when,
    set_state,
    remove_state,
    is_state
)

from charmhelpers.core import hookenv
from charmhelpers.fetch import apt_install
from charmhelpers.core.templating import render
import toml

config = hookenv.config()


# HELPERS ---------------------------------------------------------------------
def all_sites():
    """ Returns a list of known vhosts
    """
    try:
        with open('sites.toml') as fp:
            sites = toml.loads(fp.read())
        return sites
    except IOError:
        hookenv.log('No sites.toml found, not configuring vhosts', 'warning')
        return False


def process_sites():
    sites = all_sites()
    if sites:
        for site in sites.keys():
            hookenv.log(
                'Processing site: {} @ {}'.format(site,
                                                  sites[site]['server_name']),
                'debug')
            configure_site(site, sites[site])


def configure_site(site, context):
    """ configures vhost
    """
    hookenv.status_set('maintenance', 'Configuring site {}'.format(site))
    render(source='vhost.conf',
           target='/etc/nginx/sites-enabled/{}'.format(site),
           context={
               'server_name': context['server_name'],
               'host': config['host'],
               'port': config['port']
           })


# REACTORS --------------------------------------------------------------------
@when('nginx.install')
def install_nginx():
    """ Install nginx
    """
    hookenv.status_set('maintenance', 'Installing NGINX')

    # Install nginx-full
    if is_state('nginx.available'):
        return

    apt_install(['nginx-full'])
    process_sites()
    remove_state('nginx.install')
    set_state('nginx.available')


@when('website.available')
def configure_website(website):
    website.configure(config['port'])
