from fastapi import WebSocket


class ConnectionManager:
    """Class defining socket events."""

    def __init__(self) -> None:
        """Init method, keeping track of connections."""
        self.active_connections = []

    async def connect(self, websocket: WebSocket) -> None:
        """Connect event."""
        await websocket.accept()
        self.active_connections.append(websocket)

    @staticmethod
    async def send_personal_message(message: str, websocket: WebSocket) -> None:
        """Direct Message."""
        await websocket.send_text(message)

    def disconnect(self, websocket: WebSocket) -> None:
        """Disconnect event."""
        self.active_connections.remove(websocket)
