from pydriller import Repository

# commit_hash = "dc257949b338ac773b82a72de560ec5a14a1c90b"
# commit_hash = "b398e5894c525004ffaeca496956daead7ed1c8d"
# commit_hash = "fb58dcaf9a4c4bc5a220515b79a75f66ef9bf085"
# commit_hash = "738ecc8ff5626b4797eff801fd61103b4487f06e"
commit_hash = "129854f34036e5e01e75a0c8c06d72aa6d8c57f6"
github_url = f'https://github.com/ErnestFistozz/codecov-coveralls.git'

for commit in Repository(github_url, single=commit_hash).traverse_commits():
    parent_commit_methods = []
    child_commit_methods = []
    for m in commit.modified_files:
        if m.filename.endswith('.py'):
            child_commit_methods.extend(
                {
                    'method_name': method.__dict__['name'],
                    'complexity': method.__dict__['complexity']
                }
                for method in m.changed_methods
            )
            parent_commit_methods.extend(
                {
                    'method_name': method.__dict__['name'],
                    'complexity': method.__dict__['complexity']
                }
                for method in m.methods_before
            )
        delta_complexity = []
        for child_func in child_commit_methods:
            for parent_func in parent_commit_methods:
                if child_func['method_name'] == parent_func['method_name']:
                    if parent_func['complexity'] != parent_func['complexity']:
                        delta_complexity.append({
                            'method_name': child_func['name'],
                            'complexity': child_func['complexity'] - parent_func['complexity']
                        })
                else:
                    delta_complexity.append({
                        'method_name': child_func['name'],
                        'complexity': child_func['complexity']
                    })
