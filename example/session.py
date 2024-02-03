# Initialize AutoDartSession
import asyncio
from autodarts import AutoDartSession, AutoDartException

async def main():
    email = "your_email@example.com"
    password = "your_password"
    client_id = "application_client_id"
    realm_name = "application_realm_name"
    client_secret_key = "application_client_secret_key"

    session = AutoDartSession(
        email=email,
        password=password,
        client_id=client_id,
        realm_name=realm_name,
        client_secret_key=client_secret_key,
    )

    try:
        # Check if the session is authenticated
        authenticated = await session.is_authenticated()
        if authenticated:
            print("Session is authenticated")
        else:
            print("Session is not authenticated")

    except AutoDartException as e:
        #useless here, only for example
        print(f"Authentication failed: {e}")


# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())