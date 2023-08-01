
class PatchFiles:

    def patch_files(self, files: list[str], language_extension: str) -> dict:
        code_count, test_count = 0, 0
        for file in files:
            if file.endswith(language_extension):
                if 'test' in file:
                    test_count += 1
                else:
                    code_count += 1
        return {
            'test_files': 1 if code_count == 0 and test_count > 0 else 0,
            'code_files': 1 if code_count > 0 and test_count == 0 else 0,
            'test_code_files': 1 if code_count > 0 and test_count > 0 else 0,
            'other_files': 1 if code_count == 0 and test_count == 0 else 0,
        }