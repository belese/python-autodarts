
from typing import Optional
from .endpoint import AutoDartBase

class Host(AutoDartBase):
    """
    Represents a host in the AutoDARTS system.

    Attributes:
    - id (str): The ID of the host.
    - name (str): The name of the host.
    - avatar_url (str): The URL of the host's avatar.
    """

    @property
    def id(self) -> Optional[str]:
        """Get the ID of the host."""
        return self.data.get("id")

    @property
    def name(self) -> Optional[str]:
        """Get the name of the host."""
        return self.data.get("name")

    @property
    def avatar_url(self) -> Optional[str]:
        """Get the URL of the host's avatar."""
        return self.data.get("avatarUrl")