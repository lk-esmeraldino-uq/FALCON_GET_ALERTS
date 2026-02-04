"""
This module provides a Falcon class for interacting with the Falcon API.
"""

import json
import requests
import time
from modules import utils

this_month = time.strftime("%Y-%m")
separator = ";"


class API:
    """
    A class for interacting with the Falcon API.

    Attributes:
        base_url (str): The base URL for the Crowdstrike API.
        client_id (str): The client ID for the Crowdstrike API.
        client_secret (str): The client secret for the Crowdstrike API.
    """

    def __init__(
        self,
        base_url,
        client_id,
        client_secret,
        bearer_token_file,
        ALERT_IDS_FILE,
        FALCON_DETAILS_PATH,
        time_range=30,
    ) -> None:
        """
        Initializes a Falcon instance with the given base_url, client_id, and client_secret.

        Args:
            base_url (str): The base URL for the Crowdstrike API.
            client_id (str): The client ID for the Crowdstrike API.
            client_secret (str): The client secret for the Crowdstrike API.
        """
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.bearer_token_file = bearer_token_file
        self.ALERT_IDS_FILE = ALERT_IDS_FILE
        self.FALCON_DETAILS_PATH = FALCON_DETAILS_PATH
        self.time_range = time_range

    def get_auth2_token(self):
        """
        Authenticates with the Crowdstrike API and returns the access token.

        Returns:
            str: The access token for the Crowdstrike API.
        """
        url = f"{self.base_url}/oauth2/token"

        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        response = requests.post(url, data=payload, timeout=60)
        token = response.json().get("access_token")

        utils.save_json(token, self.bearer_token_file)

        print("[*] Token created")
        return token

    def check_auth2_token(self):
        """
        Checks if the access token is valid and returns it if it is, otherwise it gets a new one.
        """
        if not utils.check_lifetime(self.bearer_token_file):
            return self.get_auth2_token()
        else:
            return utils.load_json(self.bearer_token_file)

    def get_alert_ids(self):
        filter = f"filter=created_timestamp:>='now-{self.time_range}d'%2Bseverity:>3%2Btype:!'thirdparty'%2Btype:!'cwpp-image-scan-detections'&limit=5000"
        url = f"{self.base_url}/alerts/queries/alerts/v2?{filter}"

        payload = {}
        headers = {"Authorization": f"Bearer {self.check_auth2_token()}"}

        response = requests.request(
            "GET", url, headers=headers, data=payload, timeout=60
        )

        response = json.loads(response.text)

        return response

    def get_alert_detail(self, alerts_id):

        url = f"{self.base_url}/alerts/entities/alerts/v2"

        payload = json.dumps({"composite_ids": alerts_id})
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.check_auth2_token()}",
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        response = json.loads(response.text)

        return response

    def main_alerts(self, sufix=""):

        if not utils.check_lifetime(self.ALERT_IDS_FILE, 60 * 60 * 24):
            utils.save_json(self.get_alert_ids(), self.ALERT_IDS_FILE)

        alert_ids = utils.load_json(self.ALERT_IDS_FILE).get("resources")
        if not alert_ids:
            alert_ids = []

        parts = [alert_ids[i : i + 100] for i in range(0, len(alert_ids), 100)]

        fields = [
            "name",
            "product",
            "created_timestamp",
            "falcon_host_link",
            "tactic",
            "tactic_id",
            "technique",
            "technique_id",
            "severity_name",
        ]
        final_details = [""]

        # headers
        final_details.append(f"{separator}".join(fields) + "\n")

        for part in parts:
            details = self.get_alert_detail(part).get("resources")
            if not details:
                details = []

            # content
            for i in details:
                line = []
                for field in fields:
                    (line.append(i.get(field)) if i.get(field) else line.append(""))

                final_details.append(f"{separator}".join(line) + "\n")

        utils.create_folders(self.FALCON_DETAILS_PATH)

        final_details = "".join(final_details)

        utils.save_csv(
            final_details, f"{self.FALCON_DETAILS_PATH}{this_month}{sufix}.csv"
        )

        # created_timestamp
        # falcon_host_link
        # tactic_id
        # technique_id
        # severity_name

        # TODO save to sharepoint
