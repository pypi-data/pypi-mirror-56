# elasticConstants

Simple Python library/function to convert elastic constants.

## Usage

```python
import elasticConstants

print(elasticConstants.convert(E=1.0, nu=0.3))
```

## Installation

## Using conda

```bash
conda install -c conda-forge elasticConstants
```

## Using PyPi

```bash
pip install elasticConstants
```

## From source

```bash
# Download elasticConstants
git checkout https://github.com/tdegeus/elasticConstants.git
cd elasticConstants

# Install
python -m pip install .
```

## Develop

After completing an update, change the version number and upload to GitHub and then to PyPi using

```bash
python setup.py bdist_wheel --universal
twine upload dist/*
```
