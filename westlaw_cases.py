import maya
from maya import MayaInterval
from phrases import Phrases


class WestlawCase:

    def __init__(self):
        self.case_dict = {}
        self.case_list = []
        self.filter_case_list = []
        self.duplicate_case_list = []
        self.current_case_date = None
        self.phrases = Phrases()

    def line_contains_key_phrase(self, text):
        phrase_result = []
        for denied_phrase in self.phrases.key_denied_phrase_collection:
            if denied_phrase in text:
                phrase_result.append(denied_phrase)
        for grant_phrase in self.phrases.key_granted_phrase_collection:
            if grant_phrase in text:
                phrase_result.append(grant_phrase)
        for other_phrase in self.phrases.other_factors:
            if other_phrase in text:
                phrase_result.append(other_phrase)
        return phrase_result

    def is_line_a_date(self, text):
        try:
            self.current_case_date = maya.parse(text).datetime()
        except:
            return False
        return True

    def create_filter_list(self):
        with open('List of IAC + Discretionary Relief-Westlaw.txt', 'r', encoding='utf-8') as filter:
            lines = filter.readlines()
            for line in lines:
                try:
                    int(line[0])
                except ValueError:
                    try:
                        a = line[10]
                    except IndexError:
                        continue
                    date_text = line[4:].strip()
                    date_text = date_text.split('Interim')
                    date_text = date_text[0]
                    current_case_date = maya.parse(date_text).datetime()
                    self.filter_case_list.append([current_case_date, parts[1]])
                    current_case_date, current_case_name = None, None
                    continue
                current_case_name = line
                if 're:' in current_case_name:
                    parts = current_case_name.split('re:')
                elif 'RE:' in current_case_name:
                    parts = current_case_name.split('RE:')
                elif 'IN RE' in current_case_name:
                    parts = current_case_name.split('IN RE')
                elif 'In re' in current_case_name:
                    parts = current_case_name.split('In re')
                elif 'Matter of' in current_case_name:
                    parts = current_case_name.split('Matter of')
                elif 'MATTER OF' in current_case_name:
                    parts = current_case_name.split('MATTER OF')
                else:
                    print(f"NO DELIMETER: {current_case_name}")
        self.filter_case_list.sort(key=lambda x: x[0])
        for case in self.filter_case_list:
            print(case)

    def add_cases_to_dict(self, file_path):
        new_case = False
        first_case = True
        with open(file_path, 'r', encoding='utf-8') as case_file:
            lines = case_file.readlines()
            key_phrases = []
            for line in reversed(lines):
                if new_case:
                    if first_case:
                        first_case = False
                    else:
                        values["phrases"] = key_phrases
                        self.case_dict[curr_case] = values
                        key_phrases = []
                    curr_case = line.strip()
                    self.case_dict[curr_case] = "Unknown"
                    values = {}
                    new_case = False
                    self.current_case_date = None
                elif line.strip() == "End of Document":
                    new_case = True
                elif line.strip()[:6] == "IN RE:":
                    values["name"] = line.strip()[6:]
                elif self.is_line_a_date(line.strip()):
                    values["date"] = self.current_case_date
                else:
                    phrases = self.line_contains_key_phrase(line.strip())
                    if len(phrases) > 0:
                        for phrase in phrases:
                            key_phrases.append(phrase)
            values["phrases"] = key_phrases
            self.case_dict[curr_case] = values

    def filter_cases(self):
        filtered_cases = []
        total = 0
        for case in self.case_list:
            for filter_case in self.filter_case_list:
                if case[0] == filter_case[0]:
                    start_words = filter_case[1].split()
                    words = []
                    for start_word in start_words:
                        if start_word.lower() == 'a.k.a':
                            continue
                        elif len(start_word) < 3:
                            continue
                        else:
                            words.append(start_word)
                    for word in words:
                        try:
                            if word in case[1]:
                                total += 1
                                filtered_cases.append(case)
                                break
                        except TypeError:
                            break
        print(f"Total cases = {total}")
        self.case_list = filtered_cases

    def determine_result(self, phrases):
        for phrase in phrases:
            try:
                if phrase in self.phrases.key_granted_phrase_collection:
                    return 'Granted'
                if phrase in self.phrases.key_denied_phrase_collection:
                    return 'Denied'
                if phrase is self.phrases.other_factors:
                    pass
            except IndexError:
                return '*******ERROR'
        return '*******ERROR'

    def create_sorted_case_list(self):
        for case, value in self.case_dict.items():
            phrases = value['phrases']
            result = self.determine_result(phrases)
            if result == '*******ERROR':
                phrases = ['No phrases']
            try:
                case_date = value['date']
            except KeyError:
                now = maya.now()
                today = now.datetime()
                case_date = today
            try:
                non_citizen = value['name']
            except KeyError:
                non_citizen = None
            case_details = [case_date, non_citizen, result, phrases]
            self.case_list.append(case_details)
        self.case_list.sort(key=lambda x: x[0])

    def remove_duplicate_cases(self):
        with open('outputs/westlaw_duplicate_report.txt', 'w', encoding='utf-8') as result_file:
            before_length = len(self.case_list)
            result_file.writelines(f"Length of Westlaw List before: {before_length}\n")
            no_dup_case_list = []
            for case in self.case_list:
                if case not in no_dup_case_list:
                    no_dup_case_list.append(case)
                else:
                    self.duplicate_case_list.append(case)
            self.case_list = no_dup_case_list
            after_length = len(self.case_list)
            result_file.writelines(f"Length of Westlaw List after: {after_length}\n")
            difference = before_length - after_length
            result_file.writelines(f"There were {difference} duplicates in Westlaw.")

    def output_duplicate_list(self):
        with open('outputs/westlaw_duplicate.txt', 'w', encoding='utf-8') as result_text:
            for case in self.duplicate_case_list:
                case_date = maya.MayaDT.from_datetime(case[0])
                case_date = case_date.date
                result_text.writelines(f"{case[1]}: on {case_date} result: {case[2]}, with phrases: {case[3]}\n")

    def calculate_granted_rate(self):
        granted = 0
        total = 0
        no_result = 0
        with open('outputs/westlaw_result.txt', 'w') as result_file:
            for case in self.case_list:
                case_date = maya.MayaDT.from_datetime(case[0])
                case_date = case_date.date
                result_file.writelines(f"{case[1]}: on {case_date} result: {case[2]}, with phrases: {case[3]}\n")
                total += 1
                if case[2] == 'Granted':
                    granted += 1
                if case[2] == '*******ERROR':
                    no_result += 1
            granted_rate = granted * 100 / total
            result_file.writelines(f"Cases with No result: {no_result} out of {total} cases.\n")
            result_file.writelines(f"Granted Rate: {granted_rate}% out of {total} cases.")

    def presidential_granted_rate(self):
        bush_total = 0
        bush_granted = 0
        start = maya.parse('Jan 20, 2001').datetime()
        end = maya.parse('Jan 19, 2009').datetime()
        bush_term = MayaInterval(start=start, end=end)
        obama_total = 0
        obama_granted = 0
        start = maya.parse('Jan 20, 2009').datetime()
        end = maya.parse('Jan 19, 2017').datetime()
        obama_term = MayaInterval(start=start, end=end)
        trump_total = 0
        trump_granted = 0
        start = maya.parse('Jan 20, 2017').datetime()
        end = maya.parse('Jan 19, 2021').datetime()
        trump_term = MayaInterval(start=start, end=end)
        for case in self.case_list:
            if bush_term.contains_dt(case[0]):
                bush_total += 1
                if case[2] == 'Granted':
                    bush_granted += 1
            if obama_term.contains_dt(case[0]):
                obama_total += 1
                if case[2] == 'Granted':
                    obama_granted += 1
            if trump_term.contains_dt(case[0]):
                trump_total += 1
                if case[2] == 'Granted':
                    trump_granted += 1
        with open('outputs/presidential_rates.txt', 'w', encoding='utf-8') as result_file:
            bush_rate = bush_granted * 100 / bush_total
            obama_rate = obama_granted * 100 / obama_total
            trump_rate = trump_granted * 100 / trump_total
            result_file.writelines(f"The Granted Rate under President Bush was {bush_rate}%, "
                                   f"{bush_granted} granted cases out of {bush_total}\n")
            result_file.writelines(f"The Granted Rate under President Obama was {obama_rate}%, "
                                   f"{obama_granted} granted cases out of {obama_total}\n")
            result_file.writelines(f"The Granted Rate under President Trump is {trump_rate}%, "
                                   f"{trump_granted} granted cases out of {trump_total}\n")

    def calculate_granted_plus_other(self):
        other_factor_dict = {factor: 0 for factor in self.phrases.other_factors}
        for case in self.case_list:
            for factor in self.phrases.other_factors:
                if case[2] == 'Granted':
                    if factor in case[3]:
                        other_factor_dict[factor] += 1
        with open('outputs/other_factor.txt', 'w', encoding='utf-8') as result_file:
            for factor, total in other_factor_dict.items():
                percent = total * 100 / len(self.case_list)
                result_file.writelines(f"{total} granted cases mentioned {factor}"
                                       f" - or {percent}% of total Westlaw cases\n")

    @staticmethod
    def report_error_cases():
        with open('outputs/westlaw_result.txt', 'r') as result_text:
            with open('outputs/error.txt', 'w') as error_text:
                lines = result_text.readlines()
                for line in lines:
                    if '*******ERROR' in line:
                        error_text.writelines(line)

