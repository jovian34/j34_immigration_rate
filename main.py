import os
from os.path import join
from immigration import ImmigrationCase

case_file = ImmigrationCase()

for root, dirs, files in os.walk('txt/'):
    for file in files:
        file_path = join(root, file)
        print(file_path)
        case_file.add_cases_to_dict(file_path)

case_file.calculate_granted_rate()

with open('outputs/result.txt', 'r') as result_text:
    with open('outputs/error.txt', 'w') as error_text:
        lines = result_text.readlines()
        for line in lines:
            if '*******ERROR' in line:
                error_text.writelines(line)
