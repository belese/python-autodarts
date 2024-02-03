from typing import Any, Dict, Optional
from .endpoint import AutoDartEndpointWs
from .session import AutoDartSession
from .host import Host
from .player import Player
from .match import Match
from posixpath import join as urljoin

class Lobby(AutoDartEndpointWs):
    """
    Represents a lobby in the AutoDARTS system.

    Attributes:
    - createdAt (str): The creation timestamp of the lobby.
    - isPrivate (bool): Indicates if the lobby is private.
    - variant: The variant of the lobby.
    - settings: The settings of the lobby.
    - bullOffMode: The bull-off mode of the lobby.
    - hostId: The ID of the host of the lobby.
    - host: The host object representing the host of the lobby.
    - maxPlayers: The maximum number of players allowed in the lobby.
    - players: Generator yielding Player objects in the lobby.
    """

    ENDPOINT: str = "gs/v0/lobbies/"
    CHANNEL: str = "autodarts.lobbies"
    
    def __init__(self, session: AutoDartSession, on_state_cb=None, on_event_cb=None,
                 ws_url: str = AutoDartEndpointWs.WS_ENDPOINT, endpoint: str = ENDPOINT,
                 channel: str = CHANNEL) -> None:
        """
        Initialize a Lobby instance.

        Parameters:
        - session (AutoDartSession): The session used for communication.
        - on_state_cb: Callback function for state changes.
        - on_event_cb: Callback function for events.
        - ws_url (str): The WebSocket URL.
        - endpoint (str): The API endpoint for the lobby.
        - channel (str): The WebSocket channel for the lobby.

        Returns:
        None
        """
        super().__init__(session, endpoint, channel, on_state_cb=on_state_cb, on_event_cb=on_event_cb, ws_url=ws_url)
    
    @property
    def createdAt(self) -> Optional[str]:
        """Get the creation timestamp of the lobby."""
        return self._state.get("createdAt")
    
    @property
    def isPrivate(self) -> Optional[bool]:
        """Check if the lobby is private."""
        return self._state.get("isPrivate")
    
    @property
    def variant(self) -> Optional[Any]:
        """Get the variant of the lobby."""
        return self._state.get("variant")
    
    @property
    def settings(self) -> Optional[Any]:
        """Get the settings of the lobby."""
        return self._state.get("settings")
    
    @property
    def bullOffMode(self) -> Optional[Any]:
        """Get the bull-off mode of the lobby."""
        return self._state.get("bullOffMode")
    
    @property
    def hostId(self) -> Optional[Any]:
        """Get the ID of the host of the lobby."""
        return self._state.get("hostId")
    
    @property
    def host(self) -> Host:
        """Get the host object representing the host of the lobby."""
        return Host(self.session, self._state.get("host"))
    
    @property
    def maxPlayers(self) -> Optional[Any]:
        """Get the maximum number of players allowed in the lobby."""
        return self._state.get("maxPlayers")
    
    @property
    def players(self) -> Player:
        """
        Generate Player objects representing players in the lobby.

        Yields:
        - Player: The next player in the lobby.
        """
        for player in self._state.get("players"):
            yield Player(self.session, player)
    
    async def async_add_player(self, player: Player) -> None:
        """
        Add a player to the lobby.

        Parameters:
        - player (Player): The player to be added to the lobby.

        Returns:
        None
        """
        data: Dict[str, Any] = {
            'boardId': player.boardId,
            'name': player.name,
        }

        if player.userId:
            data['userId'] = player.userId
        
        await self.session.post(self.get_endpoint("players"), data=data)
    
    async def async_remove_player(self, player: Player) -> None:
        """
        Remove a player from the lobby.

        Parameters:
        - player (Player): The player to be removed from the lobby.

        Returns:
        None
        """
        await self.session.delete(self.get_endpoint("players", "by-index", player.index))
    
    async def async_delete(self) -> None:
        """Delete the lobby."""
        await self.session.delete(self.get_endpoint())
    
    async def async_start(self) -> Match:
        """
        Start the lobby.

        Returns:
        Match: The Match object representing the started match.
        """
        state = await self.session.put(self.get_endpoint("start")).json()
        return Match(self.session, state=state)
    
    @classmethod
    async def async_new(cls, session: AutoDartSession, variant: Any, settings: Any,
                        bullOffMode: str = "Off", isPrivate: bool = True) -> "Lobby":
        """
        Create a new lobby.

        Parameters:
        - session (AutoDartSession): The session used for communication.
        - variant: The variant of the lobby.
        - settings: The settings of the lobby.
        - bullOffMode (str): The bull-off mode of the lobby.
        - isPrivate (bool): Indicates if the lobby is private.

        Returns:
        Lobby: The newly created Lobby object.
        """
        data: Dict[str, Any] = {
            "variant": variant,
            "settings": settings,
            "bullOffMode": bullOffMode,
            "isPrivate": isPrivate
        }

        endpoint = urljoin(cls.API_URL, cls.ENDPOINT)
        state = await session.post(endpoint, data=data).json()
        return cls(session, state=state)
