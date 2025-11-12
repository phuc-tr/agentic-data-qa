from collections import defaultdict

def post_process_checks(proposals, max_checks=10, max_per_column=3, max_per_type=2):
    """
    Post-process a list of check proposals:
      - max 3 checks per column
      - max 2 checks per type
      - keep top N by likelihood
    """
    # Sort by likelihood descending
    sorted_checks = sorted(proposals, key=lambda x: x.get("likelihood", 0), reverse=True)

    column_counter = defaultdict(int)
    type_counter = defaultdict(int)
    final_checks = []

    for check in sorted_checks:
        col = check.get("column")
        typ = check.get("type")

        if column_counter[col] >= max_per_column:
            continue
        if type_counter[typ] >= max_per_type:
            continue

        final_checks.append(check)
        column_counter[col] += 1
        type_counter[typ] += 1

        if len(final_checks) >= max_checks:
            break

    return final_checks
