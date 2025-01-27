from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from dotenv import load_dotenv
import sentry_sdk
import os


# Loading environment variables from the .env file
load_dotenv()


# Secret key for signing JWTs
JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise ValueError("JWT_SECRET key is not defined in .env file")

JWT_ALGORITHM = 'HS256'
# Token validity period (in seconds)
JWT_EXP_DELTA_SECONDS = 3600


# Configuration de Sentry
SENTRY_DSN = os.getenv('SENTRY_DSN')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        integrations=[SqlalchemyIntegration()],
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        send_default_pii=True,
        debug=False
    )
else:
    print("SENTRY_DSN n'est pas défini. Sentry ne sera pas initialisé.")
