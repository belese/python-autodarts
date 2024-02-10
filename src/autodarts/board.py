from typing import Optional, List

from .endpoint import AutoDartEndpointWs, AutoDartBase, AutoDartEndpoint
from .session import AutoDartSession

import logging

logger = logging.getLogger(__name__)
class OpponentBoard(AutoDartBase):
    """
    Represents an opponent's dartboard.
    """
    def __init__(self, id: int, name: str) -> None:
        """
        Initialize an OpponentBoard instance.

        Parameters:
        - id (int): The unique identifier for the dartboard.
        - name (str): The name of the dartboard.

        Returns:
        None
        """
        state = {
            "id": id,
            "name": name
        }
        super().__init__(state=state)

    @property
    def id(self) -> int:
        """Get the unique identifier of the dartboard."""
        return self._state.get("id")

    @property
    def name(self) -> str:
        """Get the name of the dartboard."""
        return self._state.get("name")


class CloudBoard(AutoDartEndpointWs):
    """
    Represents a Cloud dartboard.
    """
    ENDPOINT = "bs/v0/boards/"
    CHANNEL = "autodarts.boards"

    events = [
        'Starting',
        'Started',
        'Stopped',
        'Stopping',
        'Manual_reset',
        'Connected',
        'Disconnected',
        'Throw detected',
    ]

    def __init__(self, state: dict, session: AutoDartSession, ws_url: str = AutoDartEndpointWs.WS_ENDPOINT,
                 endpoint: str = ENDPOINT, channel: str = CHANNEL, api_url: str = AutoDartEndpoint.API_URL) -> None:
        """
        Initialize a CloudBoard instance.

        Parameters:
        - state (dict): The initial state of the dartboard.
        - session (AutoDartSession): The session object for making API requests.
        - ws_url (str): The WebSocket endpoint URL.
        - endpoint (str): The API endpoint for the dartboard.
        - channel (str): The WebSocket channel for dartboard events.
        - api_url (str): The base API URL.

        Returns:
        None
        """
        super().__init__(state, session, endpoint, ws_url=ws_url, api_url=api_url, channel=channel)

    @property
    def name(self) -> Optional[str]:
        """Get the name of the dartboard."""
        return self._state.get("name")

    @property
    def connected(self) -> bool:
        """Check if the dartboard is connected."""
        return self._state.get("connected", False)

    @property
    def running(self) -> bool:
        """Check if the dartboard is running."""
        return self._state.get("running", False)

    @property
    def event(self) -> Optional[str]:
        """Get the current event on the dartboard."""
        return self._state.get("event", False)

    @property
    def status(self) -> Optional[str]:
        """Get the status of the dartboard."""
        return self._state.get("status")

    @property
    def owners(self) -> List[str]:
        """Get the list of owners of the dartboard."""
        return self._state.get("owners")

    @property
    def ip(self) -> Optional[str]:
        """Get the IP address of the dartboard."""
        return self._state.get("ip")

    @property
    def match_id(self) -> Optional[str]:
        """Get the match ID associated with the dartboard."""
        return self._state.get("matchId")

    @property
    def state(self) -> str:
        """Get the state of the dartboard."""
        if not self._state.get("state") :
            self._state['state'] = {}
        return self._state["state"]

    @property
    def version(self) -> str:
        """Get the version of the dartboard."""
        return self._state["version"]

    @property
    def os(self) -> str:
        """Get the operating system of the dartboard."""
        return self._state["os"]

    async def async_get_match(self) -> Optional["Match"]:
        """Get the Match object associated with the dartboard."""
        if not self.match_id :
            return
        else :
            return await Match.from_id(self.session,self.match_id)

    async def async_load(self):
        """Asynchronously load the state of the entity."""
        await self.async_load_data()
    
    async def async_load_data(self):
        """Asynchronously load the state of the entity."""
        board = await self.__class__.from_id(self.session,self.id)
        self._state.update(board._state)
    
    async def async_load_state(self):
        """Asynchronously load the state of the entity."""
        if self.state.get('connected') :
            self._state["state"].update(await (await self.session.get(self.get_endpoint("state"), timeout=10)).json())
    
    async def async_start(self) -> None:
        """Start the dartboard."""
        await self.session.put(self.get_endpoint("start"))

    async def async_stop(self) -> None:
        """Stop the dartboard."""
        await self.session.put(self.get_endpoint("stop"))

    async def async_reset(self) -> None:
        """Reset the dartboard."""
        await self.session.put(self.get_endpoint("reset"))
    
    @classmethod
    async def from_id(cls, session: AutoDartSession, id: str) -> "AutoDartEndpoint":
        """Create an instance of the entity from its ID."""
        async for board in cls.factory(session) :
            if board.id == id :
                return board
    
from .match import Match
