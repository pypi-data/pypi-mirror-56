# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['empusa']

package_data = \
{'': ['*']}

install_requires = \
['click', 'python-etcd>=0.4.5,<0.5.0', 'tabulate']

entry_points = \
{'console_scripts': ['empusa = empusa:main']}

setup_kwargs = {
    'name': 'empusa',
    'version': '0.0.1',
    'description': 'Service discovery tool',
    'long_description': "= Empusa\n\n`Empusa` is a trivial tool to build a *service registry* on top of https://etcd.io/[`etcd`]. etcd alone serves as a key/value store, while `empusa` handles the keys, their structure, and values to implement the functionality of a trivial service registry.\n\n\n== Usage\n\nMain command, `empusa`, provides several subcommands, dedicated to different aspects of the service registry operation.\n\n[source,shell]\n....\n$ empusa --help\nUsage: empusa [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --etcd-endpoint HOST:PORT  [required]\n  --etcd-protocol TEXT\n  --tree-root TEXT           [required]\n  --help                     Show this message and exit.\n\nCommands:\n  service\n....\n\nTwo bits of information are always required:\n\n* etcd endpoint - host and port where `etcd` listens for client connections. Use `--etcd-endpoint` command-line option, or `EMPUSA_ETCD_ENDPOINT` environment variable.\n+\n[NOTE]\n====\nAt this moment, only the first `etcd` endpoint is used, the rest is ignored. In the future, multiple endpoints will be supported.\n====\n+\n* tree root - path in the key hierarchy under which `empusa` would store it's data. `empusa --tree-root /foo` will not read nor modify data `empusa --tree-root /bar` created. Use `--tree-root` command-line option, or `EMPUSA_TREE_ROOT` environment variable.\n\n=== Services\n\nServices come in different types, e.g. HTTP server, SMTP server, Prometheus exporter, internal directory service, and so on. Of each type, usualy multiple instances exist, each having a different name and location. `emposa` treats service types as directories to which each instance, identified by its name, is added together with its location.\n\nTo register a service, execute following command:\n\n[source,shell]\n....\n$ empusa service register --service-type type-of-service --service-name name-of-the-service-instance --service-location baz:1235\n....\n\nIt is possible to use environment variables instead of command-line options:\n\n[source,shell]\n....\n$ EMPUSA_SERVICE_TYPE=type-of-service \\\n  EMPUSA_SERVICE_NAME=name-of-the-service-instance \\\n  EMPUSA_SERVICE_LOCATION=baz:1235 \\\n  empusa service register\n....\n\nThe service can be unregistered as well:\n\n[source,shell]\n....\n$ empusa service unregister --service-type type-of-service --service-name name-of-the-service-instance\n....\n\nA service remains registered until explicitly removed. This may not be always possible, e.g. sometimes the services dies without any chance to perform teardown actions including update to the service registry. To help with this situation, a TTL can be set during registration, in seconds. After that time, the service is removed from the registry.\n\n[source,shell]\n....\n$ empusa service register ... --ttl 30\n....\n\nThe service must then periodicaly update the registry, updating its record and extending the TTL before it expires. You can either have your own scripts to perform this, or you can use `empusa`'s `--refresh-every` option:\n\n[source,shell]\n....\n$ empusa service register ... --ttl 30 --refresh-every 20\n....\n\nEvery 20 seconds, `empusa` would update the registry, setting the TTL to 30 seconds. Should the service die unexpectedly, `empusa` would not have an opportunity to prolong the TTL, and `etcd` would remove service's key.\n",
    'author': 'Milos Prchlik',
    'author_email': 'mprchlik@redhat.com',
    'url': 'https://gitlab.com/testing-farm/empusa',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
