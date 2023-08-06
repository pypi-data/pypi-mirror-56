# PyUSDforex - Fiat to USD

## Project Description
PyUSDforex is a python package to convert foreign currencies into US dollars. It uses the free API key from openexchangerates.org to get over 200 currencies. PyUSDforex allows you to perform as many currency conversions as you wish by caching the hourly exchange rates from openexchange.org in a python shelve.

## Installation
install from https://pypi.org/project/pyUSDforex/

pip install pyUSDforex

## Usage
```python
import pyUSDforex

pyUSDforex.convert(100, 'EUR', 'Your APP_ID')
```

Get your app_id from https://openexchangerates.org/signup/free

## Notes
We welcome your feedback and support, raise github ticket if you want to report a bug. Need new features? Contact us on github

## Changelog

### 1.2
 - raise an exception when the currency code cannot be found 

### 1.1
 - make threading safe with lock object

### 1.0
 - Init release
