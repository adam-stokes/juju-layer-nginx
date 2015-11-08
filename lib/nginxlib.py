from charmhelpers.core.templating import render
from charmhelpers.core import hookenv
import toml
import sys
from shell import shell


REQUIRED_KEYS = ['server_name',
                 'interface',
                 'app-path']

OPTIONAL_KEYS = ['packages']

# Supported interfaces,
# reverseproxy - for nodejs, ruby like apps that just need a simple proxy
# phpfpm - sites like wordpress that need php fastcgi support
INTERFACES = ['reverseproxy',
              'phpfpm']


def _validate_config(keys):
    if set(keys) != set(REQUIRED_KEYS):
        return False
    return True


def _validate_interface(interface):
    if interface not in INTERFACES:
        return False
    return True


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

            if not _validate_config(sites[site].keys()):
                hookenv.status_set(
                    'blocked',
                    'Not all required config '
                    'items met {} != {}'.format(sites[site].keys(),
                                                REQUIRED_KEYS))
                sys.exit(0)

            if not _validate_interface(sites[site]['interface']):
                hookenv.status_set(
                    'blocked',
                    'Unsupported interface {}, '
                    'acceptable ones: {} '.format(sites[site]['interface'],
                                                  INTERFACES))
                sys.exit(0)

            configure_site(site, sites[site])
            if 'packages' in sites[site]:
                install_extra_packages(sites[site]['packages'])


def configure_site(site, context):
    """ configures vhost
    """
    hookenv.status_set('maintenance', 'Configuring site {}'.format(site))
    config = hookenv.config()
    context['host'] = config['host']
    context['port'] = config['port']
    render(source='vhost.conf',
           target='/etc/nginx/sites-enabled/{}'.format(site),
           context=context)


def install_extra_packages(pkgs):
    """ Installs additional packages defined
    """
    if isinstance(pkgs, str):
        pkgs = [pkgs]

    sh = shell('apt-get install -qy {}'.format(" ".join(pkgs)))
    if sh.code > 0:
        hookenv.status_set(
            'blocked',
            'Unable to install packages: {}'.format(sh.errors()))
        sys.exit(0)
