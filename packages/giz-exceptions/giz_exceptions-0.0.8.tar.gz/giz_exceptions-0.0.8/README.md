It's Exception lib for Gizwits PaaS Usage.

## How to use

### requirement
`python >= 3` for now.

### install

```bash
pip install giz-exceptions
```

### config in `settings.py`
base on `Django REST Framework`

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'giz_exceptions.handler.custom_handler'
}
```

### usage

```python
from rest_framework.views import APIView
from giz_exceptions.paas import exceptions


class MyView(APIView):
    def get(self, request, *args, **kwargs):
        ...
        if not self.request.condition:
            raise exceptions.ProductKeyInvalid
            # or with detail message
            # raise exceptions.ProductKeyInvalid('This required product key')
```
