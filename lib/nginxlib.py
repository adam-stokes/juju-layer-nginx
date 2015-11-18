from charmhelpers.core.templating import render
from charmhelpers.core import hookenv
from charmhelpers.core import host
from charmhelpers.fetch import apt_install

import toml
import sys


def load_site():
    try:
        with open('site.toml') as fp:
            conf = toml.loads(fp.read())
        return conf
    except IOError:
        hookenv.status_set('blocked',
                           'No site.toml found, not configuring vhost')
        sys.exit(0)


def get_app_path():
    site = load_site()
    if 'app_path' in site:
        return site['app_path']
    return '/srv/app'


def configure_site(site, template, **kwargs):
    """ configures vhost

    Arguments:
    site: Site name
    template: template to process in templates/<template.conf>
    **kwargs: additional dict items to append to template variables exposed
              through the site.toml
    """
    hookenv.status_set('maintenance', 'Configuring site {}'.format(site))

    config = hookenv.config()
    context = load_site()
    context['host'] = config['host']
    context['port'] = config['port']
    context.update(**kwargs)
    render(source=template,
           target='/etc/nginx/sites-enabled/{}'.format(site),
           context=context)
    hookenv.log('Wrote vhost config {} to {}'.format(context, template),
                'info')

    if 'packages' in context:
        install_extra_packages(context['packages'])

    host.service_reload('nginx')


def install_extra_packages(pkgs):
    """ Installs additional packages defined
    """
    hookenv.status_set('maintenance',
                       'Installing additional packages {}'.format(pkgs))
    if isinstance(pkgs, str):
        pkgs = [pkgs]

    apt_install(pkgs)
