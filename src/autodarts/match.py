from typing import Any, Dict, List, Optional
from .endpoint import AutoDartEndpointWs
from .session import AutoDartSession

class Match(AutoDartEndpointWs):
    """
    Represents a match in the AutoDARTS system.

    Attributes:
    - createdAt (str): The creation timestamp of the match.
    - finished (bool): Indicates if the match is finished.
    - gameFinished (bool): Indicates if the game within the match is finished.
    - gameScheduleFinished (bool): Indicates if the schedule for the game is finished.
    - gameScores (List[Dict[str, Any]]): List of game scores.
    - gameWinner: The winner of the game.
    - host: The host of the match.
    - set: The current set of the match.
    - sets: List of sets in the match.
    - state: The current state of the match.
    - stats: Statistics of the match.
    - turnBusted: Indicates if the turn is busted.
    - turnScore: The score of the current turn.
    - turns: The number of turns in the match.
    - winner: The winner of the match.
    - leg: The current leg of the match.
    - legs: List of legs in the match.
    - variant: The variant of the match.
    - settings: The settings of the match.
    - player: The player in the match.
    - players: List of players in the match.
    - round: The current round of the match.
    - scores: The scores in the match.
    """

    ENDPOINT: str = "gs/v0/matches/"
    CHANNEL: str = "autodarts.matches"
    
    def __init__(self, state,session: AutoDartSession,
                 ws_url: str = AutoDartEndpointWs.WS_ENDPOINT, 
                 endpoint: str = ENDPOINT,
                 channel: str = CHANNEL) -> None:
        """
        Initialize a Match instance.

        Parameters:
        - state (Dict[str, Any]): The state of the match.   
        - session (AutoDartSession): The session used for communication.
        - ws_url (str): The WebSocket URL.
        - endpoint (str): The API endpoint for the match.
        - channel (str): The WebSocket channel for the match.

        Returns:
        None
        """
        super().__init__(state,session, endpoint, channel, ws_url=ws_url)

    @property
    def createdAt(self) -> Optional[str]:
        """Get the creation timestamp of the match."""
        return self._state.get("createdAt")

    @property
    def finished(self) -> bool:
        """Check if the match is finished."""
        return self._state.get("finished", False)

    @property
    def gameFinished(self) -> bool:
        """Check if the game within the match is finished."""
        return self._state.get("gameFinished", False)

    @property
    def gameScheduleFinished(self) -> bool:
        """Check if the schedule for the game is finished."""
        return self._state.get("gameScheduleFinished", False)

    @property
    def gameScores(self) -> List[Dict[str, Any]]:
        """Get the list of game scores."""
        return self._state.get("gameScores", [])

    @property
    def gameWinner(self) -> Any:
        """Get the winner of the game."""
        return self._state.get("gameWinner")

    @property
    def host(self) -> Any:
        """Get the host of the match."""
        return self._state.get("host")

    @property
    def set(self) -> Any:
        """Get the current set of the match."""
        return self._state.get("set")

    @property
    def sets(self) -> Any:
        """Get the list of sets in the match."""
        return self._state.get("sets")

    @property
    def state(self) -> Any:
        """Get the current state of the match."""
        return self._state.get("state")

    @property
    def stats(self) -> Any:
        """Get the statistics of the match."""
        return self._state.get("stats")

    @property
    def turn_busted(self) -> Any:
        """Get the indicator if the turn is busted."""
        return self._state.get("turnBusted")

    @property
    def turn_score(self) -> Any:
        """Get the score of the current turn."""
        return self._state.get("turnScore")

    @property
    def turns(self) -> Any:
        """Get the number of turns in the match."""
        return self._state.get("turns")

    @property
    def winner(self) -> Any:
        """Get the winner of the match."""
        return self._state.get("winner")

    @property
    def leg(self) -> Any:
        """Get the current leg of the match."""
        return self._state.get("leg")

    @property
    def legs(self) -> Any:
        """Get the list of legs in the match."""
        return self._state.get("legs")

    @property
    def variant(self) -> Any:
        """Get the variant of the match."""
        return self._state.get("variant")

    @property
    def settings(self) -> Any:
        """Get the settings of the match."""
        return self._state.get("settings")

    @property
    def player(self) -> Any:
        """Get the player in the match."""
        return self._state.get("player")

    @property
    def players(self) -> Any:
        """Get the list of players in the match."""
        for player in self._state.get("players"):
            yield Player(player,self.session)

    @property
    def round(self) -> Any:
        """Get the current round of the match."""
        return self._state.get("round")

    @property
    def scores(self) -> Any:
        """Get the scores in the match."""
        return self._state.get("scores")

    async def async_next_player(self) -> None:
        """Move to the next player in the match."""
        await self.session.post(self.get_endpoint("players", "next"))

    async def async_next_match(self) -> None:
        """Move to the next match in the game."""
        await self.session.post(self.get_endpoint("games", "next"))

    async def async_undo(self) -> None:
        """Undo the match."""
        await self.session.post(self.get_endpoint("undo"))

    async def async_abort(self) -> None:
        """Abort the match."""
        await self.session.delete(self.get_endpoint())

    async def async_throw(self, throw_id: Any, point: tuple[int, int], type: str = "normal") -> None:
        """
        Perform a throw in the match.

        Parameters:
        - throw_id (Any): The ID of the throw.
        - point (tuple[int, int]): The coordinates of the throw.
        - type (str): The type of the throw.

        Returns:
        None
        """
        data: Dict[str, Any] = {
            "changes": {
                throw_id: {
                    "point": {
                        "x": point[0],
                        "y": point[1]
                    },
                    "type": type
                }
            }
        }
        await self.session.patch(self.get_endpoint("throws"), json=data)

from .player import Player