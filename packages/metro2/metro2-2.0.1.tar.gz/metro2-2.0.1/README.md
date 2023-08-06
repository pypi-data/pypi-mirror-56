# Metro2

Creates files in Metro 2 format for reporting to credit agencies

## Dependencies and Installation

Metro2 can be installed from PyPI using pip

```
$ pip install metro2
```

This is using the ruby library metro_2, run the following command to install this
```
$ gem install metro2_format
```

## Usage
 use the following code to generate the report in metro2 format

```
from metro2 import Metro2

sample = Metro2(customer_account_number = '1')
sample.get_metro2_report()
```