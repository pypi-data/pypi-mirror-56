# gmaily

Unofficial Gmail python client with pythonic API.

## Features

- [x] Clean API
- [x] No other dependencies than standard library
- [ ] Lazy loading for content

## Example

```python
import sys
import getpass
import datetime

from gmaily import Gmaily

g = Gmaily()

user_email = input("Email: ")
user_pw = getpass.getpass()

if not g.login(user_email, user_pw):
    print("Cannot login")
    sys.exit(1)

msgs = g.inbox().after(datetime.date.today() - datetime.timedelta(weeks=2))
for msg in msgs.all():
    print("\n" + (" Mail UID: %d " % msg.uid).center(80, "=") + "\n")
    print("Subject:", msg.subject)
    print("From:", msg.sender)
    print("Date:", msg.date)
    print("Attachments:", msg.attachments)

    print("-" * 10)
    print(msg.text)

g.logout()
```

## Usage

### Searching Mailbox

`SearchQuery`, which is returned by some methods like `Gmaily.inbox`
supports method chaining and you can easily mix search criterias together:

```python
two_weeks_ago = datetime.date.today() - datetime.timedelta(weeks=2)
msgs = g.inbox().by("john@example.com").before(two_weeks_ago)
```

Alternatively, you can use other mailboxes than `INBOX` in the above example
using `Gmaily.mailbox` method:

```python
msgs = g.mailbox("URGENT").on(datetime.date.today())
```

You can then execute the query and fetch the results using `SearchQuery.all`:

```python
print(msgs.all())
```

You can find the full list of supported criterias and their description at
[here](https://tools.ietf.org/html/rfc3501#section-6.4.4).
Note that `ALL` criteria is not present because it's the default criteria
and `SearchQuery.all` stands for executing the query.
Any other names like `.fetch()`, `.do()` could be taken the place,
but I chose the `.all()` because famous ORMs use it too.

Some other criterias are omitted too:

- `NOT`
- `OR`
- `UID`

## Installation

It requires `Python>=3.5`.

```
$ pip3 install -U gmaily
```

## License

MIT

