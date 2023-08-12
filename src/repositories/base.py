'''
@ This is a base class for all classes to get repositories
defines two methods 
    1. get_total_pages -> Repository API to get total pages
    2. repositories -> Repository API to get list of all repositories per organisation
'''

class Repositories:
    def __init__(self, organisation):
        self.organisation = organisation

    def repositories(self) -> list:
        pass
    
    def get_total_pages(self) -> int:
        pass