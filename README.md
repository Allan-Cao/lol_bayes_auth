# lol_bayes_auth
Simple authentication package for the Bayes Esports API

## Install
```
pip install lol_bayes_auth
```

If you wish to install the latest development version:
```
pip install -U git+https://github.com/Allan-Cao/lol_bayes_auth
```

## Example Usage
````python
from lol_bayes_auth import BayesAuth

authv1 = BayesAuth('v1username', 'v1password', True)
authv2 = BayesAuth('v2username', 'v2password')

v1token = authv1.get_token()
v2token = authv2.get_token()
````
