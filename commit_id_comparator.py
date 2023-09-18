import pandas as pd

df_mined_coveralls = pd.read_csv("src/ui/coverallsdata.csv")
df_large_scale = pd.read_csv("src/ui/large_scale_paper_coveralls_result.csv")

# print(df_large_scale)
# print(df_mined_coveralls)

print(len(df_large_scale))
print(len(df_mined_coveralls))

# similar_hashes = 0
# diff_hashes = 0
# for i, row_i in df_large_scale.iterrows():
#     for j, row_j  in df_mined_coveralls.iterrows():
#         if row_i[1] == row_j[1]:
#             similar_hashes += 1
#         else:
#             diff_hashes += 1
#
# print(similar_hashes)
# print(diff_hashes)