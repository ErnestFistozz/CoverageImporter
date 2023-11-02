from src.coverageimporter import CoverageImporter
from src.codecov import CodeCovCoverage
from src.coveralls import CoverallsCoverage
from src.helpers import Helpers

if __name__ == '__main__':
    coverage_importer = CoverageImporter()
    codecov_repositories = Helpers.repositories('codecov_repos.txt')
    coveralls_repositories = Helpers.repositories('coveralls_repos.txt')

    for codecov_repo in codecov_repositories:
        codecov = CodeCovCoverage(codecov_repo[0], codecov_repo[1])
        data = coverage_importer.codecov_data(codecov)
        Helpers.save_into_file('codecovdata.csv', data)

    for coveralls_repo in coveralls_repositories:
        coveralls = CoverallsCoverage(coveralls_repo[0], coveralls_repo[1])
        data = coverage_importer.coveralls_data(coveralls)
        Helpers.save_into_file('coverallsdata.csv', data)
