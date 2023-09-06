from src.coverageimporter import CoverageImporter
from src.codecov import CodeCovCoverage
from src.helpers import Helpers

if __name__ == '__main__':
    helpers = Helpers()
    coverage_importer = CoverageImporter()
    codecov_repositories = helpers.read_from_csv('large_scale_paper_codecov.csv')

    for codecov_repo in codecov_repositories:
       codecov = CodeCovCoverage(codecov_repo['org'],codecov_repo['repo'], codecov_repo['main_branch'])
       data = coverage_importer.codecov_data(codecov, helpers)
       helpers.save_into_file('large_scale_paper_codecov_result.csv', data)
