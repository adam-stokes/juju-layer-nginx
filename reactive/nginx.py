from charms.reactive import (
    when,
    when_not,
    set_state,
    remove_state,
    is_state,
    main,
    hook
)

from charmhelpers.core import hookenv, host
from charmhelpers.fetch import apt_install


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

    # Perform our application install
    set_state('nginx.available')


@hook('config-changed')
def config_changed():
    config = hookenv.config()
    if not is_state('nginx.available') or not config.changed('nginx-port'):
        return

    if is_state('nginx.started'):
        hookenv.close_port(config.previous('port'))
        host.service_reload('nginx')
        hookenv.open_port(config['port'])
    hookenv.status_set('maintenance', '')


# REACTORS --------------------------------------------------------------------
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
def configure_proxy(website):
    config = hookenv.config()
    website.configure(config['port'])


if __name__ == "__main__":
    main()
