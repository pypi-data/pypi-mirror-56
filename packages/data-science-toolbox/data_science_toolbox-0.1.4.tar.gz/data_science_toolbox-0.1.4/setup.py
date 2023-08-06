# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['data_science_toolbox',
 'data_science_toolbox.data_checks',
 'data_science_toolbox.etl',
 'data_science_toolbox.io',
 'data_science_toolbox.ml',
 'data_science_toolbox.pandas',
 'data_science_toolbox.text']

package_data = \
{'': ['*'],
 'data_science_toolbox': ['gists/*', 'gists/io/*', 'gists/ml/*'],
 'data_science_toolbox.data_checks': ['dataframes/*', 'dictionary/*'],
 'data_science_toolbox.etl': ['custom_transformers/*',
                              'custom_transformers/DF/*'],
 'data_science_toolbox.ml': ['feature_engineering/*',
                             'feature_list/*',
                             'scoring/*',
                             'scoring/.ipynb_checkpoints/*'],
 'data_science_toolbox.pandas': ['analysis/*',
                                 'analysis/.ipynb_checkpoints/*',
                                 'cleaning/*',
                                 'cleaning/.ipynb_checkpoints/*',
                                 'datetime/*',
                                 'datetime/.ipynb_checkpoints/*',
                                 'engineering/*',
                                 'engineering/.ipynb_checkpoints/*',
                                 'optimization/*',
                                 'optimization/.ipynb_checkpoints/*',
                                 'profiling/*',
                                 'text/*',
                                 'text/.ipynb_checkpoints/*'],
 'data_science_toolbox.text': ['.ipynb_checkpoints/*']}

install_requires = \
['click>=7.0,<8.0',
 'dask>=2.8.1,<3.0.0',
 'matplotlib>=3.0.2,<4.0.0',
 'numpy>=1.15.2,<2.0.0',
 'openpyxl>=3.0.1,<4.0.0',
 'pandas>=0.25.3,<0.26.0',
 'pandas_profiling>=2.3.0,<3.0.0',
 'papermill>=1.2.1,<2.0.0',
 'pytest>=5.2.4,<6.0.0',
 'scikit_learn>=0.21.0,<0.22.0',
 'scipy>=1.1.0,<2.0.0',
 'seaborn>=0.9.0,<0.10.0',
 'spacy>=2.2.3,<3.0.0',
 'tables>=3.6.1,<4.0.0',
 'textacy>=0.5.0,<0.6.0',
 'textblob>=0.15.3,<0.16.0',
 'vaderSentiment>=3.2.1,<4.0.0',
 'xlrd>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'data-science-toolbox',
    'version': '0.1.4',
    'description': 'Various code to aid in data science projects for tasks involving data cleaning, ETL, EDA, NLP, viz, feature engineering, feature selection, model validation, etc.',
    'long_description': '# data_science_toolbox\n\n=====================\n\nVarious code to aid in data science projects for tasks involving data cleaning,\nETL, EDA, NLP, viz, feature engineering, feature selection, model training and validation etc.\n\n## Installation\n\n### Using pip\n\nYou can install using the pip package manager by running\n\n    pip install data-science-toolbox\n\n## Project Organization\n\n---------------------\n    ├── README.md              \n    ├── data_science_toolbox   <- Project source code\n    │   │\n    │   ├── gists              <- Code gists with commonly used code (change to root\n    │   │                         directory, connect to database, profile data, etc)\n    │   ├── data_checks        <- Code for data checks and assertions\n    │   ├── io                 <- Code for input/output utilities\n    │   ├── etl                <- For building reproducible ETL pipelines, including data\n    │   │                         checks and transformers\n    │   ├── ml                 <- Machine Learning utility code (feature engineering, etc) \n    │   ├── pandas             <- Pandas related utility code\n    │   │   ├── analysis                  \n    │   │   ├── cleaning\n    │   │   ├── engineering\n    │   │   ├── text    \n    │   │   ├── datetime     \n    │   │   ├── optimization       \n    │   │   └── profiling   \n    │   ├── project_utils.py   <- For project specific utilities\n    │   │\n    │   ├── text               <- Code for dealing with text. Includes distributed loading of text corpus, \n    │   │                         entity statement extraction, sentiment analysis, pii removal etc.\n    │   └── __init__.py        <- Makes data_science_toolbox a Python module               \n    ├── tests                  <- Pytest unit tests \n    ├── dist                   <- tars and whls of version builds\n    ├── LICENSE\n    ├── poetry.lock\n    └── pyproject.toml ',
    'author': 'safurrier',
    'author_email': 'safurrier@gmail.com',
    'url': 'https://github.com/safurrier/data_science_toolbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
