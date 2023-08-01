from .base import  Repositories
import requests

class CodeCovRepositories(Repositories):
    def __init__(self, organisation: str):
        super().__init__(organisation)
     
    def get_total_pages(self) -> int:
        try:
            url = f'https://codecov.io/api/v2/gh/{self.organisation}/repos?active=true'
            res = requests.get(url)
            if res.status_code != 200:
                raise (requests.RequestException, KeyError)
            return res.json()['total_pages']
        except (requests.RequestException, KeyError):
            return None

    def repositories(self) -> list:
        pages = self.get_total_pages()
        data = []
        if pages != 0 and pages is not None:
            for page in range(1, pages + 1):
                try:
                    url = f'https://codecov.io/api/v2/gh/{self.organisation}/repos?active=true&page={page}'
                    res = requests.get(url)
                    if res.status_code != 200:
                        raise (requests.RequestException, KeyError)
                    data.extend( [{
                        "name": repos['name'],
                        "language": repos['language'],
                        "branch": repos['branch'],
                        "organisation": repos['author']['username']
                        }
                        for repos in res.json()['results']])
                except (requests.RequestException, KeyError):
                    continue
        return data

if __name__ == '__main__':
    codecov = CodeCovRepositories('apache')