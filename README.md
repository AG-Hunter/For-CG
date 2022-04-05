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

## To use with Ascend_ex

As above except with these two files:
  - api_keys.py
  - ascendex_export_balances.py

If download does not work check the "Account Group" for your API keys. If this **is not** 4 then change the url at line 29 of the code to show the appropriate account group. 
