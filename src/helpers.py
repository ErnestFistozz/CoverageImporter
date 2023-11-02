from datetime import datetime, timezone
import csv
import os
import platform
import pandas as pd
import subprocess
import logging


class Helpers:

    @staticmethod
    def index_finder(search_word: str, files: list[str]) -> int:
        for index, word in enumerate(files):
            if search_word.lower() in word.lower():
                return index
        return -1

    @staticmethod
    def date_formatter(timestamp: str):
        formated_timestamp = datetime.fromisoformat(timestamp[:-1]).astimezone(timezone.utc)
        return formated_timestamp.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def save_into_file(filename: str, coverage: list) -> None:
        print('I am saving infor to the file')
        username = Helpers.determine_machine()
        match platform.system().lower():
            case 'linux' | 'darwin':
                csv_full_path = rf'/home/{username}/repositories/{filename}'
            case _:
                csv_full_path = rf'C:\Users\{username}\Desktop\AzureDevOpsRepos\{filename}'
        with open(csv_full_path, "a+") as outfile:
            csv_writer = csv.writer(outfile)
            for row in coverage:
                try:
                    if not isinstance(row,
                                      dict) or 'patch_coverage' not in row:  # This filters all commits which could
                        # not be checked out by pydriller
                        raise Exception
                    csv_writer.writerow([Helpers.date_formatter(value) if
                                         key.lower() == 'created_at' else value for key, value in row.items()])
                except (KeyError, TypeError):
                    continue

    @staticmethod
    def read_from_csv(filename: str) -> list:
        if not os.path.exists(filename):
            raise FileNotFoundError
        else:
            df = pd.read_csv(filename, header=0, delimiter=',')
            data = [{
                'repo': row['repository'],
                'org': row['organisation'],
                'language': row['language'],
            }
                for index, row in df.iterrows()
            ]
        return data

    @staticmethod
    def repositories(file_name: str) -> list:
        with open(file_name, 'r') as file:
            return [line.split()[0].split("/") for line in file]

    @staticmethod
    def determine_machine() -> str:
        match platform.system().lower():
            case 'linux' | 'darwin':
                cmd = "whoami"
                result = (subprocess.run(cmd, capture_output=True, shell=True, text=True, check=True).stdout)
                return result
            case 'windows':
                cmd = '$env:USERNAME'
                result = (subprocess.run(["powershell", "-Command", cmd],
                                         capture_output=True, shell=True).stdout)
                data = result.decode('utf8').replace("'", '"')
                return data

    @staticmethod
    def coverage_logger(filename: str, error_message: str) -> None:
        full_datetime = datetime.now()
        file_format = '{}_{}_{}_{}_{}_{}'.format(full_datetime.day,
                                                 full_datetime.month,
                                                 full_datetime.year,
                                                 full_datetime.second,
                                                 full_datetime.minute,
                                                 full_datetime.hour)
        full_filename = f'/home/ernest/repositories/{file_format}_{filename}.log'
        logging.basicConfig(filename=full_filename,
                            encoding='utf-8',
                            format='%(asctime)s:%(levelname)s:%(message)s',
                            level=logging.DEBUG,
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.error(error_message)


if __name__ == '__main__':
    print(__name__)
