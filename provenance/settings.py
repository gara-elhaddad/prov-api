import os

HBP_IDENTITY_SERVICE_URL_V2 = "https://iam.ebrains.eu/auth/realms/hbp/protocol/openid-connect"
HBP_COLLAB_SERVICE_URL_V2 = "https://wiki.ebrains.eu/rest/v1/"
EBRAINS_IAM_CONF_URL = "https://iam.ebrains.eu/auth/realms/hbp/.well-known/openid-configuration"
EBRAINS_IAM_CLIENT_ID = os.environ.get("EBRAINS_IAM_CLIENT_ID")
EBRAINS_IAM_SECRET = os.environ.get("EBRAINS_IAM_SECRET")
SESSIONS_SECRET_KEY = os.environ.get("SESSIONS_SECRET_KEY")
BASE_URL = os.environ.get("PROV_API_BASE_URL")
