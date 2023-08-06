# mypy-boto3-iotthingsgraph

Mypy-friendly auto-generated type annotations for `boto3 iotthingsgraph 1.10.28` service.
More information can be found [here](https://github.com/vemel/mypy_boto3).

- [mypy-boto3-iotthingsgraph](#mypy-boto3-iotthingsgraph)
  - [How to use](#how-to-use)
    - [Type checking](#type-checking)
    - [Code auto-complete](#code-auto-complete)
  - [How it works](#how-it-works)

## How to use

### Type checking

Make sure you have [mypy](https://github.com/python/mypy) installed ans activated in your IDE.

Install `boto3-stubs` for `iotthingsgraph` service.

```bash
pip install boto3-stubs[mypy-boto3-iotthingsgraph]
```

Use `boto3` as usual in your project and enjoy type checking.

```python
import boto3

# Use this client as usual, now mypy can check if your code is valid.
client = boto3.client("iotthingsgraph")

# works for session as well
session = boto3.session.Session(region="us-west-1")
session_client = session.client("iotthingsgraph")

```

### Code auto-complete

Not a single Python IDE supports `Literal` type overloads yet (but in `VSCode` support is just around the corner).
Meanwhile, to have a nice auto-complete you can explicitly set types to help your IDE to get methods, arguments etc.

```python
import boto3
from mypy_boto3.iotthingsgraph import Client

from mypy_boto3.iotthingsgraph.paginator import GetFlowTemplateRevisionsPaginator

# now you have auto-complete for methods, arguments and even return types
client: Client = boto3.client("iotthingsgraph")

# even for paginators
get_flow_template_revisions_paginator: GetFlowTemplateRevisionsPaginator = client.get_paginator("get_flow_template_revisions")
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