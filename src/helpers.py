from datetime import datetime, timezone
import csv
import os
import platform
import pandas as pd
class Helpers:

    @classmethod
    def index_finder(cls, search_file: str, files: list[str]) -> int:
        for index, word in enumerate(files):
            if search_file in word:
                return index
        return -1
    
    @classmethod
    def date_formatter(cls, timestamp: str):
        formated_timestamp = datetime.fromisoformat(timestamp[:-1]).astimezone(timezone.utc)
        return formated_timestamp.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def save_into_file(cls, filename: str,  coverage :list) -> None:
        csv_full_path = ''
        match platform.system().lower():
            case 'linux' | 'darwin':
                csv_full_path = rf'/home/ernest/repositories/{filename}'
            case _:
                csv_full_path = rf'C:\Users\ebmamba\Desktop\AzureDevOpsRepos{filename}'
        with open(csv_full_path, "a+") as outfile:
            csv_writer = csv.writer(outfile)
            #csv_writer.writerow(["RepositoryName", "Branch" , "Date", "CommitHash", "OverallCoverage", "PatchCooverage", "PatchSize"])
            #csv_writer.writerow(["RepositoryName", "Branch" , "Date", "CommitHash", "OverallCoverage", "PatchCooverage", "PatchSize"])
            for row in coverage:
                csv_writer.writerow([row['repository_name'], row['branch'], Helpers.date_formatter(row['created_at']), row['commit_sha'], row['covered_percent'], row['patch_coverage'] ])

    @classmethod
    def read_from_csv(cls, filename: str) -> list:
        if not os.path.exists(filename):
            raise FileNotFoundError
        else:
            df = pd.read_csv(filename , header=0, delimiter=',')
            data = [{
                'repo': row['repository'],
                'main_branch': row['branch'],
                'org': row['organisation'],
                'language': row['language'],
                }
                    for index, row in df.iterrows()
                ]

        return data
                
if __name__ == '__main__':
    print(__name__)
