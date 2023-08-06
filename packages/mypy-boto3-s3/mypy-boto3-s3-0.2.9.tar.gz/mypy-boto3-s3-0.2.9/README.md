# mypy-boto3-s3

Mypy-friendly auto-generated type annotations for `boto3 s3 1.10.28` service.
More information can be found [here](https://github.com/vemel/mypy_boto3).

- [mypy-boto3-s3](#mypy-boto3-s3)
  - [How to use](#how-to-use)
    - [Type checking](#type-checking)
    - [Code auto-complete](#code-auto-complete)
  - [How it works](#how-it-works)

## How to use

### Type checking

Make sure you have [mypy](https://github.com/python/mypy) installed ans activated in your IDE.

Install `boto3-stubs` for `s3` service.

```bash
pip install boto3-stubs[mypy-boto3-s3]
```

Use `boto3` as usual in your project and enjoy type checking.

```python
import boto3

# Use this client as usual, now mypy can check if your code is valid.
client = boto3.client("s3")

# works for session as well
session = boto3.session.Session(region="us-west-1")
session_client = session.client("s3")

# Do you prefer resource approach? We've got you covered!
resource = boto3.resource("s3")
```

### Code auto-complete

Not a single Python IDE supports `Literal` type overloads yet (but in `VSCode` support is just around the corner).
Meanwhile, to have a nice auto-complete you can explicitly set types to help your IDE to get methods, arguments etc.

```python
import boto3
from mypy_boto3.s3 import Client
from mypy_boto3.s3 import ServiceResource

from mypy_boto3.s3.paginator import ListMultipartUploadsPaginator
from mypy_boto3.s3.waiter import BucketExistsWaiter

# now you have auto-complete for methods, arguments and even return types
client: Client = boto3.client("s3")

# same for resource
resource: ServiceResource = boto3.resource("s3")

# even for paginators
list_multipart_uploads_paginator: ListMultipartUploadsPaginator = client.get_paginator("list_multipart_uploads")

# and waiters are also annotated
bucket_exists_waiter: BucketExistsWaiter = client.get_waiter("bucket_exists")
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