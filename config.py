from dotenv import load_dotenv
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
