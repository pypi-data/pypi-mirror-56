# 🧙‍♀️ Prophetess Salesforce Plugin

[Prophetess](https://github.com/vapor-ware/prophetess) plugin for extracting data from [Salesforce](https://salesforce.com)

# 🚀 Installation

```sh
pip install prophetess-salesforce
```

# 🔧 Configuration

[SalesforceExtractor](/prophetess_salesforce/extractor.py#L7) takes several required configuration options. The full configuration break down is presented below:

```yaml
key: |-
  -----BEGIN PRIVATE KEY-----
  ...
  -----END PRIVATE KEY-----
client_id: "yourclient.idfromsfdc"
user: marco@vapor.io
instance: na02
query: |-
  SELECT Id, Name
  FROM Account
  WHERE Type IN ('Customer', 'Partner')
```

## Extractor

| Key       | Values     | Description  |
| ----------| ---------- | ------------ |
| user      | string     | Salesforce user which the `key` is assigned to |
| key       | string     | User private key for signing requests to SFDC API |
| client_id | string     | SFDC API Client ID  |
| instance  | string     | Which SFDC instance to connect to |
| query     | string     | The Salesforce Object Query Languge (SOQL) for record extraction |

# 🧰 Development

Please fork this project and create a new branch to submit any changes. While not required, it's highly recommended to first create an issue to propose the change you wish to make. Keep pull requests well scoped to one change / feature.

This project uses `tox` + `pytest` to unit test and lint code. Use the following commands to validate your changes aren't breaking:

```sh
tox --cov-report term-missing
tox -e lint
```

# 🎉 Special Thanks

❤️ [Kyler Burke](https://github.com/KylerBurke) original author of `SFClient`  
❤️ [Charles Butler](https://github.com/lazypower)  
