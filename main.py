from src.coverageimporter import CoverageImporter
from src.codecov import CodeCovCoverage
from src.coveralls import CoverallsCoverage
from src.helpers import Helpers

if __name__ == '__main__':
    helpers = Helpers()
    coverage_importer = CoverageImporter()
    codecov_repositories = helpers.read_from_csv('codecov_repositories.csv')
    coveralls_repositories = helpers.read_from_csv('coveralls_repositories.csv')

    for codecov_repo in codecov_repositories:
        codecov = CodeCovCoverage(codecov_repo['org'],codecov_repo['repo'], codecov_repo['main_branch'])
        data = coverage_importer.codecov_data(codecov, helpers, codecov_repo['language'])
        helpers.save_into_file('codecovdata.csv', data)

    # for coveralls_repo in codecov_repositories:
    #     coveralls = CoverallsCoverage(coveralls_repo['org'],coveralls_repo['repo'], coveralls_repo['main_branch'])
    #     data = coverage_importer.coveralls_data(coveralls, helpers, coveralls_repo['language'])
    #     helpers.csv_creator('coverallsdata.csv', data)