# mypy-boto3-dynamodb

Mypy-friendly auto-generated type annotations for `boto3 dynamodb 1.10.28` service.
More information can be found [here](https://github.com/vemel/mypy_boto3).

- [mypy-boto3-dynamodb](#mypy-boto3-dynamodb)
  - [How to use](#how-to-use)
    - [Type checking](#type-checking)
    - [Code auto-complete](#code-auto-complete)
  - [How it works](#how-it-works)

## How to use

### Type checking

Make sure you have [mypy](https://github.com/python/mypy) installed ans activated in your IDE.

Install `boto3-stubs` for `dynamodb` service.

```bash
pip install boto3-stubs[mypy-boto3-dynamodb]
```

Use `boto3` as usual in your project and enjoy type checking.

```python
import boto3

# Use this client as usual, now mypy can check if your code is valid.
client = boto3.client("dynamodb")

# works for session as well
session = boto3.session.Session(region="us-west-1")
session_client = session.client("dynamodb")

# Do you prefer resource approach? We've got you covered!
resource = boto3.resource("dynamodb")
```

### Code auto-complete

Not a single Python IDE supports `Literal` type overloads yet (but in `VSCode` support is just around the corner).
Meanwhile, to have a nice auto-complete you can explicitly set types to help your IDE to get methods, arguments etc.

```python
import boto3
from mypy_boto3.dynamodb import Client
from mypy_boto3.dynamodb import ServiceResource

from mypy_boto3.dynamodb.paginator import ListBackupsPaginator
from mypy_boto3.dynamodb.waiter import TableExistsWaiter

# now you have auto-complete for methods, arguments and even return types
client: Client = boto3.client("dynamodb")

# same for resource
resource: ServiceResource = boto3.resource("dynamodb")

# even for paginators
list_backups_paginator: ListBackupsPaginator = client.get_paginator("list_backups")

# and waiters are also annotated
table_exists_waiter: TableExistsWaiter = client.get_waiter("table_exists")
```

## How it works

Fully automated [builder](https://github.com/vemel/mypy_boto3) carefully generates
type annotations for each service, patiently waiting for `boto3` updates. It delivers
a drop-in type annotations for you and makes sure that:

- Latest version of `boto3` is used.
- Each public class and method of every `boto3` service gets valid type annotations
  extracted from latest documentation (blame `botocore` docs if types are incorrect).
- Type annotations include up-to-date documentation.
- Code is processed by [black](https://github.com/psf/black) for readability.