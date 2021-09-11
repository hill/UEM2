PROJECT_NAME = "The University of Extrinsic Motivation API"
ENVIRONMENT = "development"
DEBUG = True
PERSIST_DB = True
ECHO_DATABASE = False
VERSION = "0.1.1"
API_PREFIX = "/api/v1"
BACKEND_CORS_ORIGINS = ["*"]

# Email stuff
EMAILS_ENABLED = False
EMAILS_FROM_NAME = "Extrinsic University"
EMAILS_FROM_EMAIL = "hello@motivation.university"
SMTP_TLS = True
SMTP_USER = "hello"
SMTP_PASSWORD = "password123"
EMAIL_RESET_TOKEN_EXPIRE_HOURS = 24