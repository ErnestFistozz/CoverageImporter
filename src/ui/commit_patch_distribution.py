import pandas as pd
import matplotlib.pyplot as plt

header_names = [ 'date', 'commitHash', 'api_coverage', 'branch', 
                'code_patch_size', 'test_patch_size', 'config_patch_size',
                'test_files', 'code_files', 'test_code_files', 'other_files',
                'patch_coverage', 'repository_name', 'computed_coverage', 'dmm_unit_size',
                'dmm_unit_complexity', 'dmm_unit_interface', 'dmm', 'crap_metric'
                ]


projects = [ "apache/commons-collections", "apache/commons-io", "apache/commons-math",
            "apache/commons-validator", "ARMmbed/mbed-ls", "bitwalker/timex", "broadinstitute/firecloud-orchestration",
            "containers/virtcontainers", "coreos/alb-ingress-controller", "damianszczepanik/cucumber-reporting",
            "dask/dask", "doanduyhai/Achilles", "dropwizard/dropwizard", "F5Networks/k8s-bigip-ctlr", "Gillespie59/eslint-plugin-angular",
            "HazyResearch/deepdive", "ikawaha/kagome", "ilovepi/Compiler", "jknack/handlebars.java",
            "joel-costigliola/assertj-core", "mailgun/kafka-pixy", "MITLibraries/topichub", "platinumazure/eslint-plugin-qunit",
            "PragTob/benchee", "ShiftForward/apso", "spatialmodel/inmap", "terasolunaorg/terasoluna-gfw" ]

df = pd.read_csv('large_scale_paper_coveralls_result.csv', encoding='utf-8', names=header_names) 
print(df['crap_metric'])
# distibution_data = []
# for project in projects:
#     df = pd.read_csv('large_scale_paper_coveralls_result.csv', encoding='utf-8', names=header_names)  
#     filtered = df[ df['repository_name'] == project.lower() ]
#     print(project)
#     zero = []
#     zero_to_25 = []
#     twenty5_to_50 = []
#     fifty = []
#     fifty_to_75 = []
#     seventy5_to_100 = []
#     hundred = []
#     for i, row in filtered.iterrows():
#         commit_patch = float(row[11])
#         if  commit_patch == 0:
#             zero.append(commit_patch)
#         elif  commit_patch > 0 and commit_patch <= 25:
#             zero_to_25.append(commit_patch)
#         elif  commit_patch > 25 and commit_patch < 50:
#             twenty5_to_50.append(commit_patch)
#         elif commit_patch == 50 :
#             fifty.append(commit_patch)
#         elif  commit_patch > 50 and commit_patch <= 75:
#             fifty_to_75.append(commit_patch)
#         elif  commit_patch > 75 and commit_patch < 100:
#              seventy5_to_100.append(commit_patch)
#         elif  commit_patch == 100:
#             hundred.append(commit_patch)

#     distibution_data.append([ project,        
#                             (len(zero)/len(filtered))*100, 
#                             (len(zero_to_25)/len(filtered))*100, 
#                             (len(twenty5_to_50)/len(filtered))*100,
#                             (len(fifty)/len(filtered))*100, 
#                             (len(fifty_to_75)/len(filtered))*100,
#                             (len(seventy5_to_100)/len(filtered))*100,
#                             (len(hundred)/len(filtered))*100])

# data_frame = pd.DataFrame(distibution_data, columns=['repositories', '0' ,'0-25', '25-50', '50', '50-75', '75-100', '100'])
# data_frame.plot(x='repositories', kind='barh', stacked=True
#                 ,xlabel='percentage (%)', ylabel='repositories')
# plt.legend(loc="lower right", bbox_to_anchor=(1., 1.02) , borderaxespad=0., ncol=4)
# plt.show()