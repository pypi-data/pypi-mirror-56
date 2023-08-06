# mypy-boto3-elb

Mypy-friendly auto-generated type annotations for `boto3 elb 1.10.28` service.
More information can be found [here](https://github.com/vemel/mypy_boto3).

- [mypy-boto3-elb](#mypy-boto3-elb)
  - [How to use](#how-to-use)
    - [Type checking](#type-checking)
    - [Code auto-complete](#code-auto-complete)
  - [How it works](#how-it-works)

## How to use

### Type checking

Make sure you have [mypy](https://github.com/python/mypy) installed ans activated in your IDE.

Install `boto3-stubs` for `elb` service.

```bash
pip install boto3-stubs[mypy-boto3-elb]
```

Use `boto3` as usual in your project and enjoy type checking.

```python
import boto3

# Use this client as usual, now mypy can check if your code is valid.
client = boto3.client("elb")

# works for session as well
session = boto3.session.Session(region="us-west-1")
session_client = session.client("elb")

```

### Code auto-complete

Not a single Python IDE supports `Literal` type overloads yet (but in `VSCode` support is just around the corner).
Meanwhile, to have a nice auto-complete you can explicitly set types to help your IDE to get methods, arguments etc.

```python
import boto3
from mypy_boto3.elb import Client

from mypy_boto3.elb.paginator import DescribeAccountLimitsPaginator
from mypy_boto3.elb.waiter import AnyInstanceInServiceWaiter

# now you have auto-complete for methods, arguments and even return types
client: Client = boto3.client("elb")

# even for paginators
describe_account_limits_paginator: DescribeAccountLimitsPaginator = client.get_paginator("describe_account_limits")

# and waiters are also annotated
any_instance_in_service_waiter: AnyInstanceInServiceWaiter = client.get_waiter("any_instance_in_service")
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