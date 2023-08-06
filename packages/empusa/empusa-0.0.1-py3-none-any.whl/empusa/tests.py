import click.testing
import pytest
from unittest.mock import MagicMock

import empusa


@pytest.fixture(name='mock_client')
def fixture_mock_client(monkeypatch):
    client = empusa.EtcdClient('/foo')

    mock_etcd_client = MagicMock()
    monkeypatch.setattr(empusa.EtcdClient, '_client', mock_etcd_client)

    return client, mock_etcd_client


@pytest.fixture(name='cli_runner')
def fixture_cli_runner():
    return click.testing.CliRunner()


@pytest.fixture(name='cmd_options')
def fixture_cmd_options():
    return ['--etcd-endpoint=foo:123', '--tree-root=/foo']


def test_sanity() -> None:
    pass


@pytest.mark.parametrize('specs, expected', [
    ('foo:1234', [('foo', 1234)]),
    (['foo:1234'], [('foo', 1234)]),
    (['foo:1234', 'bar:567'], [('foo', 1234), ('bar', 567)]),
    (['foo:1234,bar:567'], [('foo', 1234), ('bar', 567)]),
])
def test_parse_endpoints(specs, expected):
    assert empusa.parse_endpoints(specs) == expected


def test_register_entity(mock_client):
    client, mock_etcd_client = mock_client

    client.register_entity('dummy type', 'dummy subtype', 'dummy name', 'dummy location')

    mock_etcd_client.write.assert_called_once_with(
        '/foo/dummy type/dummy subtype/dummy name',
        'dummy location',
        ttl=None
    )


def test_register_entity_ttl(mock_client):
    client, mock_etcd_client = mock_client

    client.register_entity('dummy type', 'dummy subtype', 'dummy name', 'dummy location', ttl=79)

    mock_etcd_client.write.assert_called_once_with(
        '/foo/dummy type/dummy subtype/dummy name',
        'dummy location',
        ttl=79
    )


def test_unregister_entity(mock_client):
    client, mock_etcd_client = mock_client

    client.unregister_entity('dummy type', 'dummy subtype', 'dummy name')

    mock_etcd_client.delete.assert_called_once_with(
        '/foo/dummy type/dummy subtype/dummy name'
    )


def test_cmd(cli_runner, cmd_options):
    result = cli_runner.invoke(empusa.cmd_root)

    assert result.exit_code == 0

    result = cli_runner.invoke(empusa.cmd_root, ['service'])

    assert result.exit_code == 2
    assert 'Error: Missing option "--etcd-endpoint".' in result.output

    result = cli_runner.invoke(empusa.cmd_root, [cmd_options[0], 'service'])

    assert result.exit_code == 2
    assert 'Error: Missing option "--tree-root".' in result.output

    result = cli_runner.invoke(empusa.cmd_root, [cmd_options[0], cmd_options[1], 'service'])

    assert result.exit_code == 0


def test_cmd_service(cli_runner, cmd_options):
    result = cli_runner.invoke(empusa.cmd_root, cmd_options + ['service'])

    assert result.exit_code == 0


def test_cmd_service_register(cli_runner, cmd_options, mock_client, monkeypatch):
    client, mock_etcd_client = mock_client
    monkeypatch.setattr(empusa.EtcdClient, 'register_entity', MagicMock())

    result = cli_runner.invoke(empusa.cmd_root, cmd_options + [
        'service',
        'register',
        '--service-type', 'dummy-type',
        '--service-name', 'dummy-name',
        '--service-location', 'dummy-location',
        '--ttl', '79'
    ])

    assert result.exit_code == 0
    client.register_entity.assert_called_once_with('service', 'dummy-type', 'dummy-name', 'dummy-location', ttl=79)


def test_cmd_service_unregister(cli_runner, cmd_options, mock_client, monkeypatch):
    client, mock_etcd_client = mock_client
    monkeypatch.setattr(empusa.EtcdClient, 'unregister_entity', MagicMock())

    result = cli_runner.invoke(empusa.cmd_root, cmd_options + [
        'service',
        'unregister',
        '--service-type', 'dummy-type',
        '--service-name', 'dummy-name'
    ])

    assert result.exit_code == 0
    client.unregister_entity.assert_called_once_with('service', 'dummy-type', 'dummy-name')
