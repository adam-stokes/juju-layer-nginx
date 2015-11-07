import sys
import toml

sys.path.insert(0, 'lib')  # noqa
from nginxlib import (_validate_config,
                      _validate_interface)

SITES = "tests/fixtures/sites.toml"

with open(SITES) as fp:
    site_conf = toml.loads(fp.read())


class TestValidateConfig:
    def test_valid_options(self):
        """ Test that valid options are True
        """
        valid_site = site_conf['correct']
        assert _validate_config(valid_site.keys()) is True

    def test_invalid_options(self):
        """ Test improper config
        """
        invalid_site = site_conf['incorrect']
        assert _validate_config(invalid_site.keys()) is False

    def test_valid_interface(self):
        """ Test valid interface
        """
        valid_iface = site_conf['correct']
        assert _validate_interface(valid_iface['interface']) is True

    def test_invalid_interface(self):
        """ Test invalid interface
        """
        invalid_site = site_conf['incorrect-interface']
        assert _validate_interface(invalid_site['interface']) is False
