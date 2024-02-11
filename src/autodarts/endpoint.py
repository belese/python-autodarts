from typing import Any, Awaitable, Callable, Dict, Optional
from collections import defaultdict
import asyncio
import aiohttp
from .session import AutoDartSession, AutoDartException
from posixpath import join as urljoin
import json
import logging

logger = logging.getLogger(__name__)
class AutoDartMissingIdException(AutoDartException):
    pass

class AutoDartInvalidStateException(AutoDartException):
    pass

class AutoDartBase:
    """
    Represents the base class for AutoDARTS entities.
    """
    def __init__(self, state: Dict[str, Any], session: Optional[AutoDartSession] = None) -> None:
        """
        Initialize an AutoDartBase instance.

        Parameters:
        - state (dict): The initial state of the entity.
        - session (AutoDartSession): The session used for communication.

        Returns:
        None
        """
        self._state = state
        self.session = session
    
class AutoDartEndpoint(AutoDartBase):
    """
    Represents an endpoint in the AutoDARTS system.
    """
    API_URL = "https://api.autodarts.io"

    ENDPOINT = None
    
    def __init__(self, state: Dict[str, Any], session: AutoDartSession, endpoint: str, api_url: str = API_URL) -> None:
        """
        Initialize an AutoDartEndpoint instance.

        Parameters:
        - state (dict): The initial state of the entity.
        - session (AutoDartSession): The session used for communication.
        - endpoint (str): The API endpoint for the entity.
        - api_url (str): The base API URL.

        Raises:
        - AutoDartMissingIdException: If the entity's state lacks an 'id'.

        Returns:
        None
        """
        if not state or not state.get('id'):
            raise AutoDartMissingIdException(f"Can't init {self.__class__.__name__} without id in state")
        super().__init__(state, session=session)
        self.collection_endpoint = endpoint
        self.api_url = api_url
    
    def __await__(self):
        self.async_load_state().__await__()
        return self
    
    @property	
    def id(self) -> str | None:
        """Get the ID of the entity."""
        return self._state.get('id')
    
    def get_endpoint(self, *args: [str]) -> str:
        """Get the full API endpoint for the entity."""
        return urljoin(self.api_url, self.collection_endpoint, self.id, *args) 

    async def async_load(self):
        """Asynchronously load the state of the entity."""
        await self.async_load_data()
        await self.async_load_state()
    
    async def async_load_data(self):
        """Asynchronously load the state of the entity."""
        self._state.update(await (await self.session.get(self.get_endpoint(), timeout=10)).json())
    
    async def async_load_state(self):
        """Asynchronously load the state of the entity."""
        pass
        self._state.update(await (await self.session.get(self.get_endpoint("state"), timeout=10)).json())
    
    @classmethod
    async def from_id(cls, session: AutoDartSession, id: str) -> "AutoDartEndpoint":
        """Create an instance of the entity from its ID."""
        endpoint = urljoin(cls.API_URL, cls.ENDPOINT, id)
        state = await session.get(endpoint)
        item = cls(await state.json(),session=session)
        await item.async_load_state()
        return item
    
    @classmethod
    async def factory(cls, session: AutoDartSession):
        """Create instances of the entity using a factory method."""
        endpoint = urljoin(cls.API_URL, cls.ENDPOINT)
        states = await session.get(endpoint)
        for state in await states.json():
            item = cls(state, session=session)
            await item.async_load_state()
            yield item


class AutoDartEndpointWs(AutoDartEndpoint):
    """
    Represents an endpoint with WebSocket support in the AutoDARTS system.
    """
    WS_ENDPOINT = "wss://api.autodarts.io/ms/v0/subscribe"

    event_topics = [
        "state",
        "events"
    ]
    
    events = [
    ]

    def __init__(self, state: Dict[str, Any], session: AutoDartSession, endpoint: str, channel: str,
                 ws_url: str = WS_ENDPOINT, api_url: str = AutoDartEndpoint.API_URL) -> None:
        """
        Initialize an AutoDartEndpointWs instance.

        Parameters:
        - state (dict): The initial state of the entity.
        - session (AutoDartSession): The session used for communication.
        - endpoint (str): The API endpoint for the entity.
        - channel (str): The WebSocket channel.
        - ws_url (str): The WebSocket URL.
        - api_url (str): The base API URL.

        Returns:
        None
        """
        super().__init__(state, session, endpoint, api_url=api_url)
        self.ws = None
        self.channel = channel
        self.last_event = None
        self.task = None
        self.ws_url = ws_url
        self.event_cb = { name: defaultdict(list) for name in self.event_topics } 
        self.async_event_cb = { name: defaultdict(list) for name in self.event_topics }

    @property
    def connected(self) :
        return True if self.task and not self.task.done() else False 
    
    @property
    def state_topic(self) -> str:
        """Get the state topic for the entity."""
        return self.id + ".state"
    
    @property
    def event_topic(self) -> str:
        """Get the event topic for the entity."""
        return self.id + ".events"
        
    def connect(self, on_event_cb=None, on_state_cb=None) -> None:
        """Connect to the WebSocket channel."""
        self.task = asyncio.create_task(
            self.async_messages_task(on_event_cb, on_state_cb)
        )

    def disconnect(self) -> None:
        """Disconnect from the WebSocket channel."""
        self.task.cancel()
        self.task = None

    async def async_messages_task(self, on_event_cb=None, on_state_cb=None) -> None:
        """Asynchronously handle messages from the WebSocket channel."""
        try:
            async with self.session.session.ws_connect(url=self.ws_url, headers=await self.session.headers()) as ws:
                await self._subscribe_channel(ws, self.state_topic)
                await self._subscribe_channel(ws, self.event_topic)
                async for msg in ws: 
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        msg = msg.json()
                        topic = msg['topic'] 
                        if  topic == "info" :
                            continue
                        elif topic == self.state_topic :
                            await self.on_state_message(msg["data"])
                            if on_state_cb :
                                await on_state_cb(msg["data"])
                        elif topic == self.event_topic :
                            await self.on_event_message(msg["data"])
                            if on_event_cb :
                                await on_event_cb(msg["data"])
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        await self.on_event_message({'event' : 'error', 'data' : ws.exception()})
                        logger.error('ws connection closed with exception %s' % ws.exception())
                        break
                    elif msg.type == aiohttp.WSMsgType.CLOSED:
                        await self.on_event_message({'event' : 'disconnected'})
                        break
        except asyncio.CancelledError:
            pass
        except Exception as e :
            logger.exception(f'Uncatch exception in wait msg {e}')
        finally :
            await self.on_event_message({'event' : 'task_ended'})

    async def _subscribe_channel(self, ws, topic) -> None:
        """Subscribe to a WebSocket channel."""
        await ws.send_json(
            {
                "type": "subscribe",
                "channel": self.channel,
                "topic" : topic
            }
        )

    @property
    def ws_data(self) :
        if not self._state['state'] :
            self._state['state'] = {}
        return self._state['state']


    async def on_state_message(self, data) -> None:
        """Handle state messages from the WebSocket channel."""
        if not self._state['state'] :
            self._state['state'] = {}
        
        self.ws_data.update(data)

        event = data.get('event')
        
        if event :       
            for cb in self.async_event_cb["state"].get(event,[])  :
                await cb(self._state)
            for cb in self.event_cb["state"].get(event,[]) :       
                cb(self._state)    
                
        for cb in self.async_event_cb["state"].get(None,[]) :
            await cb(self._state)
        
        for cb in self.event_cb["state"].get(None,[]) :
            cb(self._state)

    async def on_event_message(self, data) -> None:
        """Handle event messages from the WebSocket channel."""
        self.last_event = data
        
        event = data.get('event')
        if event :       
            for cb in self.async_event_cb["events"].get(event,[])  :
                await cb(data)
            for cb in self.event_cb["events"].get(event,[]) :        
                cb(data)    
                
        for cb in self.async_event_cb["events"].get(None,[]) :
            await cb(data)
        
        for cb in self.event_cb["events"].get(None,[]) :
            cb(data)

                
    def register_async_callback(self, cb, event=None , topic="state") -> Callable[[], None]:
        """Register a callback for a specific event and topic."""
        #if event not in self.events :
        #    raise AutoDartInvalidStateException(f"Event not supported, allowed events are {','.join(self.events)}")        
        if topic not in self.event_topics :
            raise AutoDartInvalidStateException(f"Topic not supported, allowed topics are {','.join(self.event_topics)}")
        
        self.async_event_cb[topic][event].append(cb)
        
        def unregister() -> None:
            self.async_event_cb[topic][event].remove(cb)
        
        return unregister

    def register_callback(self, cb,event=None, topic="state") -> Callable[[], None]:
        """Register a callback for a specific event and topic."""
        #if event not in self.events :
        #    raise AutoDartInvalidStateException(f"Event not supported, allowed events are {','.join(self.events)}")        
        if topic not in self.event_topics :
            raise AutoDartInvalidStateException(f"Topic not supported, allowed topics are {','.join(self.event_topics)}")
        self.event_cb[topic][event].append(cb)
        def unregister() -> None:
            self.event_cb[topic][event].remove(cb)
        return unregister
