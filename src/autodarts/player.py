from typing import Optional
from .endpoint import AutoDartBase
from .session import AutoDartSession

class Player(AutoDartBase):
    """
    Represents a player in the AutoDARTS system.

    Attributes:
    - index (int): The index of the player.
    - userId (str): The user ID associated with the player.
    - user (User): The user object representing the player.
    - name (str): The name of the player.
    - avatarUrl (str): The URL of the player's avatar.
    - hostId (str): The host ID associated with the player.
    - host (Host): The host object representing the player's host.
    - boardId (str): The board ID associated with the player.
    - board (OpponentBoard): The opponent board object representing the player's board.
    - boardName (str): The name of the player's board.
    - cpuPPR (float): The player's CPU PPR (Points Per Round).
    """

    collection_endpoint: Optional[str] = None

    @property
    def index(self) -> Optional[int]:
        """Get the index of the player."""
        return self._state.get("index")

    @property
    def userId(self) -> Optional[str]:
        """Get the user ID associated with the player."""
        return self._state.get("userId")

    @property
    def user(self) -> "User":
        """Get the user object representing the player."""
        return User(self.session, self.name, self.userId)

    @property
    def name(self) -> Optional[str]:
        """Get the name of the player."""
        return self._state.get("name")

    @property
    def avatarUrl(self) -> Optional[str]:
        """Get the URL of the player's avatar."""
        return self._state.get("avatarUrl")

    @property
    def hostId(self) -> Optional[str]:
        """Get the host ID associated with the player."""
        return self._state.get("hostId")

    @property
    def host(self) -> "Host":
        """Get the host object representing the player's host."""
        return Host(self.session, self._state.get("host"))

    @property
    def boardId(self) -> Optional[str]:
        """Get the board ID associated with the player."""
        return self._state.get("boardId")

    @property
    def board(self) -> "OpponentBoard":
        """Get the opponent board object representing the player's board."""
        return OpponentBoard(self.boardId, self.boardName)

    @property
    def boardName(self) -> Optional[str]:
        """Get the name of the player's board."""
        return self._state.get("boardName")

    @property
    def cpuPPR(self) -> Optional[float]:
        """Get the player's CPU PPR (Points Per Round)."""
        return self._state.get("cpuPPR")

from .user import User
from .board import OpponentBoard
from .host import Host
