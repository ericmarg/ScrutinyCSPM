import json

def storage_trasformation(json_content: str):
    data = json.loads(json_content)

    storage_dict = []
    provider = "azure"

    for storage_account in data:

        storage_dict_item = {
            "name": storage_account["name"],
            "provider": "azure",
            "region": storage_account["location"],
            "all_public_access_blocked": (storage_account.get("allow_blob_public_access", False) and storage_account.get("public_network_access", False) == "Disabled"),
            "versioning_enabled": False if storage_account.get("versioning_enabled", False) is None else True,
            "provider_specific": {'MFADeleteEnabled': False},
            "id": storage_account["id"]
        }

        storage_dict.append(storage_dict_item)
    return storage_dict