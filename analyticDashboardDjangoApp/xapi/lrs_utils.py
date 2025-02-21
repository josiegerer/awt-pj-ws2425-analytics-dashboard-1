import json
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
import psycopg2
from psycopg2.extras import RealDictCursor

def login_and_get_token():
    """
    Authenticates with the Learning Record Store (LRS) and retrieves a JSON Web Token (JWT).
    This function sends a POST request to the LRS admin login endpoint using the admin username
    and password specified in the settings. If the login is successful, it returns the JWT token
    from the response.
    Returns:
        str: The JSON Web Token (JWT) retrieved from the LRS upon successful authentication.
    Raises:
        Exception: If the login request fails (i.e., the status code is not 200), an exception is raised
                   with the error message from the response.
    """
    
    base_url = settings.LRS_URL
    login_endpoint = f"{base_url}/admin/account/login"
    login_payload = {
        "username": settings.LRS_ADMIN_USERNAME,  # Replace with your admin username
        "password": settings.LRS_ADMIN_PASSWORD   # Replace with your admin password
    }

    login_response = requests.post(login_endpoint, json=login_payload)

    if login_response.status_code != 200:
        raise Exception(f"Failed to login: {login_response.text}")

    return login_response.json().get("json-web-token")

def create_new_api_secret_key(json_web_token):
    """
    Creates new API and Secret keys by making a POST request to the LRS credentials endpoint.
    Args:
        json_web_token (str): The JSON Web Token used for authorization.
    Returns:
        tuple: A tuple containing the new API key and Secret key.
    Raises:
        Exception: If the request to create new credentials fails.
    """
    
    base_url = settings.LRS_URL
    create_creds_endpoint = f"{base_url}/admin/creds"
    creds_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {json_web_token}"
    }
    creds_payload = {
        "scopes": [
            "all"
        ]
    }

    create_response = requests.post(create_creds_endpoint, headers=creds_headers, json=creds_payload)

    if create_response.status_code != 200:
        raise Exception(f"Failed to create new API and Secret keys: {create_response.text}")

    new_creds = create_response.json()
    return new_creds["api-key"], new_creds["secret-key"]

def get_api_and_secret_keys_with_all_or_read_scope(json_web_token):
    """
    Retrieve API and Secret keys with 'all' or 'all/read' scope from the Learning Record Store (LRS).
    This function sends a GET request to the LRS credentials endpoint using the provided JSON Web Token (JWT).
    It then parses the response to find credentials that have either 'all' or 'all/read' scope. If such credentials
    are found, their API key and Secret key are returned. If no suitable credentials are found, a new API and Secret
    key are created and returned.
    Args:
        json_web_token (str): The JSON Web Token used for authorization to access the LRS credentials endpoint.
    Returns:
        tuple: A tuple containing the API key and Secret key.
    Raises:
        Exception: If the request to the LRS credentials endpoint fails or returns a non-200 status code.
    """
    
    base_url = settings.LRS_URL
    creds_endpoint = f"{base_url}/admin/creds"
    creds_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {json_web_token}"
    }

    creds_response = requests.get(creds_endpoint, headers=creds_headers)

    if creds_response.status_code != 200:
        raise Exception(f"Failed to retrieve API and Secret keys: {creds_response.text}")

    credentials = creds_response.json()

    for cred in credentials:
        scopes = cred.get("scopes", [])
        if "all" in scopes or "all/read" in scopes:
            return cred["api-key"], cred.get("secret-key")

    # If no suitable keys found, create a new one
    return create_new_api_secret_key(json_web_token)

def fetch_xapi_statements(api_key, secret_key, query_params={},path="xapi/statements"):    
    
    """
    Fetches xAPI statements from a Learning Record Store (LRS).
    Args:
        api_key (str): The API key for authentication.
        secret_key (str): The secret key for authentication.
        query_params (dict, optional): A dictionary of query parameters to filter the xAPI statements. Defaults to {}.
        path (str, optional): The endpoint path for fetching xAPI statements. Defaults to "xapi/statements".
    Returns:
        dict: A dictionary containing the xAPI statements.
    Raises:
        Exception: If the request to the LRS fails, an exception is raised with the error message.
     """
    
    base_url = settings.LRS_URL
    xapi_endpoint  = f"{base_url}{path}"
    print(xapi_endpoint)
    xapi_version = "1.0.3"

    headers = {
        "Content-Type": "application/json",
        "X-Experience-API-Version": xapi_version
    }

    auth = HTTPBasicAuth(api_key, secret_key)

    response = requests.get(xapi_endpoint, headers=headers, params=query_params, auth=auth)

    if response.status_code != 200:
        raise Exception(f"Failed to retrieve xAPI statements: {response.text}")

    return response.json()

def get_xapi_statements(query_params={}, path="/xapi/statements"):
    """
    Fetches xAPI statements based on the provided query parameters.
    Args:
        query_params (dict, optional): A dictionary of query parameters to filter the xAPI statements. Defaults to an empty dictionary.
        path (str, optional): The API endpoint path for fetching xAPI statements. Defaults to "/xapi/statements".
    Returns:
        list: A list of xAPI statements that match the query parameters.
    """
    
    print(query_params)
    json_web_token = login_and_get_token()
    api_key, secret_key = get_api_and_secret_keys_with_all_or_read_scope(json_web_token)
    statements = fetch_xapi_statements(api_key, secret_key, query_params, path)
    return statements

def get_all_xapi_statements():
    """
    Fetches all xAPI statements from the Learning Record Store (LRS).
    This function retrieves all xAPI statements by making repeated requests to the LRS
    until there are no more statements to fetch. It handles pagination by following the
    'more' field in the response and adjusts the limit parameter to fetch a large number
    of statements in each request.
    Returns:
        list: A list of all xAPI statements retrieved from the LRS.
    """
    
    statements = []
    more = True
    
    path="/xapi/statements?limit=2000000"     
    # Fetch all statements
    while more:
        response = get_xapi_statements(path=path)
        statements.extend(response.get('statements', []))
        path = response.get('more', '')
        if "limit=50" in path:
            path = path.replace("limit=50", "limit=2000000")
        if path == '':
            more = False
    
    return statements
def fetch_xapi_statements_from_db(query_params={}):
    """
    Fetches xAPI statements from the database based on the provided query parameters.
    Args:
        query_params (dict, optional): A dictionary of query parameters to filter the xAPI statements.
            The keys should be the column names and the values should be the values to filter by.
            Defaults to an empty dictionary.
    Returns:
        list: A list of dictionaries, where each dictionary represents an xAPI statement with the following keys:
            - statement_id: The ID of the xAPI statement.
            - timestamp: The timestamp of the xAPI statement.
            - statement_payload: The payload of the xAPI statement.
    Raises:
        psycopg2.DatabaseError: If there is an error connecting to or querying the database.
    Note:
        Ensure that the database connection details are set in the environment variables.
    """
    conn = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    query = """
    SELECT 
    xs.id AS statement_id,
    xs.timestamp,
    xs.payload AS statement_payload FROM 
    xapi_statement xs


 """
    params = []

    for key, value in query_params.items():
        query += f" AND {key} = %s"
        params.append(value)

    cursor.execute(query, params)
    statements = cursor.fetchall()

    cursor.close()
    conn.close()

    return statements

def fetch_xapi_statements_from_db_for_user(email_of_user, query_params={}):
    """
    Fetches xAPI statements from the database for a specific user.
    This function connects to a PostgreSQL database using credentials specified in the settings.
    It retrieves xAPI statements associated with the given user's email address. Additional
    query parameters can be provided to filter the results.
    Args:
        email_of_user (str): The email address of the user whose xAPI statements are to be fetched.
        query_params (dict, optional): A dictionary of additional query parameters to filter the results.
            Defaults to an empty dictionary.
    Returns:
        list: A list of dictionaries representing the xAPI statements for the specified user.
    Raises:
        psycopg2.DatabaseError: If there is an error connecting to the database or executing the query.
    """
    
    conn = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    query = """
    SELECT * FROM statement_to_actor 
    JOIN xapi_statement xs ON xs.statement_id = statement_to_actor.statement_id
    WHERE actor_ifi = %s;
    """
    params = [f"mbox::mailto:{email_of_user}"]

    for key, value in query_params.items():
        query += f" AND {key} = %s"
        params.append(value)

    cursor.execute(query, params)
    statements = cursor.fetchall()

    cursor.close()
    conn.close()

    return statements

def fetch_all_activities_from_db():
    """
    Fetches all unique activity IRIs from the database.
    This function connects to a PostgreSQL database using psycopg2, executes a query to retrieve all activity IRIs from the 'activity' table,
    and returns a set of unique activity IRIs.
    Returns:
        set: A set of unique activity IRIs.
    Raises:
        psycopg2.DatabaseError: If there is an error connecting to the database or executing the query.
    """
    
    #TODO:use environment variables for database connection 
    conn = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    query = """
    SELECT activity_iri  FROM activity;
   
    """
    cursor.execute(query)
    statements = cursor.fetchall()

    cursor.close()
    conn.close()
    
    statementsJson = json.loads(json.dumps(statements))
    activities = set()
    
    for statement in statementsJson:
        activity_iri = statement.get("activity_iri")
        if activity_iri:
            activities.add(activity_iri)

    return activities

