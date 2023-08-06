[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# ayx-learn

A foundation of [scikit-learn](https://scikit-learn.org/stable/) compatible data science tools, such as Transformers, that both Alteryx Assisted Modeling and Code Fee ML Tools are built on.

## Source code organization

```
.
├── README.md
├── ayx_learn: Source code for the ayx_learn package.
│   ├── classifiers: Classifiers source code.
│   ├── regressors: Regressors source code.
│   ├── transformers: Transformer source code.
│   └── utils: Utility functions, such as validation.
├── docs: Sphinx documentation.
├── requirements-dev.txt: Requirements for development env.
├── requirements.txt: Requirements for building and running in a production env.
├── setup.py
├── tests
│   └── unit: pytest unit tests.
└── tox.ini: Ini file for tox.
```

## Code standards

`ayx-learn` follows the [Alteryx Python Code Standards](https://alteryx.quip.com/qR3kAG4OA32X/Python-Code-Standards)

## Testing

Unit tests are written using [pytest](https://docs.pytest.org/) and are located in `./tests/unit`.

[tox](https://tox.readthedocs.io/) can be used for creating a virtualenv and automatically running the pytest unit tests.

## Documentation

`ayx-learn` follows the [Alteryx Python Documentation Standards](https://alteryx.quip.com/bFgiAZThHaJv/Python-Documentation-Standards).

See [README](docs/README.md).


