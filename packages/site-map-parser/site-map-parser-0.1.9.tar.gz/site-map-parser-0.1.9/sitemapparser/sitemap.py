class Sitemap:
    def __init__(self, loc, lastmod=None):
        """
        Representation of the <sitemap> element
        :param loc: String of the url
        :param lastmod: DateTime, The date of last modification of the file.
        """
        self.loc = loc
        self.lastmod = lastmod

    def __str__(self):
        return self.loc
