
class CrapMetric:
    
    def commit_crap_metric(commitInst, patch_coverage: float) -> float:
        total_method_complexity = 0 
        for m in commitInst.modified_files:
            for changed_method in m.changed_methods:
                method_details = changed_method.__dict__
                total_method_complexity += method_details['complexity']
        commit_crap = pow(total_method_complexity, 2)*pow(1 - (patch_coverage/100), 3) + total_method_complexity
        return round(commit_crap, 3)

if __name__ == '__main__':
    print(__name__)