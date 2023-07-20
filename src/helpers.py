from datetime import datetime, timezone
import csv

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
    def csv_creator(cls, filename: str, data: list[dict]):
        pass
    
    @classmethod
    def csv_reader(cls, filename: str) -> list[dict]:
        pass

if __name__ == '__main__':
    print(__name__)