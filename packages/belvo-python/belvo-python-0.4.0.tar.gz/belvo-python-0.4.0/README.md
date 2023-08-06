<h1 align="center">Belvo Python SDK</h1>
<p align="center">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/belvo-python?style=for-the-badge">
    <img alt="Travis (.com)" src="https://img.shields.io/travis/com/belvo-finance/belvo-python?style=for-the-badge">
    <img alt="Coveralls github" src="https://img.shields.io/coveralls/github/belvo-finance/belvo-python?style=for-the-badge">
</p>
<p align="center"><a href="https://developers.belvo.co">Developers portal</a> | <a href="https://belvo-finance.github.io/belvo-python">Documentation</a></p>

## :clipboard: Requirements
* Python 3.6+

## :rocket: Getting started

Install using `pip`:
```
$ pip install belvo-python
```

## Example
```python

from pprint import pprint

from belvo.client import Client

# Login to Belvo API
client = Client("my-secret-key-id", "my-secret-key", "https://api.belvo.co")

# Register a link 
link = client.Links.create(
    institution="banamex",
    username="johndoe",
    password="supersecret"
)

# Get all accounts
client.Accounts.create(link["id"])

# Pretty print all checking accounts
for account in client.Accounts.list(type="checking"):
    pprint(account)
```

## :busts_in_silhouette: Contributing
**Anyone** can do something to make `belvo-python` better, so contributors are always welcome!
For more details about contributing to this project, please take a look to our [guidelines](CONTRIBUTING.md). 