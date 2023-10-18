import pandas as pd
import matplotlib.pyplot as plt

'''
0 - 20
20 - 50
50 - 70
70 - 100
100+
'''

# header_names = [ 'date', 'commitHash', 'coverage_change', 'coverage', 'branch',
#                 'code_patch_size', 'test_patch_size', 'config_patch_size',
#                 'test_files', 'code_files', 'test_code_files', 'other_files',
#                 'patch_coverage', 'repository_name', 'dmm_unit_size',
#                 'dmm_unit_complexity', 'dmm_unit_interface', 'dmm', 'crap_metric'
#                 ]

header_names = ['date', 'commitHash', 'coverage', 'branch', 'repository_name',
                'code_patch_size', 'test_patch_size', 'config_patch_size',
                'test_files', 'code_files', 'test_code_files', 'other_files',
                'patch_coverage', 'dmm_unit_size',
                'dmm_unit_complexity', 'dmm_unit_interface', 'dmm', 'crap_metric'
                ]

# df = pd.read_csv('coverallsdata.csv', encoding='utf-8', header=None)

# projects = [ "commons-collections", "bookkeeper", "commons-rng",
#             "commons-fileupload", "servicecomb-java-chassis", "carbondata",
#             "commons-io", "commons-compress", "commons-math", "commons-codec"]
# projects = [ "apache/commons-collections", "apache/commons-io", "apache/commons-math",
#             "apache/commons-validator", "ARMmbed/mbed-ls", "bitwalker/timex", "broadinstitute/firecloud-orchestration",
#             "containers/virtcontainers", "coreos/alb-ingress-controller", "damianszczepanik/cucumber-reporting",
#             "dask/dask", "doanduyhai/Achilles", "dropwizard/dropwizard", "F5Networks/k8s-bigip-ctlr", "Gillespie59/eslint-plugin-angular",
#             "HazyResearch/deepdive", "ikawaha/kagome", "ilovepi/Compiler", "jknack/handlebars.java",
#             "joel-costigliola/assertj-core", "mailgun/kafka-pixy", "MITLibraries/topichub", "platinumazure/eslint-plugin-qunit",
#             "PragTob/benchee", "ShiftForward/apso", "spatialmodel/inmap", "terasolunaorg/terasoluna-gfw" ]

projects = ["apache/commons-collections", "apache/commons-io", "apache/commons-math",
            "ARMmbed/mbed-ls" ] # "bitwalker/timex"

# df = pd.read_csv('large_scale_paper_coveralls_result.csv', encoding='utf-8', names=header_names)
# print(df['repository_name'])
distibution_data = []
for project in projects:
    # df = pd.read_csv('large_scale_paper_coveralls_result.csv', encoding='utf-8', names=header_names)
    df = pd.read_csv('apache_coveralls_test_results.csv', encoding='utf-8', names=header_names)
    filtered = df.query("repository_name == @project")  # works perfectly
    # filtered = df[df['repository_name'] == project.lower()]
    zero = []
    zero_to_25 = []
    twenty5_to_50 = []
    # fifty = []
    fifty_to_75 = []
    seventy5_to_100 = []
    hundred = []
    for i, row in filtered.iterrows():
        commit_patch = float(row[12])
        if commit_patch == 0:
            zero.append(commit_patch)
        elif 0 < commit_patch < 25:
            zero_to_25.append(commit_patch)
        elif 25 < commit_patch <= 50:
            twenty5_to_50.append(commit_patch)
        elif 50 < commit_patch <= 75:
            fifty_to_75.append(commit_patch)
        elif 75 < commit_patch < 100:
            seventy5_to_100.append(commit_patch)
        elif commit_patch == 100:
            hundred.append(commit_patch)
    print(f'Project Name: {project} = {len(filtered)}')
    if len(filtered) > 0:
        distibution_data.append([project,  # os.path.splitext(project[0])[0].strip('CommitsDistMaster'),
                                 (len(zero) / len(filtered)) * 100,
                                 (len(zero_to_25) / len(filtered)) * 100,
                                 (len(twenty5_to_50) / len(filtered)) * 100,
                                 (len(fifty_to_75) / len(filtered)) * 100,
                                 (len(seventy5_to_100) / len(filtered)) * 100,
                                 (len(hundred) / len(filtered)) * 100])

data_frame = pd.DataFrame(distibution_data,
                          columns=['repositories', '0', '0-25', '25-50', '50-75', '75-100', '100'])
data_frame.plot(x='repositories', kind='barh', stacked=True
                , xlabel='percentage (%)', ylabel='repositories', title='Python Algorithm')
plt.legend(loc="lower right", bbox_to_anchor=(1., 1.02), borderaxespad=0., ncol=4)
# plt.savefig('./outputs/all_branch_commit_size_dist.pdf')
plt.show()
