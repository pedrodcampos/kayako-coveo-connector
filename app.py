from src.factory import kayako_client
users = kayako_client.helpcenter.sections.get(id=1, include='locale_field')
print(users)
