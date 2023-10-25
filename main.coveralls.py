from src.coverageimporter import CoverageImporter
from src.coveralls import CoverallsCoverage
from src.helpers import Helpers

if __name__ == '__main__':
    helpers = Helpers()
    coverage_importer = CoverageImporter()
    # coveralls_repositories = helpers.read_from_csv('large_scale_paper_coveralls.csv')
    # coveralls_repositories = helpers.read_from_csv('large_scale_paper_coveralls.csv')
    coveralls_repositories = helpers.repositories('coveralls_repos.txt')
    for coveralls_repo in coveralls_repositories:
        print(f'ORGANISATION:{coveralls_repo[0]}')
        print(f'REPOSITORY: {coveralls_repo[1]}')
        coveralls = CoverallsCoverage(coveralls_repo[0], coveralls_repo[1])
        data = coverage_importer.coveralls_data(coveralls, helpers)
        helpers.save_into_file('coverall_coverage_results.csv', data)
