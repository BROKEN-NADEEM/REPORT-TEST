from flask import Flask, request
import requests

app = Flask(__name__)

# Facebook Page Access Token and Verify Token
PAGE_ACCESS_TOKEN = "YOUR_PAGE_ACCESS_TOKEN"
VERIFY_TOKEN = "YOUR_VERIFY_TOKEN"
GROUP_ID = "YOUR_GROUP_ID"
LOCKED_NAME = "Locked Group Name"

# Function to set group name
def set_group_name(group_id, new_name):
    url = f"https://graph.facebook.com/v12.0/{group_id}"
    payload = {
        "name": new_name,
        "access_token": PAGE_ACCESS_TOKEN
    }
    response = requests.post(url, data=payload)
    return response.json()

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        verify_token = request.args.get("hub.verify_token")
        if verify_token == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verification token"
    elif request.method == "POST":
        data = request.json
        # Monitor for group name change
        if "changes" in data:
            for change in data["changes"]:
                if change["field"] == "name" and change["value"] != LOCKED_NAME:
                    # Reset group name to LOCKED_NAME
                    set_group_name(GROUP_ID, LOCKED_NAME)
        return "EVENT_RECEIVED"

if __name__ == "__main__":
    app.run(port=5000)
