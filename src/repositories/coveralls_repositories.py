from .base import Repositories
from requests_html import HTMLSession
import requests
import urllib3

urllib3.disable_warnings()


class CoverallsRepository(Repositories):
    def __init__(self, organisation: str, request_headers: dict):
        super().__init__(organisation)
        self.request_headers = request_headers

    '''
        Method total number of paginations representing ALL pages with repositories for that Organisation in coveralls
        Coveralls.IO currently does not have an API for retrive all repositories covered  per organisation
        In fact, they don't have the concept of an organisation at all

        @param <request_headers: str> --> currently requires headers (each computer has its own headers)
            I will have to remove this as the base methods do not have this signature
        @return <int> --> total number of pages representing all repositories configured to have coveralls
    '''

    def get_total_pages(self) -> int:
        session = HTMLSession()
        url = f"https://coveralls.io/github/{self.organisation}?page=1"
        res = session.get(url, headers=self.request_headers, verify=False)
        page_elements = res.html.find('ul.pagination')
        if len(page_elements) == 0 or page_elements is None:
            return 1
        else:
            pagination = page_elements[0].find('a')
            array_size = len(pagination)
            length_elem = pagination[array_size - 2]
            return int(length_elem.find('a')[0].text)

    '''
        Method for scrapping repository names from organisation page in coveralls
        Based on the total number of paginations above, this will scrap each and retrieve the organisation
        name. Currently using requests_html for WebScrapping

        @param <request_headers: str> --> computer specific request headers
        @return <list> --> returns a list of all repository names
    '''

    def repositories(self) -> list:
        start_page = 1
        repo_names = []
        total_pages = self.get_total_pages()
        while start_page <= total_pages:
            session = HTMLSession()
            url = f"https://coveralls.io/github/{self.organisation}?page={start_page}"
            response = session.get(url, headers=self.request_headers)
            page_elements = response.html.find('div.repoChartInfo')
            for repo in page_elements:
                repository_name = repo.find('a')
                if not repository_name:
                    continue
                else:
                    try:
                        gh_url = f'https://api.github.com/repos/{self.organisation}/{repo}'
                        res = session.get(gh_url)
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
