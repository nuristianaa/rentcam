import ssl

import jwt
import requests
from config import getenv
from jwt import PyJWKClient
from utils.helpers.number_text import generate_random_string

client_id = getenv("MSAL_CLIENT_ID", "120c11c0-ad14-4ebd-b5d4-eb271c87e7ce")
tenant_id = getenv("MSAL_TENANT_ID", "b299b3a0-3c80-4197-999e-234442c38b5e")


def check_jwt_azure(token: str):
  stat = "success"
  msg = None
  name = None
  email = None
  role_code = None
  password = None
  user_id = None
  ssl._create_default_https_context = ssl._create_unverified_context
  jwks_url = f"https://login.microsoftonline.com/{tenant_id}/discovery/keys"
  jwks_client = PyJWKClient(jwks_url)
  signing_key = jwks_client.get_signing_key_from_jwt(token)
  try:
    decoded = jwt.decode(
      token,
      signing_key.key,
      algorithms=["RS256"],
      audience="00000003-0000-0000-c000-000000000000",
      options={"verify_exp": True, "verify_signature": False},
    )
    # print("✅ Token is valid")
    # print(json.dumps(decoded, indent=2))
    try:
      name = decoded["given_name"] + " " + decoded["family_name"]
    except:
      name = decoded["name"]

    try:
      email = decoded["email"]
    except:
      email = decoded["unique_name"]

    try:
      role_code = decoded["idtyp"]
    except:
      role_code = "user"

    user_id = decoded["oid"]

    try:
      password = decoded["puid"] + "-" + decoded["sid"]
    except:
      password = generate_random_string(16)

  except jwt.exceptions.InvalidSignatureError:
    stat = "failed"
    msg = "❌ Signature verification failed"
  except jwt.exceptions.ExpiredSignatureError:
    stat = "failed"
    msg = "❌ Token expired"
  except jwt.exceptions.InvalidAudienceError:
    stat = "failed"
    msg = "❌ Invalid audience"
  except jwt.exceptions.InvalidIssuerError:
    stat = "failed"
    msg = "❌ Invalid issuer"
  except Exception as e:
    stat = "failed"
    msg = f"❌ Other error: {e}"

  return {
    "status": stat,
    "msg": msg,
    "user_id": user_id,
    "name": name,
    "email": email,
    "role_code": role_code,
    "password": password,
  }


def get_msal_profile(user_id: str, access_token: str):
  """
  Get MSAL profile from access token.

  Args:
    access_token (str): The access token to decode.

  Returns:
    dict: A dictionary containing the decoded profile information.
  """
  try:
    fields = "displayName,companyName,mail,mobilePhone,jobTitle,officeLocation,department,usageLocation"
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}?$select={fields}"

    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    profile = response.json()
    return profile
  except jwt.DecodeError as e:
    raise ValueError(f"Invalid access token: {e}")
