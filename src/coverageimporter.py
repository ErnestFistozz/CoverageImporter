from .codecov import CodeCovCoverage
from .coveralls import CoverallsCoverage
from pydriller import Repository
from .helpers import Helpers
from .patch_extracts import PatchExtracts
from .crap_metric.commit_crap import CrapMetric
import logging as log

class CoverageImporter:

    def coveralls_data(self, coveralls: CoverallsCoverage, helpers: Helpers):
        git_url = f'https://github.com/{coveralls.org()}/{coveralls.repo()}.git'
        builds = coveralls.collect_builds_data()
        for build in builds:
            try:
                for commit in Repository(git_url, single = build['commit_sha']).traverse_commits():
                    coveralls_commit_files = coveralls.fetch_source_files(commit.hash)
                    executable_lines = executed_lines = commit_crappiness =  0 
                    patch_extracts = PatchExtracts()
                    crap_metric = CrapMetric()
                    if coveralls_commit_files:
                        for m in commit.modified_files:
                            coveral_file_path = helpers.index_finder(m.filename, coveralls_commit_files)
                            if coveral_file_path != -1:
                                coverage_array = coveralls.source_coverage_array( commit.hash,
                                                coveralls_commit_files[coveral_file_path])
                                if coverage_array: # if the coverage array is not empty
                                    modified_lines  = [ line_number[0] for line_number in m.diff_parsed['added'] ]
                                    executable_lines += len([1 for line_number in modified_lines  if isinstance(coverage_array[line_number - 1], int)])
                                    executed_lines += len([1 for line_number in modified_lines  if isinstance(coverage_array[line_number - 1], int) and coverage_array[line_number - 1] > 0])
                    # patch related files
                    patch_files = patch_extracts.patch_files(commit, coveralls_commit_files)
                    patch_size = patch_extracts.patch_sizes(commit, coveralls_commit_files)
                    build.update(patch_files)
                    build.update(patch_size)                    
                    # delta maintainability model
                    dmm_commit_size = commit.dmm_unit_size if not isinstance(commit.dmm_unit_size, type(None)) else 0
                    dmm_commit_complexity = commit.dmm_unit_complexity if not isinstance(commit.dmm_unit_complexity, type(None)) else 0
                    dmm_commit_interface = commit.dmm_unit_interfacing if not isinstance(commit.dmm_unit_interfacing, type(None)) else 0
                    delta_maintainibility_model = round((dmm_commit_size + dmm_commit_complexity + dmm_commit_interface)/3 , 3)
                    # CRAP Metric and Patch Coverage
                    if executable_lines == 0:
                        build['patch_coverage'] = 0
                        commit_crappiness = crap_metric.commit_dmm_crap_metric(dmm_commit_complexity,0)
                    else:
                        commit_crappiness = crap_metric.commit_dmm_crap_metric(dmm_commit_complexity, (executed_lines/executable_lines)*100)
                        build['patch_coverage'] = round((executed_lines/executable_lines)*100, 3)
                    # update dictionary to have delta maintainability and crap metric
                    build['repository_name'] = f'{coveralls.org()}/{coveralls.repo()}'
                    build['dmm_unit_size'] =  dmm_commit_size
                    build['dmm_unit_complexity'] =  dmm_commit_complexity
                    build['dmm_unit_interface'] =  dmm_commit_interface
                    build['dmm'] =  delta_maintainibility_model
                    build['crap_metric'] =  commit_crappiness
            except Exception:
                continue
        return builds
    
    def codecov_data(self,  codecov: CodeCovCoverage, helpers: Helpers):
        git_url = f'https://github.com/{codecov.org()}/{codecov.repo()}.git'
        builds = codecov.collect_build_data()
        for build in builds:
            try:
                for commit in Repository(git_url, single = build['commit_sha']).traverse_commits():
                    commit_report = codecov.commit_report(commit.hash) # will call the report API and return a response
                    codecov_commit_files = codecov.fetch_source_file_names(commit_report)
                    overall_coverage = codecov.computed_overall_coverage(commit_report)
                    patch_coverage_from_api = codecov.api_patch_coverage(commit_report)
                    executable_lines = executed_lines = commit_crappiness = 0 
                    patch_extracts = PatchExtracts()
                    crap_metric = CrapMetric()
                    if codecov_commit_files:
                        for m in commit.modified_files:
                            coveral_file_path = helpers.index_finder(m.filename, codecov_commit_files)
                            if coveral_file_path != -1:
                                coverage_array = codecov.file_line_coverage_array( commit_report,
                                                    codecov_commit_files[coveral_file_path])
                                if coverage_array:
                                    modified_lines  = [ line_number[0] for line_number in m.diff_parsed['added'] ]
                                    for line in modified_lines:
                                        for line_coverage_arr in coverage_array:
                                            if line == line_coverage_arr[0]:
                                                if  line_coverage_arr[1] == 0:
                                                    executed_lines += 1
                                                if line_coverage_arr[1] == 0 or line_coverage_arr[1] == 1 or line_coverage_arr[1] == 2:
                                                    executable_lines += 1
                    # patch size
                    patch_files = patch_extracts.patch_files(commit, codecov_commit_files)
                    patch_size = patch_extracts.patch_sizes(commit, codecov_commit_files)
                    build.update(patch_files)
                    build.update(patch_size)
                    # delta maintainability model
                    
                    dmm_commit_size = commit.dmm_unit_size if not isinstance(commit.dmm_unit_size, type(None)) else 0
                    dmm_commit_complexity = commit.dmm_unit_complexity if not isinstance(commit.dmm_unit_complexity, type(None)) else 0
                    dmm_commit_interface = commit.dmm_unit_interfacing if not isinstance(commit.dmm_unit_interfacing, type(None)) else 0
                    delta_maintainibility_model = round((dmm_commit_size + dmm_commit_complexity + dmm_commit_interface)/3 , 3)
                    # commit crappines and patch coverage
                    if executable_lines == 0:
                        commit_crappiness = crap_metric.commit_dmm_crap_metric(dmm_commit_complexity, 0)
                        build['patch_coverage'] = 0
                    else:
                        build['patch_coverage'] = round((executed_lines/executable_lines)*100, 3)
                        commit_crappiness = crap_metric.commit_dmm_crap_metric(dmm_commit_complexity, (executed_lines/executable_lines)*100)
                    # update dictionary to have delta maintainability model and crap metric
                    build['repository_name'] = f'{codecov.org()}/{codecov.repo()}'
                    build['api_patch_coverage'] = patch_coverage_from_api
                    build['computed_coverage'] = overall_coverage
                    build['dmm_unit_size'] = dmm_commit_size
                    build['dmm_unit_complexity'] = dmm_commit_complexity
                    build['dmm_unit_interface'] = dmm_commit_interface
                    build['dmm'] =  delta_maintainibility_model
                    build['crap_metric'] =  commit_crappiness
            except Exception:
                continue
        return builds

if __name__ == '__main__':
    print(__name__)