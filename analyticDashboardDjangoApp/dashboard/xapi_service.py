import time
from threading import Lock

from xapi.lrs_utils import fetch_xapi_statements_from_db

class XAPIService:
    def __init__(self, cache_duration=300):
        self.statements = None
        self.new_statements = None  # Will hold new data while updating
        self.last_fetched_time = None
        self.cache_duration = cache_duration  # Cache duration in seconds (e.g., 5 minutes)
        self.is_updating = False  # Flag to check if update is in progress
        self.lock = Lock()  # Lock to ensure thread-safety during update

    def fetch_statements(self):
        """
        Fetch statements based on cache expiration.
        If an update is in progress, serve the old data.
        """
        current_time = time.time()
        
        # If there is an ongoing update, return old data until update is complete
        if self.is_updating:
            print("Using cached statements while update is in progress.")
            return self.statements  # Return old data
        
        # If no update or cache expired, fetch fresh data
        if self.statements is None or (current_time - self.last_fetched_time > self.cache_duration):
            print("Fetching fresh statements from DB.")
            self.statements = fetch_xapi_statements_from_db()
            self.last_fetched_time = current_time
            
        return self.statements

    def update_statements(self):
        """
        Simulate updating statements. This method will lock the update process.
        """
        self.lock.acquire()
        try:
            self.is_updating = True  # Mark the start of the update
            
            # Simulate a long update process (e.g., updating from DB or external source)
            print("Updating statements...")
            self.new_statements = fetch_xapi_statements_from_db()  # Fetch fresh data
            time.sleep(5)  # Simulate time taken to fetch and process the data
            
            # Once the new data is ready, switch it to the current data
            self.statements = self.new_statements
            self.new_statements = None
            self.is_updating = False  # Mark the end of the update
            print("Update complete.")
        finally:
            self.lock.release()