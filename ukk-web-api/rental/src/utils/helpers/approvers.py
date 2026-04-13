import base64
import copy
from collections import defaultdict

import requests
from config import getenv
from pydantic import BaseModel

apiUrl = getenv("PUBLIC_MAIN", "https://dev-api.unais.com")


class ApproverSchema(BaseModel):
  approver: str
  sign_type: str
  approver_group: str
  approver_title: str | None = None
  name: str | None = None
  signature_default: str | None = None  # base64 or URL
  signature_with_stamp: str | None = None


GroupedApproversSchema = dict[str, dict[str, list[ApproverSchema]]]


def _mapping_grouped_approvers(approval_details: list, token: str, with_text: bool = True):
  """
  example: {
  "PT UNAIS" (Group),
  {
    "Disiapkan oleh" (Type):
    [
      {
        "approver": "name@UNAIS.id",
        "approver_name": "name",
        "approver_title": "",
        "approver_group": "PT UNAIS - Disiapkan oleh",
        "sign_type": "default",
        "name": "name",
        "signature_default": "base64image"
      }
    ]
    }
  }
  """
  grouped_approvers = defaultdict(lambda: defaultdict(list))

  for meta_approver in approval_details:
    if meta_approver["approvers"]:
      for approver in meta_approver["approvers"]:
        email = approver.get("approver")
        approver_name = approver.get("approver_name")
        approver_title = approver.get("approver_title")
        # sign_type = approver.get("sign_type")

        company = "Unknown Company"
        role = "Unknown Role"
        if approver.get("approver_group"):
          groups = approver.get("approver_group").split(sep=" - ")
          company = groups[0]
          role = groups[1] if len(groups) > 1 else "None"

        # Fetch signature info
        username, user_title, signature_default = fetch_signature(email, "default", token)
        _, _, signature_with_stamp = fetch_signature(email, "with_stamp", token)

        approver["name"] = username if username else approver_name
        approver["title"] = user_title if user_title else approver_title

        # if sign_type == "default":
        approver["signature_default"] = signature_default
        # elif sign_type == "with_stamp":
        approver["signature_with_stamp"] = signature_with_stamp

        grouped_approvers[company][role].append(approver)

  # Convert to list format for Jinja2 rendering
  result = []
  for company, roles in grouped_approvers.items():
    positions = []
    for role, approvers in roles.items():
      positions.append({"role": role, "approvers": approvers})
    result.append({"group": company, "positions": positions})

  return {"render_type": "grouped", "data": result, "with_text": with_text}


def _process_placement(approval_details: list, placement: dict, token: str):
  # Process approvers if they exist
  if "approvers" in placement:
    for approver in placement["approvers"]:
      if "data" in approver and isinstance(approver["data"], dict):
        data: dict = approver["data"]

        approval = next((item for item in approval_details if item["id"] == data.get("id")), data)

        email = approval.get("email")
        sign_type = approval.get("sign_type")

        data["sign_type"] = sign_type
        data["email"] = email
        data["name"] = approval.get("name")
        data["title"] = approval.get("title")

        if email:
          _, _, signature_default = fetch_signature(email, "default", token)
          _, _, signature_with_stamp = fetch_signature(email, "with_stamp", token)
          data["signature_default"] = signature_default
          data["signature_with_stamp"] = signature_with_stamp

  # Process children recursively if they exist
  if "children" in placement:
    for child in placement["children"]:
      _process_placement(approval_details, child, token)


def _mapping_sign_placements(approval_details: list, sign_placements: list, token: str):
  updated_placements = copy.deepcopy(sign_placements)
  raw_details = []
  for meta_approver in approval_details:
    if meta_approver["approvers"]:
      for approver in meta_approver["approvers"]:
        email = approver.get("approver")
        approver_name = approver.get("approver_name")
        approver_title = approver.get("approver_title")

        approver["email"] = email
        approver["name"] = approver_name
        approver["title"] = approver_title

        raw_details.append(approver)

  for placement in updated_placements:
    _process_placement(raw_details, placement, token)

  return {"render_type": "sign_placements", "data": updated_placements}


def get_approvers(approval_meta: dict | None, token: str, with_text: bool = True):
  if approval_meta:
    if approval_meta.get("sign_placements"):
      return _mapping_sign_placements(approval_meta.get("details", []), approval_meta.get("sign_placements", []), token)
    elif approval_meta.get("details"):
      return _mapping_grouped_approvers(approval_meta.get("details", []), token, with_text)
  return None


# async def fetch_signature(email: str, sign_type: str, token: str):
#   try:
#     endpoint = "v1/auth/users/signature" if sign_type == "default" else "v1/auth/users/signature-stamp"
#
#     async with httpx.AsyncClient(timeout=10) as client:
#       response = await client.get(
#         f"{apiUrl}/{endpoint}",
#         params={"email": email, "token": token},
#         headers={"Accept": "*/*"},
#       )
#       response.raise_for_status()
#
#       # Extract headers
#       username = response.headers.get("X-Username")
#       user_title = response.headers.get("X-UserTitle")
#
#       # Convert to base64 data URL
#       file_data = response.content
#       if file_data:
#         content_type = response.headers.get("Content-Type", "image/png")
#         base64_data = base64.b64encode(file_data).decode("utf-8")
#         data_url = f"data:{content_type};base64,{base64_data}"
#       else:
#         data_url = None
#
#       return username, user_title, data_url
#
#   except Exception as e:
#     print(f"[fetch_signature] Failed for {email=} {sign_type=}: {e}")
#     return None, None, None


def fetch_signature(email: str, sign_type: str, token: str):
  try:
    endpoint = "v1/auth/users/signature" if sign_type == "default" else "v1/auth/users/signature-stamp"

    response = requests.get(
      f"{apiUrl}/{endpoint}", params={"email": email, "token": token}, headers={"Accept": "*/*"}, stream=True
    )
    response.raise_for_status()

    # Extract username from custom header
    username = response.headers.get("X-Username")
    user_title = response.headers.get("X-UserTitle")
    file_data = response.content

    content_type = response.headers.get("Content-Type", "image/png")
    base64_data = base64.b64encode(file_data).decode("utf-8") if file_data else None
    data_url = f"data:{content_type};base64,{base64_data}" if file_data else None

    return username, user_title, data_url
  except Exception as e:
    print("fetch signature:", e)
    return None, None, None
