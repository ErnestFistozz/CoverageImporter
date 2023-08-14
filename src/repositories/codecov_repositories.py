from .base import  Repositories
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class CodeCovRepositories(Repositories):
    def __init__(self, organisation: str):
        super().__init__(organisation)
    '''
    method to retrieve the total number of pages from codecov
    uses the codecov repository API (which expects an organisation name or username)
    username/organisation name is instatiated with object creation

    @return <int> total number of pages --> each page contains 10 repositories
    '''
    def get_total_pages(self) -> int:
        try:
            url = f'https://codecov.io/api/v2/gh/{self.organisation}/repos?active=true'
            res = requests.get(url)
            if res.status_code != 200:
                raise (requests.RequestException, KeyError)
            return res.json()['total_pages']
        except (requests.RequestException, KeyError):
            return None
    '''
        method to retriev all repositories
        iterates all pages based on the get_total_pages method above
        @return dict {
        name --> repository name
        language --> language of which the repository is written in 
        branch --> main branch (default branch), whilst the main branch can be any other branch other than main/master
            we assume main/master represent production code
        organisation --> this is the organisation or username 
        }
    '''
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