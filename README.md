# AutoDarts Python Library

## Overview

The AutoDarts Python library is an unofficial implementation for interacting with the AutoDarts web API and WebSocket. This library is designed to provide a convenient way to integrate AutoDarts functionality into Python applications. It supports asynchronous operations to handle real-time updates via WebSocket.


**THIS IS A WIP PROJECT, IN BETA VERSION**

## Features

### Session
- **AutoDartSession:** Handles authentication and provides a session for making API requests and web socket connection.

### Websocket and endpoint
- **CloudBoard:** Represents your Cloud dartboard support.
- **Match:** Represents a match in AutoDarts.
- **Lobby:** Represents a lobby in AutoDarts.

### Endpoint
- **User:** Represents a user in AutoDarts.

### Child
- **Player:** Represents a player in AutoDarts.


## Installation

```bash
pip install autodarts
```

## Usage


```python

# Initialize AutoDartSession
from autodarts import AutoDartSession

#create the session
session = AutoDartSession(
    email=email,
    password=password,
    client_id=client_id,
    realm_name=realm_name,
    client_secret_key=client_secret_key,
)

#get the cloud board from its id
cloud_board = await CloudBoard.from_id( sessions, BOARD_ID )

# Connect to events 
cloud_board.connect() 

#get attribute
print(f"Board Name: {cloud_board.name}")

#call action
await cloud_board.async_start()

#access relationchip
match = await cloud_board.async_get_match()

#register callback
async def on_board_connected(msg):
    print("Board connected : ", msg)
    await asyncio.sleep(1)
       
unregister_handler = cloud_board.register_callback( "Connected",  on_board_connected )

#unregister
unregister_handler()

# disConnect from events 
cloud_board.disconnect()

```
See example folder for a more detailled example

