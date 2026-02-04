import os
import time
from dotenv import load_dotenv
from modules import falcon

load_dotenv(".env")

this_month = time.strftime("%Y-%m")

if __name__ == "__main__":

    # get panvel servers alerts
    falcon_ = falcon.API(
        base_url=os.getenv("BASE_URL"),
        client_id=os.getenv("PANVEL_SERVERS_CLIENT_ID"),
        client_secret=os.getenv("PANVEL_SERVERS_CLIENT_SECRET"),
        bearer_token_file=os.getenv("BEARER_TOKEN_FILE"),
        ALERT_IDS_FILE=os.getenv("FALCON_ALERT_IDS"),
        FALCON_DETAILS_PATH=os.getenv("FALCON_DETAILS_PATH"),
        time_range=60,
    )
    falcon_.main_alerts(sufix="_servers")

    print(
        f"[*] Servers done, saved in {os.getenv('FALCON_DETAILS_PATH')}{this_month}_servers.csv"
    )

    # clean up old files
    os.remove(str(os.getenv("FALCON_ALERT_IDS")))
    os.remove(str(os.getenv("BEARER_TOKEN_FILE")))

    # get panvel workstations alerts
    falcon = falcon.API(
        base_url=os.getenv("BASE_URL"),
        client_id=os.getenv("PANVEL_DESKTOPS_CLIENT_ID"),
        client_secret=os.getenv("PANVEL_DESKTOPS_CLIENT_SECRET"),
        bearer_token_file=os.getenv("BEARER_TOKEN_FILE"),
        ALERT_IDS_FILE=os.getenv("FALCON_ALERT_IDS"),
        FALCON_DETAILS_PATH=os.getenv("FALCON_DETAILS_PATH"),
        time_range=int(os.getenv("TIME_RANGE_IN_DAYS")),
    )
    falcon.main_alerts(sufix="_desktops")

    print(
        f"[*] Desktops done, saved in {os.getenv('FALCON_DETAILS_PATH')}{this_month}_desktops.csv"
    )

    # clean up old files
    os.remove(str(os.getenv("FALCON_ALERT_IDS")))
    os.remove(str(os.getenv("BEARER_TOKEN_FILE")))
