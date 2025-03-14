import json
import requests
import base64

def generate_token_and_authenticate(base_url, username, password):
    # Step 1: Login to retrieve JSON Web Token
    login_url = f"{base_url}/admin/account/login"
    login_payload = {
        "username": username,
        "password": password
    }
    
    login_response = requests.post(login_url, json=login_payload, headers={"Content-Type": "application/json"})
    
    if login_response.status_code != 200:
        raise Exception(f"Failed to login: {login_response.status_code} - {login_response.text}")
    
    json_web_token = login_response.json().get("json-web-token")

    if not json_web_token:
        raise Exception("Login response did not contain a JSON Web Token.")

    # Step 2: Generate API Key and Secret Key
    creds_url = f"{base_url}/admin/creds"
    creds_payload = {
        "scopes": [
            "all",
            "statements/write",
            "statements/read",
            "all/read",
            "state",
            "activities_profile",
            "agents_profile",
            "statements/read/mine"
        ]
    }
    creds_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {json_web_token}"
    }

    creds_response = requests.post(creds_url, json=creds_payload, headers=creds_headers)
    
    if creds_response.status_code != 200:
        raise Exception(f"Failed to generate credentials: {creds_response.status_code} - {creds_response.text}")

    creds_data = creds_response.json()
    api_key = creds_data.get("api-key")
    secret_key = creds_data.get("secret-key")
    print("API Key",api_key)
    print("Secret Key",secret_key)
    if not api_key or not secret_key:
        raise Exception("Credentials response did not contain API Key and/or Secret Key.")

    # Step 3: Encode API Key and Secret Key to Base64
    token = base64.b64encode(f"{api_key}:{secret_key}".encode()).decode()
    print("Token",token)

    return token

def send_data_to_lrs(json_file_path, lrs_url, base_url, username, password):
    # Generate the token
    auth_token = generate_token_and_authenticate(base_url, username, password)

    # Read the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        statements = json.load(file)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {auth_token}',
        'X-Experience-API-Version': '1.0.3'
    }

    # File to save user emails
    user_emails = set()

    for statement in statements:
        
        # Extract user email if available
        actor = statement.get("actor", {})
        mbox = actor.get("mbox")
        if mbox:
            user_emails.add(mbox)

        # Send statement to LRS
        response = requests.post(lrs_url, headers=headers, json=statement)
        if response.status_code == 200 or response.status_code == 204:
            print(f"Successfully sent statement {statement.get('id', 'unknown')}")
        else:
            
            print(f"Failed to send statement {statement.get('id', 'unknown')}: {response.status_code} - {response.text}")

    # Save unique emails to a file
    with open("user_emails.txt", "w") as email_file:
        for email in user_emails:
            email_file.write(f"{email}\n")

    print("User emails saved to user_emails.txt")
    

send_data_to_lrs("./generated_data/xapi_statements_combined.json", "http://localhost:8080/xapi/statements", "http://localhost:8080", "my_username", "my_password")