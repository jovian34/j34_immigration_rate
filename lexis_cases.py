import maya


class LexisCase:
    def __init__(self):
        self.case_list = []

    @staticmethod
    def determine_name(info):
        names = []

        if 're:' in info:
            parts = info.split('re:')
        elif ' re.' in info:
            parts = info.split(' re.')
        elif ' of:' in info:
            parts = info.split(' of:')
        elif ' OF:' in info:
            parts = info.split(' OF:')
        elif ' of,' in info:
            parts = info.split(' of,')
        elif 'of___,' in info.lower():
            parts = ['BLANK', 'NO NAME']
        else:
            parts = info.split(' of ')
            if len(parts) == 1:
                parts = parts[0].split(' re ')
        try:
            name_text = parts[1].split(',')
        except IndexError:
            print(f"ERROR: ")
            name_text = parts[0]
            print(name_text)

        subparts = []

        for part in name_text:
            text = part.strip()
            try:
                int(text[0])
                break
            except ValueError:
                subparts.append(text)
            except IndexError:
                subparts.append('NO NAME')

        for part in subparts:
            aka_parts = part.split(' a.k.a. ')
            if len(aka_parts) == 1:
                names.append(part)
            else:
                for aka_part in aka_parts:
                    names.append(aka_part)

        return names

    def add_cases_to_list_and_sort(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as case_file:
            lines = case_file.readlines()
            for line in lines:
                case = line.split(';')
                info = case[0].strip()
                names = self.determine_name(info)
                jurisdiction = case[1].strip()
                date_text = case[2].strip()
                try:
                    case_date = maya.parse(date_text).datetime()
                except:
                    now = maya.now()
                    today = now.datetime()
                    case_date = today

                self.case_list.append([case_date, names, jurisdiction])
        self.case_list.sort(key=lambda x: x[0])

    def remove_duplicate_cases(self):
        with open('outputs/lexis_duplicate_report.txt', 'w', encoding='utf-8') as result_file:
            before_length = len(self.case_list)
            result_file.writelines(f"Length of Lexis List before: {before_length}\n")
            no_dup_case_list = []
            for case in self.case_list:
                if case not in no_dup_case_list:
                    no_dup_case_list.append(case)
            self.case_list = no_dup_case_list
            after_length = len(self.case_list)
            result_file.writelines(f"Length of Lexis List after: {after_length}\n")
            difference = before_length - after_length
            result_file.writelines(f"There were {difference} duplicates in Lexis.")

    def output_lexis_case_list(self):
        with open('outputs/lexis_result.txt', 'w') as result_file:
            total = 0
            for case in self.case_list:
                total += 1
                case_date = maya.MayaDT.from_datetime(case[0])
                case_date = case_date.date
                result_file.writelines(f"{case[1]}: on {case_date} \n")
            result_file.writelines(f"There are {total} Lexis Cases")