import time
from threading import Lock

from xapi.lrs_utils import fetch_xapi_statements_from_db, fetch_xapi_statements_from_db_for_user

class XAPIService:
    """
    XAPIService is a class that handles the fetching and updating of xAPI statements. It uses caching to 
    reduce the number of database queries and ensures thread safety during the update process.
    Attributes:
        statements (list): Cached xAPI statements.
        new_statements (list): Temporary storage for new xAPI statements during an update.
        last_fetched_time (float): Timestamp of the last fetch operation.
        cache_duration (int): Duration (in seconds) for which the cache is valid.
        is_updating (bool): Flag indicating if an update is currently in progress.
        lock (Lock): A threading lock to ensure thread safety during updates.
    Methods:
        fetch_statements():
            Fetches xAPI statements, either from cache or from the database. If an update is in progress, 
            it returns the cached statements. If the cache has expired or there are no cached statements, 
            it fetches fresh data from the database.
        update_statements():
            Updates the xAPI statements by fetching fresh data from the database or an external source. 
            This method acquires a lock to ensure thread safety during the update process. It simulates a 
            delay to represent the time taken to fetch and process the data.
    """
    def __init__(self, cache_duration=300):
        self.statements = None
        self.new_statements = None  # Will hold new data while updating
        self.last_fetched_time = None
        self.cache_duration = cache_duration  # Cache duration in seconds (e.g., 5 minutes)
        self.is_updating = False  # Flag to check if update is in progress
        self.lock = Lock()  # Lock to ensure thread-safety during update

    def fetch_statements(self):
        """
        Fetches xAPI statements, either from cache or from the database.
        This method checks if there is an ongoing update or if the cached data has expired.
        If an update is in progress, it returns the cached statements. If the cache has expired
        or there are no cached statements, it fetches fresh data from the database.
        Returns:
            list: A list of xAPI statements.
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
        Update the xAPI statements by fetching fresh data from the database or an external source.
        This method acquires a lock to ensure thread safety during the update process. It marks the 
        start of the update, simulates a long update process by fetching new xAPI statements from 
        the database, and then replaces the current statements with the new data. The lock is 
        released after the update is complete.
        Note:
            This method simulates a delay using `time.sleep(5)` to represent the time taken to 
            fetch and process the data.
        Raises:
            Any exceptions raised during the fetching of xAPI statements will be propagated.
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


class UserXAPIService:
    """
    A service class to handle xAPI statements for users.
    This class provides methods to fetch and update xAPI statements for users identified by their email addresses.
    It uses caching to minimize database queries and ensures thread-safety during updates.
    Attributes:
        user_statements (dict): A dictionary to hold xAPI statements for each user.
        new_user_statements (dict): A dictionary to hold new xAPI statements while updating.
        last_fetched_time (float): The timestamp of the last fetch operation.
        cache_duration (int): The duration (in seconds) for which the cache is valid.
        is_updating (bool): A flag to indicate if an update is in progress.
        lock (Lock): A lock to ensure thread-safety during updates.
    Methods:
        fetch_statements_for_user(email_of_user, query_params={}):
            Fetches xAPI statements for a specific user. This method checks if there is an ongoing update 
            or if the cached data has expired. If an update is in progress, it returns the cached statements. 
            If the cache has expired or there are no cached statements, it fetches fresh data from the database.
        update_statements_for_user(email_of_user, query_params={}):
            Updates the xAPI statements for a specific user by fetching fresh data from the database or an 
            external source. This method acquires a lock to ensure thread safety during the update process. 
            It simulates a delay to represent the time taken to fetch and process the data.
    """
    def __init__(self, cache_duration=300):
        self.user_statements = {}  # Dictionary to hold statements for each user
        self.new_user_statements = {}  # To hold new data while updating
        self.last_fetched_time = None
        self.cache_duration = cache_duration  # Cache duration in seconds (e.g., 5 minutes)
        self.is_updating = False  # Flag to check if update is in progress
        self.lock = Lock()  # Lock to ensure thread-safety during update

    def fetch_statements_for_user(self, email_of_user, query_params={}):
        """
        Fetches xAPI statements for a specific user.
        This function retrieves xAPI statements for a given user identified by their email.
        It first checks if there is an ongoing update process. If so, it returns cached statements.
        If there is no ongoing update or the cache has expired, it fetches fresh data from the database.
        Args:
            email_of_user (str): The email address of the user whose xAPI statements are to be fetched.
            query_params (dict, optional): Additional query parameters to filter the xAPI statements. Defaults to an empty dictionary.
        Returns:
            list: A list of xAPI statements for the specified user.
        """
        
        current_time = time.time()
        
        # Check if there is an ongoing update for the specific user
        if self.is_updating:
            print(f"Using cached statements for {email_of_user} while update is in progress.")
            return self.user_statements.get(email_of_user)  # Return old data
        
        # If no update or cache expired, fetch fresh data
        if (email_of_user not in self.user_statements or 
            current_time - self.last_fetched_time > self.cache_duration):
            print(f"Fetching fresh statements for {email_of_user} from DB.")
            self.user_statements[email_of_user] = fetch_xapi_statements_from_db_for_user(email_of_user, query_params)
            self.last_fetched_time = current_time
            
        return self.user_statements[email_of_user]

    def update_statements_for_user(self, email_of_user, query_params={}):
        """
        Update the xAPI statements for a specific user.
        This method acquires a lock to ensure thread safety, marks the start of the update process,
        fetches fresh xAPI statements for the given user from the database or an external source,
        and then updates the user's statements. The lock is released after the update is complete.
        Args:
            email_of_user (str): The email address of the user whose statements are to be updated.
            query_params (dict, optional): Additional query parameters to filter the xAPI statements. Defaults to an empty dictionary.
        Raises:
            Any exceptions raised during the fetching of xAPI statements will propagate up.
        Note:
            This method simulates a long update process by sleeping for 5 seconds.
        """
        
        self.lock.acquire()
        try:
            self.is_updating = True  # Mark the start of the update
            
            # Simulate a long update process (e.g., updating from DB or external source)
            print(f"Updating statements for {email_of_user}...")
            self.new_user_statements[email_of_user] = fetch_xapi_statements_from_db_for_user(email_of_user, query_params)  # Fetch fresh data
            time.sleep(5)  # Simulate time taken to fetch and process the data
            
            # Once the new data is ready, switch it to the current data
            self.user_statements[email_of_user] = self.new_user_statements[email_of_user]
            self.new_user_statements[email_of_user] = None
            self.is_updating = False  # Mark the end of the update
            print(f"Update complete for {email_of_user}.")
        finally:
            self.lock.release()
