import pandas as pd
import matplotlib.pyplot as plt

header = "repo,childSha,parentSha,childBranch,timestamp,newHitLines,newNonHitLines,newFileHitLines,newFileNonHitLines,deletedLinesTested,deletedLinesNotTested,deletedFileLinesTested,deletedFileLinesNotTested,oldLinesNewlyTested,oldLinesNoLongerTested,modifiedLinesNewlyHit,modifiedLinesStillHit,modifiedLinesNotHit,nStatementsInBoth,nStatementsInEither,totalStatementsHitNow,totalStatementsHitPrev,totalStatementsNow,totalStatementsPrev,insFilesSrc,insFilesTest,modFilesSrc,modFilesTest,delFilesSrc,delFilesTest,newLinesSrc,newLinesTest,delLinesSrc,delLinesTest,insLinesAllFiles,delLinesAllFiles"
headers = header.split(",")


class LargeScaleStudyPatchCoverage:

    @staticmethod
    def plot_patch_coverage(filename: str, ) -> None:
        data_frame = pd.read_csv(filename, encoding='utf-8', delimiter=',', header=1)
        data_frame.drop(data_frame.columns[len(data_frame.columns) - 1], axis=1, inplace=True)
        data_frame.columns = headers
        projects = ["apache/commons-collections", "apache/commons-io",
                    "apache/commons-math", "ARMmbed/mbed-ls"]
        print(len(data_frame))
        data = []
        for project in projects:
            zero_bin = []
            zero_to_twenty_five_bin = []
            twenty_five_to_fifty_bin = []
            fifty_to_seventy_five_bin = []
            seventy_five_to_hundred = []
            hundred_bin = []
            filtered = data_frame.query("repo == @project")
            for index, row in filtered.iterrows():
                newHitLines = int(row['newHitLines'])
                newNonHitLines = int(row['newNonHitLines'])
                newFileHitLines = int(row['newFileHitLines'])
                newFileNonHitLines = int(row['newFileNonHitLines'])

                numerator = (newHitLines + newFileHitLines)
                denominator = (newHitLines + newNonHitLines + newFileNonHitLines + newFileNonHitLines)
                # denominator = (newHitLines + newNonHitLines + newFileHitLines + newFileNonHitLines)

                if denominator == 0:
                    current_patch = 0
                else:
                    current_patch = (numerator / denominator)*100

                if current_patch == 0:
                    zero_bin.append(current_patch)
                elif 0 < current_patch < 25:
                    zero_to_twenty_five_bin.append(current_patch)
                elif 25 < current_patch <= 50:
                    twenty_five_to_fifty_bin.append(current_patch)
                elif 50 < current_patch <= 75:
                    fifty_to_seventy_five_bin.append(current_patch)
                elif 75 < current_patch < 100:
                    seventy_five_to_hundred.append(current_patch)
                elif current_patch == 100:
                    hundred_bin.append(current_patch)
            print(f'Project Name: {project} = {len(filtered)}')
            if len(filtered) > 0:
                data.append([project,
                             (len(zero_bin) / len(filtered)) * 100,
                             (len(zero_to_twenty_five_bin) / len(filtered)) * 100,
                             (len(twenty_five_to_fifty_bin) / len(filtered)) * 100,
                             (len(fifty_to_seventy_five_bin) / len(filtered)) * 100,
                             (len(seventy_five_to_hundred) / len(filtered)) * 100,
                             (len(hundred_bin) / len(filtered)) * 100])

        data_frame = pd.DataFrame(data,
                                  columns=['repositories', '0', '0-25', '25-50', '50-75', '75-100', '100'])
        data_frame.plot(x='repositories', kind='barh', stacked=True
                        , xlabel='percentage (%)', ylabel='repositories', title='Large Scale Paper')
        plt.legend(loc="lower right", bbox_to_anchor=(1., 1.02), borderaxespad=0., ncol=4)
        # plt.savefig('./outputs/all_branch_commit_size_dist.pdf')
        plt.show()


if __name__ == '__main__':
    LargeScaleStudyPatchCoverage.plot_patch_coverage("largeScaleScriptCombined.csv")
