# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['airflow_indexima']

package_data = \
{'': ['*']}

install_requires = \
['PyHive==0.6.1',
 'apache-airflow==1.10.2',
 'gitpython>=2.1.0,<2.2.0',
 'thrift-sasl',
 'thrift==0.13.0']

setup_kwargs = {
    'name': 'airflow-indexima',
    'version': '1.0.1',
    'description': 'Indexima Airflow integration',
    'long_description': "# airflow-indexima\n\n\n[![Unix Build Status](https://img.shields.io/travis/geronimo-iia/airflow-indexima/master.svg?label=unix)](https://travis-ci.org/geronimo-iia/airflow-indexima)\n[![PyPI Version](https://img.shields.io/pypi/v/airflow-indexima.svg)](https://pypi.org/project/airflow-indexima)\n[![PyPI License](https://img.shields.io/pypi/l/airflow-indexima.svg)](https://pypi.org/project/airflow-indexima)\n\nVersions following [Semantic Versioning](https://semver.org/)\n\n## Overview\n\n[Indexima](https://indexima.com/) [Airflow](https://airflow.apache.org/) integration based on pyhive.\n\n\n## Setup\n\n### Requirements\n\n* Python 3.6+\n\n### Installation\n\nInstall this library directly into an activated virtual environment:\n\n```text\n$ pip install airflow-indexima\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```text\n$ poetry add airflow-indexima\n```\n\n## Usage\n\nAfter installation, the package can imported:\n\n```text\n$ python\n>>> import airflow_indexima\n>>> airflow_indexima.__version__\n```\n\nSee [Api documentation](https://geronimo-iia.github.io/airflow-indexima/api/)\n\n\n## Example\n\n### a simple query\n\n```python\nfrom airflow_indexima import IndeximaQueryRunnerOperator\n\n...\n\nwith dag:\n    ...\n    op = IndeximaQueryRunnerOperator(\n        task_id = 'my-task-id',\n        sql_query= 'DELETE FROM Client WHERE GRPD = 1',\n        indexima_conn_id='my-indexima-connection'\n    )\n    ...\n```\n\n\n### a load into indexima\n\n```python\nfrom airflow_indexima import IndeximaLoadDataOperator\n\n...\n\nwith dag:\n    ...\n    op = IndeximaLoadDataOperator(\n        task_id = 'my-task-id',\n        indexima_conn_id='my-indexima-connection',\n        target_table='Client',\n        source_select_query='select * from dsi.client',\n        truncate=True,\n        load_path_uri='jdbc:redshift://my-private-instance.com:5439/db_client?ssl=true&user=airflow-user&password=XXXXXXXX'\n    )\n    ...\n\n```\n\n## License\n\n[The MIT License (MIT)](https://geronimo-iia.github.io/airflow-indexima/license)\n\n\n## Contributing\n\nSee [Contributing](https://geronimo-iia.github.io/airflow-indexima/contributing)\n\n",
    'author': 'Jerome Guibert',
    'author_email': 'jguibert@gmail.com',
    'url': 'https://pypi.org/project/airflow_indexima',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
