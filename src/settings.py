from os import environ

kayako_api_url = environ.get("KAYAKO_API_URL", None)
kayako_user = environ.get("KAYAKO_USER", None)
kayako_password = environ.get("KAYAKO_PASSWORD", None)
mongodb_url = environ.get("MONGODB_URL", None)
mongodb_database = environ.get("MONGODB_DATABASE", None)
