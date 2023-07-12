

class SourceFile:
    name: str
    relevant_line_count: int
    covered_line_count: int
    missed_line_count: int
    covered_percent: int

class SourceFileList:
    total: int
    current_page: int
    total_pages: int
    source_files: str
    parsed_files: list[SourceFile]