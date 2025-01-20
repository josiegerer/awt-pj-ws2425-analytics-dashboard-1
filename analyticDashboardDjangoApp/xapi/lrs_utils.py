import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
import psycopg2
from psycopg2.extras import RealDictCursor

def login_and_get_token():
    """
    Logs into the admin account and retrieves the JSON Web Token.
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
    Creates a new API and Secret key with the "all" scope if no suitable keys are found.
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
    Retrieves the API and Secret keys with the "all" or "read" scope using the provided JSON Web Token.
    If no such keys exist, creates a new one.
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
    Fetches xAPI statements using the provided API and Secret keys.
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
    A Django view to automate retrieval of keys/secrets and fetch xAPI statements.
    """
    print(query_params)
    json_web_token = login_and_get_token()
    api_key, secret_key = get_api_and_secret_keys_with_all_or_read_scope(json_web_token)
    statements = fetch_xapi_statements(api_key, secret_key, query_params, path)
    return statements

def get_all_xapi_statements():
    """
    Fetches all xAPI statements.
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
    Fetches xAPI statements from a PostgreSQL database using the provided query parameters.
    """
    conn = psycopg2.connect(
        dbname="database",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
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

