import asyncio
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent
from datetime import datetime
from plyer import notification
from utils.logger_utils import log_event  # Import the log_event function

class LiveChecker:
    def __init__(self):
        self.clients = {}
        self.running = False

    async def is_account_online(self, username):
        """Check if a specific account is live."""
        log_event(f"LiveChecker: Checking live status for account '{username}'.")
        
        if username not in self.clients:
            # Initialize a new client for the username if not already present
            client = TikTokLiveClient(unique_id=username)
            self.clients[username] = client

        client = self.clients[username]

        try:
            # Check if the user is live
            is_live = await client.is_live()
            log_event(f"LiveChecker: Account '{username}' is {'live' if is_live else 'not live'}.")
            return is_live
        except Exception as e:
            log_event(f"LiveChecker: Error checking live status for '{username}': {str(e)}", level="error")
            return False

    def get_current_time(self):
        """Get the current time in ISO 8601 format."""
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    async def on_connect(self, event: ConnectEvent):
        """Handle the connect event."""
        log_event(f"LiveChecker: Connected to TikTok live stream for user: {event.client.unique_id}")
        print(f"Connected to TikTok live stream for user: {event.client.unique_id}")

    async def on_comment(self, event: CommentEvent):
        """Handle the comment event."""
        log_event(f"LiveChecker: Comment from {event.user.nickname}: {event.comment}")
        print(f"Comment from {event.user.nickname}: {event.comment}")

    def stop(self):
        """Stop the live checker loop."""
        log_event("LiveChecker: Stopping the live check loop.")
        self.running = False