from .session import AutoDartSession
from .endpoint import AutoDartEndpoint
from .session import AutoDartSession

class User(AutoDartEndpoint):
    """Represent a User."""

    ENDPOINT = "as/v0/users/"
    STATS_ENDPOINT = "stats/"
    
    supported_stats = ["countup","cricket","x01"]

    def __init__(self, session:AutoDartSession, name, id=None , endpoint:str=ENDPOINT,api_url:str=AutoDartEndpoint.API_URL,stats_endpoint=STATS_ENDPOINT) -> None:
        state = {
            "id" : id,
            "name" : name
        }
        super().__init__(session, endpoint, api_url, state)
        self.stats_endpoint = stats_endpoint
    
    @property
    def name(self):
        """Player name."""
        return self._state.get("name")
    
    async def get_stat(self, variant, limit=10):
        """Return the stats."""
        if variant not in self.supported_stats:
            raise ValueError("Unsupported variant")
        if self.id is None:
            raise ValueError("Guest User has no stats")
        return (await self.session.get(self.get_endpoint(self.id,self.stats_endpoint,variant),params={'limit' : limit})).json()