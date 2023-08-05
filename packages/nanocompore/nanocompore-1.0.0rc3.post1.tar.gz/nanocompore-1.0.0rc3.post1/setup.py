# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['nanocompore']

package_data = \
{'': ['*'], 'nanocompore': ['models/*']}

install_requires = \
['bedparse>=0.2.2,<0.3.0',
 'matplotlib>=3.1,<4.0',
 'numpy>=1.16,<2.0',
 'pandas>=0.24.2,<0.25.0',
 'pyfaidx>=0.5.5,<0.6.0',
 'pyyaml>=5.1,<6.0',
 'scikit-learn>=0.21.2,<0.22.0',
 'scipy>=1.2,<1.3',
 'seaborn>=0.9.0,<0.10.0',
 'statsmodels>=0.9.0,<0.10.0',
 'tqdm>=4.32,<5.0']

entry_points = \
{'console_scripts': ['nanocompore = nanocompore.__main__:main']}

setup_kwargs = {
    'name': 'nanocompore',
    'version': '1.0.0rc3.post1',
    'description': 'Software package that identifies raw signal changes between two conditions from https://github.com/jts/nanopolish resquiggled dRNA-Seq data.',
    'long_description': '![Nanocompore](docs/pictures/Nanocompore_logo.png)\n\n---\n\n[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)\n[![Build Status](https://travis-ci.com/tleonardi/nanocompore.svg?token=2uTrW9fP9RypfMALjksc&branch=master)](https://travis-ci.com/tleonardi/nanocompore)\n\n---\n\n**Nanocompore identifies differences in ONT nanopore sequencing raw signal corresponding to RNA modifications by comparing 2 samples**\n\nNanocompore compares 2 ONT nanopore direct RNA sequencing datasets from different experimental conditions expected to have a significant impact on RNA modifications. It is recommended to have at least 2 replicates per condition. For example one can use a control condition with a significantly reduced number of modifications such as a cell line for which a modification writing enzyme was knocked-down or knocked-out. Alternatively, on a smaller scale transcripts of interests could be synthesized in-vitro.\n\nFull documentation is available at http://nanocompore.rna.rocks\n',
    'author': 'Tommaso Leonardi',
    'author_email': 'tom@itm6.xyz',
    'url': 'https://github.com/tleonardi/nanocompore',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
