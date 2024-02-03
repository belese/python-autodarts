from autodarts import AutoDartSession, CloudBoard,AutoDartException

BOARD_ID = "myboardid"

async def main():
    email = "your_email@example.com"
    password = "your_password"
    client_id = "application_client_id"
    realm_name = "application_realm_name"
    client_secret_key = "application_client_secret_key"

    # Initialize AutoDartSession
    session = AutoDartSession(
        email=email,
        password=password,
        client_id=client_id,
        realm_name=realm_name,
        client_secret_key=client_secret_key,
    )

    try:
        #List your CloudBoard (factory is a generator available for all endpoints)
        async for cloud_board in CloudBoard.factory(session=session) :
            # Access properties of the board
            print(f"Board Name: {cloud_board.name}")
            print(f"Connected: {cloud_board.connected}")
            print(f"Running: {cloud_board.running}")
            print(f"Last Event: {cloud_board.last_event}")

        #get the first board
        cloud_board = await anext( CloudBoard.factory(session=session) )
        print("First board: ", cloud_board.name)

        
        match = await cloud_board.async_get_match()
        if match is not None: 
            print("Variant: ", match.variant)
            print("First Player: ", next(match.players).name) 
            #Connecting an Autodart object will keep state updated with websocket events, and you could register call back too
            match.connect()
            await asyncio.sleep(5)
            await match.async_next_player()
        #get the board from a id
        #cloud_board = await CloudBoard.from_id(sessions,BOARD_ID)
            
        # Connect to events (with optional parameter for all msgs callbacks (event and state in different cb) )
        cloud_board.connect()
        
        # Perform actions on the board (object don't need to be connected), but object need to be connected if you want msg callbacks for those actions
        await cloud_board.async_start()
        print("Board started.")

        await asyncio.sleep(5)
        await cloud_board.async_reset()
        print("Board reset.")

        await asyncio.sleep(5)
        await cloud_board.async_stop()
        print("Board stopped.")

        #refresh data
        await cloud_board.async_load_state()

        async def on_board_connected(msg):
            print("Board connected : ", msg)
            await asyncio.sleep(1)
       
        unregister_handler = cloud_board.register_callback("Connected", on_board_connected)

        await asyncio.sleep(12225)
        unregister_handler()

        #Optionnal
        cloud_board.disconnect()

    except AutoDartException as e:
        # Catch autodarts exceptions
        print ('Exception: ', e)
        raise e

# Run the asyncio event loop
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())