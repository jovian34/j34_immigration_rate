import os
import maya
from os.path import join
from westlaw_cases import WestlawCase
from lexis_cases import LexisCase

westlaw_case_file = WestlawCase()
westlaw_case_file.create_filter_list()

lexis_case_file = LexisCase()

for root, dirs, files in os.walk('westlaw/'):
    for file in files:
        file_path = join(root, file)
        print(file_path)
        westlaw_case_file.add_cases_to_dict(file_path)

for root, dirs, files in os.walk('lexis/'):
    for file in files:
        file_path = join(root, file)
        print(file_path)
        lexis_case_file.add_cases_to_list_and_sort(file_path)


westlaw_case_file.create_sorted_case_list()
westlaw_case_file.filter_cases()
westlaw_case_file.remove_duplicate_cases()
westlaw_case_file.output_duplicate_list()
westlaw_case_file.calculate_granted_rate()
westlaw_case_file.report_error_cases()
westlaw_case_file.calculate_granted_plus_other()
westlaw_case_file.presidential_granted_rate()

lexis_case_file.remove_duplicate_cases()
lexis_case_file.output_duplicate_list()
lexis_case_file.output_lexis_case_list()


combined_case_list = []
for lexis_case in lexis_case_file.case_list:
    for westlaw_case in westlaw_case_file.case_list:
        if lexis_case[0] != westlaw_case[0]:
            pass
        else:
            words = []
            try:
                names = lexis_case[1]
            except IndexError:
                continue
            for name in names:
                subnames = name.split()
                for subname in subnames:
                    words.append(subname)
            for word in words:
                if word in westlaw_case[1]:
                    combined_case_list.append(lexis_case)
                    break

unique_westlaw_case_list = []
for westlaw_case in westlaw_case_file.case_list:
    westlaw_case_is_unique = True
    for combined_case in combined_case_list:
        if combined_case[0] != westlaw_case[0]:
            pass
        else:
            words = []
            try:
                names = combined_case[1]
            except IndexError:
                continue
            for name in names:
                subnames = name.split()
                for subname in subnames:
                    words.append(subname)
            for word in words:
                if word in westlaw_case[1]:
                    westlaw_case_is_unique = False
                    break
    if westlaw_case_is_unique:
        unique_westlaw_case_list.append(westlaw_case)

with open('outputs/unique_westlaw_cases.txt', 'w', encoding='utf-8') as result_file:
    for case in unique_westlaw_case_list:
        case_date = maya.MayaDT.from_datetime(case[0])
        case_date = case_date.date
        result_file.writelines(f"{case[1]}: on {case_date} result: {case[2]}, with phrases: {case[3]}\n")
    unique_westlaw_case_count = len(unique_westlaw_case_list)
    print(f"There are {unique_westlaw_case_count} unique Westlaw cases")
    result_file.writelines("==============================================\n")
    result_file.writelines(f"There were {unique_westlaw_case_count} unique Westlaw cases.\n")

unique_lexis_case_list = []
for lexis_case in lexis_case_file.case_list:
    if lexis_case in combined_case_list:
        continue
    else:
        unique_lexis_case_list.append(lexis_case)

with open('outputs/combined_case.txt', 'w', encoding='utf-8') as result_file:
    for case in combined_case_list:
        case_date = maya.MayaDT.from_datetime(case[0])
        case_date = case_date.date
        result_file.writelines(f"{case[1]}: on {case_date} \n")
    combined_case_count = len(combined_case_list)
    print(f"There were {combined_case_count} combined cases "
                           f"between Westlaw and Lexis")
    result_file.writelines("==============================================\n")
    result_file.writelines(f"There were {combined_case_count} combined cases "
                           f"between Westlaw and Lexis")

with open('outputs/unique_lexis_cases.txt', 'w', encoding='utf-8') as result_file:
    for case in unique_lexis_case_list:
        case_date = maya.MayaDT.from_datetime(case[0])
        case_date = case_date.date
        result_file.writelines(f"{case[1]}: on {case_date} \n")
    unique_lexis_case_count = len(unique_lexis_case_list)
    print(f"There are {unique_lexis_case_count} unique Lexis cases")
    result_file.writelines("==============================================\n")
    result_file.writelines(f"There were {unique_lexis_case_count} unique Lexis cases.\n")

