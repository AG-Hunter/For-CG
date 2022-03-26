# For-CG

## Data export tools

## To use with Gate.io

You will need two files:
  - api_keys.py
  - gate_export_balances.py

Place both python files in the same directory. The CSV output will also appear in this directory.

You will need a read only API key with access to your spot account on Gate.io. Input these keys into the api_keys.py file then run export_balances.py. The file will take about 30s to run depending on how many pairs you are downloading data for. You will receive a message when the program is complete. 

## To use with Kucoin

As above except with these two files:
  - api_keys.py
  - kucoin_export_balances.py

