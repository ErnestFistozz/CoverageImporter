from src.coverageimporter import CoverageImporter
from src.codecov import CodeCovCoverage
from src.helpers import Helpers

if __name__ == '__main__':
    helpers = Helpers()
    coverage_importer = CoverageImporter()
    codecov_repositories = helpers.repositories('codecov_repos.txt')

    for codecov_repo in codecov_repositories:
        codecov = CodeCovCoverage(codecov_repo[0], codecov_repo[1])
        data = coverage_importer.codecov_data(codecov, helpers)
        helpers.save_into_file('codecov_coverage_results.csv', data)
