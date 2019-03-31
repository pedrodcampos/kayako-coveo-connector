from kayako.resources.helpcenter.articles import KayakoArticles
from kayako.resources.helpcenter.sections import KayakoSections
from kayako.resources.helpcenter.categories import KayakoCategories


class KayakoHelpcenter():
    def __init__(self, requests):
        self.categories = KayakoCategories(requests)
        self.sections = KayakoSections(requests)
        self.articles = KayakoArticles(requests)
