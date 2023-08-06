The goal of this module is to automate creation JSON APIs consistent with [Google JSON API Style Guide](https://google.github.io/styleguide/jsoncstyleguide.xml).

## Installation

```bash
pip install google_json_style
```

To use sanic integration it's assumed that you have sanic installed:
```bash
pip install sanic
```

## Usage
```python
from sanic import Sanic
from google_json_style import set_api_version
from google_json_style.sanic import json_resp

set_api_version('0.1.0')
app = Sanic()

@app.route('/')
async def handle_request(request):
    return json_resp({'test_field': 'test_value'})
```


## License 

This code is distributed under terms of MIT License.
