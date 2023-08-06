# Blip Session

Provide a `session` `class` from `requests` module to use as a BLiP Session.

## Usage

### Constructor

```python
from blip_session import BlipSession

my_auth_key = 'Key sdasadsa='

bs = BlipSession(my_auth_key)
```

### Methods

The following methods are provided

#### send_command

| Parameters | Type   |
| ---------- | ------ |
| command    | `dict` |

Fire and forget

```python
command = {
  "method": "set",
  "uri": "/contacts",
  "type": "application/vnd.lime.contact+json",
  "resource": {
    "identity": "11121023102013021@messenger.gw.msging.net",
    "name": "John Doe",
  }
}

bs.send_command(command)
```

---

#### process_command

| Parameters | Type   |
| ---------- | ------ |
| command    | `dict` |

Receive the response

```python
command = {
  "to": "postmaster@analytics.msging.net",
  "method": "get",
  "uri": "/event-track"
}

tracks = bs.process_command(command)
print(tracks)

# Output
# {
#     "type": "application/vnd.lime.collection+json",
#     "resource": {
#         "itemType": "application/vnd.iris.eventTrack+json",
#         "items": [
#             {
#                 "category": "accounts"
#             },
#             {
#                 "category": "payments"
#             }
#         ]
#     },
#     "method": "get",
#     "status": "success",
#     "id": "{{some_guid}}",
#     "from": "postmaster@analytics.msging.net/#az-iris5",
#     "to": "contact@msging.net",
#     "metadata": {
#         "#command.uri": "lime://contact@msging.net/event-track"
#     }
# }

```

---

#### force_command

| Parameters    | Type    | Required |
| ------------- | ------- | -------- |
| command       | `dict`  | yes      |
| attempts      | `int`   | no       |
| cooldown_time | `float` | no       |

Make the amount of `attempts` with the `cooldown_time` until the request success.

Will return the response

```python
command = {
  "to": "postmaster@broadcast.msging.net",
  "method": "set",
  "type": "application/vnd.iris.distribution-list+json",
  "uri": "/lists",
  "resource": {
    "identity": "your_distributionList@broadcast.msging.net"
  }
}

list_response = bs.force_command(command, 4, 0.5)
print(list_response)

# Output
# {
#   "id": "{{some_guid}}",
#   "from": "postmaster@broadcast.msging.net/#irismsging1",
#   "to": "contact@msging.net/default",
#   "method": "set",
#   "status": "success"
# }

```

---

#### send_message

| Parameters | Type   |
| ---------- | ------ |
| message    | `dict` |

Fire and forget

```python
message = {
    "to": "551100001111@0mn.io",
    "type": "text/plain",
    "content": "Hello, how can I help you?"
}

bs.send_message(message)
```
