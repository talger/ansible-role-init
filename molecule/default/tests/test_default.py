import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('pkg', [
  'python',
  'sudo'
])
def test_pkg(host, pkg):
    package = host.package(pkg)

    assert package.is_installed


def test_ansible_user_exists(host):
    user = host.user('ansible')

    assert user.uid


@pytest.mark.parametrize('path', [
  '/home/ansible',
  '/home/ansible/.ssh',
  '/home/ansible/.ssh/authorized_keys'
])
def test_ansible_paths_exists(host, path):

    assert host.file(path).exists


def test_ansible_paths_permissions(host):

    assert host.file('/home/ansible').mode == 0o700
    assert host.file('/home/ansible').user == 'ansible'
    assert host.file('/home/ansible/.ssh/authorized_keys').mode == 0o400
