from charms.reactive import (
    when,
    set_state,
    remove_state,
    is_state,
    main,
    hook
)

from charmhelpers.core import hookenv, host
from charmhelpers.fetch import apt_install
from charmhelpers.core.templating import render
import toml


# HELPERS ---------------------------------------------------------------------
def configure_site(site, context):
    """ configures vhost
    """
    hookenv.status_set('maintenance', 'Configuring site {}'.format(site))
    config = hookenv.config()
    render(source='vhost.conf',
           target='/etc/nginx/sites-enabled/{}'.format(site),
           context={
               'application_address': hook.unit_private_ip(),
               'application_port': context['proxy_port'],
               'location': context['location'],
               'hostname': context['servername'],
               'port': config['nginx-port']
           })


# HOOKS -----------------------------------------------------------------------
@hook('install')
def install():
    """ Install dependencies for application
    """
    hookenv.status_set('maintenance', 'Installing NGINX')
    # Install nginx-full
    if is_state('nginx.available'):
        return

    apt_install(['nginx-full'])
    with open('sites.toml') as fp:
        sites = toml.loads(fp.read())

    for site in sites.keys():
        configure_site(site, sites[site])

    # Perform our application install
    set_state('nginx.available')


@hook('config-changed')
def config_changed():
    config = hookenv.config()
    if not is_state('nginx.available') or not config.changed('nginx-port'):
        return

    with open('sites.toml') as fp:
        sites = toml.loads(fp.read())

    for site in sites.keys():
        configure_site(site, sites[site])

    if is_state('nginx.started'):
        hookenv.close_port(config.previous('port'))
        host.service_reload('nginx')
        hookenv.open_port(config['port'])
    hookenv.status_set('maintenance', '')


# REACTORS --------------------------------------------------------------------
@when('nginx.restart')
def restart_nginx():
    remove_state('nginx.started')
    host.service_restart('nginx')
    set_state('nginx.started')


@when('website.available')
def configure_website(website):
    config = hookenv.config()
    website.configure(config['nginx-port'])

if __name__ == "__main__":
    main()
