# Coverage

The bundled coverage table classifies known Bot API methods as verified,
inferred, or unverified. Unknown method names return `UNVERIFIED`.

```python
from wizardgram import status

print(status("sendMessage"))
```