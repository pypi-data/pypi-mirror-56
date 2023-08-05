# Py-Mortgage

To install:
```
pip install py_mortgage
```

To access Mortgage object
```
import py_mortgage as pym
new_mortgage = pym.mortgage.Mortgage(rate=.04/12,term=360,loan=400000)
```

py_mortgage has the following methods:
1. `Mortgage.get_pmt()`: Will return the payment per period

2. `Mortgage.get_pmt(period)`: Will return all payments paid up to and including period

3. `Mortgage.get_amortization_table(format='pandas_df', decimal_places=2)`:
Will return an amortization table per period. If format = 'pandas_df', it will return a Pandas DataFrame. If format = 'json', it will convert the DataFrame to a JSON object. Decimal places defaults to 2.

4. `Mortgage.get_interest_pmt(period)`: Will return the total interest paid in period

5. `Mortgage.get_principal_pmt(period)`: Will return the total principal paid down in period

6. `Mortgage.cumulative_interest_pmt(period)`: Will return all interest paid up to and including period.

7. `Mortgage.cumulative_principal_pmt(period)`: Will return all principal paid up to and including period.

8. `Mortgage.remaining_mortgage_balance(ending_period)`: Will return the remaining principal up to and including ending_period

9. `Mortgage.describe()`: Will return fields from Mortgage

`Mortgage.get_apr()` is not completed yet and will be included in next release
