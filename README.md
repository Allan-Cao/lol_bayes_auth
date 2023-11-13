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

### Get a Bayes Esports authentication token using a v1/v2 login

````python
from lol_bayes_auth import BayesAuth

authv1 = BayesAuth('v1username', 'v1password', True)
authv2 = BayesAuth('v2username', 'v2password')

v1token = authv1.get_token()
v2token = authv2.get_token()
````

### Get a formatted header to authenticate with the Bayes Esports API

````python
auth = BayesAuth('username', 'password')
header = auth.get_headers()

# Example usage with the requests library
requests.get(
    f'https://lolesports-api.bayesesports.com/v2/games',
    headers=auth.get_headers(),
    params=parameters,
).json()
````