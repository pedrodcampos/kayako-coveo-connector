from src.factory import kayako_client

articles = kayako_client.insights.helpcenter.articles(
    include='section,category,locale_field')

print(articles[0])
