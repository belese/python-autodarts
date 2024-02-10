from typing import Any, Dict, List, Optional
from .endpoint import AutoDartEndpointWs
from .session import AutoDartSession

# From  https://github.com/lbormann/autodarts-caller/blob/d6d56a4edeab63440f934bc36b122c6a6c395f5b/autodarts-caller.py#L155
# with permission of wusssa
FIELD_COORDS = {
    "Miss": {"x": 0.016160134143785285,"y": 1.1049884720184449},
    "S1": {"x": 0.2415216935652902,"y": 0.7347516243974009}, 
    "D1": {"x": 0.29786208342066656,"y": 0.9359673024523162}, 
    "T1": {"x": 0.17713267658771747,"y": 0.5818277090756655},
    "S2": {"x": 0.4668832529867955,"y": -0.6415636134982183}, 
    "D2": {"x": 0.5876126598197445,"y": -0.7783902745755609}, 
    "T2": {"x": 0.35420247327604254,"y": -0.4725424439320897},
    "S3": {"x": 0.008111507021588693,"y": -0.7864389016977573}, 
    "D3": {"x": -0.007985747222804492,"y": -0.9715573255082791}, 
    "T3": {"x": -0.007985747222804492,"y": -0.5932718507650387},
    "S4": {"x": 0.6439530496751206,"y": 0.4530496751205198}, 
    "D4": {"x": 0.7888283378746596,"y": 0.5657304548312723}, 
    "T4": {"x": 0.48298050723118835,"y": 0.36451477677635713},
    "S5": {"x": -0.23334730664430925,"y": 0.7508488786417943}, 
    "D5": {"x": -0.31383357786627536,"y": 0.9279186753301195}, 
    "T5": {"x": -0.1850555439111297,"y": 0.5737790819534688},
    "S6": {"x": 0.7888283378746596,"y": -0.013770697966883233}, 
    "D6": {"x": 0.9739467616851814,"y": 0.010375183399706544}, 
    "T6": {"x": 0.5956612869419406,"y": -0.005722070844686641},
    "S7": {"x": -0.4506602389436176,"y": -0.6335149863760215}, 
    "D7": {"x": -0.5713896457765667,"y": -0.7703416474533641}, 
    "T7": {"x": -0.3540767134772585,"y": -0.4725424439320897},
    "S8": {"x": -0.7323621882204988,"y": -0.239132257388388}, 
    "D8": {"x": -0.9255292391532174,"y": -0.2954726472437643}, 
    "T8": {"x": -0.5713896457765667,"y": -0.18279186753301202},
    "S9": {"x": -0.627730035631943,"y": 0.4691469293649132}, 
    "D9": {"x": -0.7726053238314818,"y": 0.5657304548312723}, 
    "T9": {"x": -0.48285474743240414,"y": 0.34841752253196395},
    "S10": {"x": 0.7244393208970865,"y": -0.23108363026619158}, 
    "D10": {"x": 0.9256549989520018,"y": -0.28742402012156787}, 
    "T10": {"x": 0.5715154055753511,"y": -0.19084049465520878},
    "S11": {"x": -0.7726053238314818,"y": -0.005722070844686641}, 
    "D11": {"x": -0.9657723747642004,"y": -0.005722070844686641}, 
    "T11": {"x": -0.5955355271431566,"y": 0.0023265562775099512},
    "S12": {"x": -0.4506602389436176,"y": 0.6140222175644519}, 
    "D12": {"x": -0.5633410186543703,"y": 0.7910920142527772}, 
    "T12": {"x": -0.3540767134772585,"y": 0.4932928107315028},
    "S13": {"x": 0.7244393208970865,"y": 0.24378536994340808}, 
    "D13": {"x": 0.917606371829805,"y": 0.308174386920981}, 
    "T13": {"x": 0.5634667784531546,"y": 0.18744498008803193},
    "S14": {"x": 0.6278557954307273,"y": -0.46449381680989327}, 
    "D14": {"x": -0.9255292391532174,"y": 0.308174386920981}, 
    "T14": {"x": -0.5713896457765667,"y": 0.19549360721022835},
    "S15": {"x": 0.6278557954307273,"y": -0.46449381680989327}, 
    "D15": {"x": 0.7888283378746596,"y": -0.5771745965206456}, 
    "T15": {"x": 0.4910291343533851,"y": -0.34376440997694424},
    "S16": {"x": -0.6196814085097464,"y": -0.4725424439320897}, 
    "D16": {"x": -0.7967512051980717,"y": -0.5610773422762524}, 
    "T16": {"x": -0.49090337455460076,"y": -0.33571578285474746},
    "S17": {"x": 0.2415216935652902,"y": -0.730098511842381}, 
    "D17": {"x": 0.29786208342066656,"y": -0.9152169356529029}, 
    "T17": {"x": 0.18518130370991423,"y": -0.5691259693984492},
    "S18": {"x": 0.48298050723118835,"y": 0.6462167260532384}, 
    "D18": {"x": 0.5554181513309578,"y": 0.799140641374974}, 
    "T18": {"x": 0.3292712798530314,"y": 0.49608083282302506},
    "S19": {"x": -0.2586037966932027,"y": -0.7658909981628906}, 
    "D19": {"x": -0.3134721371708513,"y": -0.9148193508879362}, 
    "T19": {"x": -0.19589712186160443,"y": -0.562094304960196},
    "S20": {"x": 0.00006123698714003468,"y": 0.7939375382731171}, 
    "D20": {"x": 0.01119619445411297, "y": 0.9726766446223462}, 
    "T20": {"x": 0.00006123698714003468, "y": 0.6058175137783223},
    "25": {"x": 0.06276791181873864, "y": 0.01794243723208814}, 
    "Bull": {"x": -0.007777097366809472, "y": 0.0022657685241886157},
}

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
    def created_at(self) -> Optional[str]:
        """Get the creation timestamp of the match."""
        return self._state.get("createdAt")

    @property
    def finished(self) -> bool:
        """Check if the match is finished."""
        return self._state.get("finished", False)

    @property
    def game_finished(self) -> bool:
        """Check if the game within the match is finished."""
        return self._state.get("gameFinished", False)

    @property
    def game_schedule_finished(self) -> bool:
        """Check if the schedule for the game is finished."""
        return self._state.get("gameScheduleFinished", False)

    @property
    def game_scores(self) -> List[Dict[str, Any]]:
        """Get the list of game scores."""
        return self._state.get("gameScores", [])

    @property
    def game_winner(self) -> Any:
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
        if not self._state.get("state") :
            self._state['state'] = {}
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
        return [Player(player,self.session) for player in self._state.get("players")]
            

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

    async def async_finish(self) -> None:
        """Undo the match."""
        await self.session.post(self.get_endpoint("finish"))
    
    @property
    def ws_data(self) :
        return self._state
    
    async def async_throw(self,segment:{str:any}, point: {str:float} = None, throw_id:int|None = None,type: str = "normal") -> None:
        """
        Perform a throw in the match.

        Parameters:
        - segment: The sgment of the throw
        - point ({str:float}|None): The coordinates of the throw.
        - throw_id (int|None): The ID of the throw.
        - type (str): The type of the throw.

        Returns:
        None
        """
        if throw_id is None :
            data = {
                "segment" : segment
            }
            if point :
                data['coords'] = point
            await self.session.post(self.get_endpoint("throws"), json=data)
        else :
            if not point :
                point = FIELD_COORDS[segment['name']]
            data: Dict[str, Any] = {
                "changes": {
                    throw_id: {
                        "point": point,
                        "type": type
                    }
                }
            }
            await self.session.patch(self.get_endpoint("throws"), json=data)

from .player import Player