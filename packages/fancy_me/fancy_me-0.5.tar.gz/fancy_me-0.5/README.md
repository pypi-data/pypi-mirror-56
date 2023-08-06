# socket_me
### Introduction
 An production make you use tcp to control websocket

### Install
```bash
    pip install socket_me
```

### Usage

``` python
from socket_me import Ipo, ipo, send


@ipo(type="connect_me")
def somewheve(**kwargs) -> None:
    print(kwargs)
    send("wh", "hello")
    print("进入处理函数")


@ipo(type="init")
def ko(**kwargs) -> None:
    user = kwargs.get('data').get('data').get("user")
    send(user, "hello")
    print("ws 已经连接")

a = Ipo()
a.start()

```

# More 
developing....
