from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def main():
    """
    Read user's secret file and generate token.json to be used by emailing service.
    Since 2022 it's impossible to fully automate this process withour service account / google workspace.
    https://stackoverflow.com/questions/19766912/how-do-i-authorise-an-app-web-or-installed-without-user-intervention
    https://developers.google.com/identity/protocols/oauth2/service-account
    """
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
        token.write(creds.to_json())


if __name__ == "__main__":
    main()
