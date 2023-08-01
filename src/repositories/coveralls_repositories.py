from .base import Repositories
from requests_html import HTMLSession
import requests

class CoverallsRepository(Repositories):
    def __init__(self, organisation: str):
        super().__init__(organisation)
    
    def get_total_pages(self, request_headers: dict) -> int:
        session = HTMLSession()
        url = f"https://coveralls.io/github/{self.organisation}?page=1"
        res = session.get(url, headers=request_headers)
        page_elements = res.html.find('ul.pagination')
        if len(page_elements) == 0 or page_elements is None: 
            return 1
        else:
            pagination = page_elements[0].find('a')
            array_size = len(pagination)
            length_elem = pagination[array_size-2]
            return int(length_elem.find('a')[0].text)
        
    def repositories(self, request_headers: str) -> list:
        start_page = 1
        repo_names = []
        total_pages = self.get_total_pages()
        while start_page <= total_pages:
            session = HTMLSession()
            url = f"https://coveralls.io/github/{self.organisation}?page={start_page}"
            response = session.get(url, headers=request_headers)
            page_elements = response.html.find('div.repoChartInfo')
            for repo in page_elements:
                repository_name = repo.find('a')
                if not repository_name:
                    continue
                else:
                    try:
                        gh_url = f'https://api.github.com/repos/{self.organisation}/{repo}'
                        res = request_headers(gh_url)
                        if res.status_code != 200:
                            raise (KeyError, requests.RequestException)
                        org_project_name = repository_name[1].find('a')
                        repo_names.append({
                            "name": org_project_name[0].text,
                            "language": res.json()['language'],
                            "branch": res.json()['default_branch'],
                            "organisation": res.json()['organization']['login']
                        })
                    except (KeyError, requests.RequestException):
                        continue
            start_page += 1
        return repo_names
    
if __name__ == '__main__':
    codecov = CoverallsRepository('apache')