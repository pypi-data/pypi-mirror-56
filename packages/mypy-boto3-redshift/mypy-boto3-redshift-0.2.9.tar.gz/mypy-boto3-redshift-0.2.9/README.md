# mypy-boto3-redshift

Mypy-friendly auto-generated type annotations for `boto3 redshift 1.10.28` service.
More information can be found [here](https://github.com/vemel/mypy_boto3).

- [mypy-boto3-redshift](#mypy-boto3-redshift)
  - [How to use](#how-to-use)
    - [Type checking](#type-checking)
    - [Code auto-complete](#code-auto-complete)
  - [How it works](#how-it-works)

## How to use

### Type checking

Make sure you have [mypy](https://github.com/python/mypy) installed ans activated in your IDE.

Install `boto3-stubs` for `redshift` service.

```bash
pip install boto3-stubs[mypy-boto3-redshift]
```

Use `boto3` as usual in your project and enjoy type checking.

```python
import boto3

# Use this client as usual, now mypy can check if your code is valid.
client = boto3.client("redshift")

# works for session as well
session = boto3.session.Session(region="us-west-1")
session_client = session.client("redshift")

```

### Code auto-complete

Not a single Python IDE supports `Literal` type overloads yet (but in `VSCode` support is just around the corner).
Meanwhile, to have a nice auto-complete you can explicitly set types to help your IDE to get methods, arguments etc.

```python
import boto3
from mypy_boto3.redshift import Client

from mypy_boto3.redshift.paginator import DescribeClusterDbRevisionsPaginator
from mypy_boto3.redshift.waiter import ClusterAvailableWaiter

# now you have auto-complete for methods, arguments and even return types
client: Client = boto3.client("redshift")

# even for paginators
describe_cluster_db_revisions_paginator: DescribeClusterDbRevisionsPaginator = client.get_paginator("describe_cluster_db_revisions")

# and waiters are also annotated
cluster_available_waiter: ClusterAvailableWaiter = client.get_waiter("cluster_available")
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