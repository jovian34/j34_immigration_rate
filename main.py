import os
from os.path import join
from immigration import ImmigrationCase

case_file = ImmigrationCase()

for root, dirs, files in os.walk('westlaw/'):
    for file in files:
        file_path = join(root, file)
        print(file_path)
        case_file.add_cases_to_dict(file_path)

case_file.create_sorted_case_list()
case_file.calculate_granted_rate()
case_file.report_error_cases()
