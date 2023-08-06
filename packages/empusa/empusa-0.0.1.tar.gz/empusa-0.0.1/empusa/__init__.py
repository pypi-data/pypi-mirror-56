import argparse
import json
import logging
import os
import time

import click
import etcd
import tabulate

from typing import Any, Dict, List, Optional, Tuple, Union


DEFAULT_ETCD_PROTOCOL = 'http'


def parse_endpoints(endpoint_specs: Union[str, List[str]]) -> List[Tuple[str, int]]:
    endpoints: List[Tuple[str, int]] = []

    if isinstance(endpoint_specs, str):
        endpoint_specs = [endpoint_specs]

    for item in endpoint_specs:
        for endpoint in item.split(','):
            try:
                host, port = endpoint.split(':')

            except ValueError:
                raise Exception('Endpoint "{}" is not in HOST:PORT format'.format(endpoint))

            endpoints += [
                (host.strip(), int(port.strip()))
            ]

    return endpoints


class EtcdClient:
    def __init__(
        self,
        tree: str,
        client_args: Optional[Any] = None,
        client_kwargs: Optional[Dict[str, Any]] = None,
        ttl: Optional[int] = None
    ) -> None:
        self._tree = tree
        self._ttl = ttl

        self._client_args = client_args or tuple()
        self._client_kwargs = client_kwargs or dict()

    @property
    def _client(self) -> etcd.Client:
        return etcd.Client(*self._client_args, **self._client_kwargs)

    def list_entities(
        self,
        entity_type: str,
        entity_subtype: str
    ) -> List[etcd.EtcdResult]:
        directory = self._client.get('{self._tree}/{entity_type}/{entity_subtype}'.format(**locals()))

        return [r for r in directory.children]

    def register_entity(
        self,
        entity_type: str,
        entity_subtype: str,
        name: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> None:
        self._client.write(
            '{self._tree}/{entity_type}/{entity_subtype}/{name}'.format(**locals()),
            value,
            ttl=ttl or self._ttl
        )

        logging.getLogger().info('{entity_type} {entity_subtype} {name} registered'.format(**locals()))

    def unregister_entity(
        self,
        entity_type: str,
        entity_subtype: str,
        name: str
    ) -> None:
        self._client.delete(
            '{self._tree}/{entity_type}/{entity_subtype}/{name}'.format(**locals()),
        )

        logging.getLogger().info('{entity_type} {entity_subtype} {name} unregistered'.format(**locals()))


@click.group()
@click.pass_context
@click.option(
    '--etcd-endpoint',
    type=str, envvar='EMPUSA_ETCD_ENDPOINT',
    required=True, metavar='HOST:PORT', multiple=True
)
@click.option(
    '--etcd-protocol',
    type=str, envvar='EMPUSA_ETCD_PROTOCOL',
    default=DEFAULT_ETCD_PROTOCOL
)
@click.option(
    '--tree-root',
    type=str, envvar='EMPUSA_TREE_ROOT',
    required=True
)
def cmd_root(
    ctx: Any,
    etcd_endpoint: List[str],
    etcd_protocol: str,
    tree_root: str
) -> None:
    ctx.ensure_object(argparse.Namespace)
    cfg = ctx.obj

    endpoints = parse_endpoints(etcd_endpoint)

    if not endpoints:
        raise Exception('At least one etcd endpoint must be specified')

    endpoint = endpoints[0]

    cfg.client = EtcdClient(
        tree_root,
        client_kwargs={
            'host': endpoint[0],
            'port': endpoint[1],
            'protocol': etcd_protocol,
            'allow_reconnect': False
        }
    )

    print('new etcd client is {}'.format(cfg.client))


@cmd_root.group(name='service')
def cmd_service() -> None:
    pass


@cmd_service.command(name='list')
@click.option('--service-type', type=str, envvar='EMPUSA_SERVICE_TYPE', required=True)
@click.option('--format', type=click.Choice(['table', 'json']), default='table')
@click.pass_obj
def cmd_service_list(
    cfg: Any,
    service_type: str,
    format: str
) -> None:
    services = cfg.client.list_entities(
        'service',
        service_type
    )

    if format == 'table':
        table = [
            [
                'Key', 'Location', 'TTL'
            ]
        ]

        for service in services:
            table += [
                [
                    service.key,
                    service.value,
                    service.ttl
                ]
            ]

        print(tabulate.tabulate(table, tablefmt='psql', headers='firstrow'))

    elif format == 'json':
        print(json.dumps([
            {
                'key': service.key,
                'value': service.value,
                'ttl': service.ttl
            }
            for service in services
        ]))


@cmd_service.command(name='register')
@click.option('--service-type', type=str, envvar='EMPUSA_SERVICE_TYPE', required=True)
@click.option('--service-name', type=str, envvar='EMPUSA_SERVICE_NAME', required=True)
@click.option('--service-location', type=str, envvar='EMPUSA_SERVICE_LOCATION', required=True)
@click.option('--ttl', type=int, envvar='EMPUSA_SERVICE_TTL')
@click.option('--refresh-every', type=int, envvar='EMPUSA_SERVICE_REFRESH_EVERY')
@click.pass_obj
def cmd_service_register(
    cfg: Any,
    service_type: str,
    service_name: str,
    service_location: str,
    ttl: Optional[int] = None,
    refresh_every: Optional[int] = None
) -> None:
    def _register() -> None:
        cfg.client.register_entity(
            'service',
            service_type,
            service_name,
            service_location,
            ttl=ttl
        )

    if not refresh_every:
        _register()
        return

    while True:
        _register()

        time.sleep(refresh_every)


@cmd_service.command(name='unregister')
@click.option('--service-type', type=str, envvar='EMPUSA_SERVICE_TYPE', required=True)
@click.option('--service-name', type=str, envvar='EMPUSA_SERVICE_NAME', required=True)
@click.pass_obj
def cmd_service_unregister(
    cfg: Any,
    service_type: str,
    service_name: str
) -> None:
    print(cfg.client.unregister_entity)
    cfg.client.unregister_entity(
        'service',
        service_type,
        service_name
    )


def main() -> None:
    logging.basicConfig(
        level=logging._nameToLevel[os.environ.get('EMPUSA_LOGLEVEL', 'INFO').upper()]
    )

    cmd_root()


if __name__ == '__main__':
    main()
