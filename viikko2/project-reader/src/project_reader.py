import toml
from urllib import request
from project import Project


class ProjectReader:
    def __init__(self, url):
        self._url = url

    def get_project(self):
        # tiedoston merkkijonomuotoinen sisältö
        content = request.urlopen(self._url).read().decode("utf-8")
        file = toml.loads(content)

        name = file["tool"]["poetry"]["name"]
        desc = file["tool"]["poetry"]["description"]
        license = file["tool"]["poetry"]["license"]
        authors = file["tool"]["poetry"]["authors"]
        dependencies = file["tool"]["poetry"]["dependencies"]
        dev_dependencies = file["tool"]["poetry"]["group"]["dev"]["dependencies"]

        # deserialisoi TOML-formaatissa oleva merkkijono ja muodosta Project-olio sen tietojen perusteella
        return Project(name, desc, license, [authors], [dependencies], [dev_dependencies])
        