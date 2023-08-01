from pydriller import Commit

class PatchSize:
    	
    def patch_sizes(self, commit: Commit, language_extension: str) -> dict:
        code_patch_size, test_patch_size, config_patch_size = 0, 0, 0
        for m in commit.modified_files:
            if m.filename.endswith(language_extension):
                if 'test' in m.filename:
                    test_patch_size += m.added_lines + m.deleted_lines
                else:
                    code_patch_size += m.added_lines + m.deleted_lines
            else:
                config_patch_size += m.added_lines + m.deleted_lines
        return {
                'code_patch_size': code_patch_size,
                'test_patch_size': test_patch_size,
                'config_patch_size': config_patch_size
            }
