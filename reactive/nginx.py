from charms.reactive import (
    when,
    when_not,
    set_state,
    remove_state,
    is_state,
    hook
)

from charmhelpers.core import hookenv, host
from charmhelpers.fetch import apt_install
from charmhelpers.core.templating import render
import toml


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
            hookenv.log('Processing site: {}'.format(site), 'debug')
            configure_site(site, sites[site])


def configure_site(site, context):
    """ configures vhost
    """
    hookenv.status_set('maintenance', 'Configuring site {}'.format(site))
    config = hookenv.config()
    render(source='vhost.conf',
           target='/etc/nginx/sites-enabled/{}'.format(site),
           context={
               'application_address': hookenv.unit_private_ip(),
               'application_port': context['proxy_port'],
               'location': context['location'],
               'hostname': context['servername'],
               'port': config['nginx-port']
           })


# REACTORS --------------------------------------------------------------------
@hook('install')
def install():
    """ Install nginx
    """
    hookenv.status_set('maintenance', 'Installing NGINX')

    # Install nginx-full
    if is_state('nginx.available'):
        return

    apt_install(['nginx-full'])

    set_state('nginx.available')


@hook('config-changed')
def config_changed():
    config = hookenv.config()

    if not is_state('nginx.available') or not config.changed('port'):
        return

    hookenv.log('Updating NGINX vhosts', 'info')
    process_sites()

    if is_state('nginx.started'):
        hookenv.close_port(config.previous('port'))
        host.service_reload('nginx')
        hookenv.open_port(config['port'])
    hookenv.status_set('maintenance', '')


@when('nginx.start')
@when_not('nginx.started')
def start_nginx():
    host.service_start('nginx')
    set_state('nginx.started')


@when('nginx.available', 'nginx.started')
@when_not('nginx.start')
def stop_nginx():
    host.service_stop('nginx')
    remove_state('nginx.started')


@when('website.available')
def configure_website(website):
    config = hookenv.config()
    website.configure(config['nginx-port'])
