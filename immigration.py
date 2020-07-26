import maya


class ImmigrationCase:

    def __init__(self):
        self.case_dict = {}
        self.case_list = []
        self.current_case_date = None
        self.other_factors = [
            "asylum",
            "cancellation of removal",
            "voluntary departure",
            "adjustment of status",
        ]
        self.key_denied_phrase_collection = [
            "is denied",
            "are denied",
            "is dismissed",
            "are dismissed",
            "is hereby denied",
            "is, hereby, denied",
            "are hereby denied",
            "is, therefore, denied",
            "are, therefore, denied",
            "motion to reopen will be denied",  # 2005 WL 3709369 (BIA)
            "will be dismissed",
            "are dismissing",
            "we have dismissed",
            "dismiss the appeal",
            "We adopt and affirm the decision",  # 2005 WL 3709334 (BIA)
            "we hold that reopening is not warranted",  # 2005 WL 698449 (BIA)
            "find no error",  # 2008 WL 5537794 (BIA)
            "the appeal is untimely",  # 2003 WL 23269917 (BIA)
            "The respondent’s motion is untimely",  # 2003 WL 23270101 (BIA)
            "is affirmed",  # The decision of the immigration judge
        ]

        self.key_granted_phrase_collection = [
            "is granted",
            "are granted",
            "is hereby granted",
            "are hereby granted",
            "will be granted",
            "grant the motion",
            "is remanded",
            "are remanded",
            "We therefore remand",
            "is hereby remanded",
            "are hereby remanded",
            "remand this case",
            "is vacated",
            "are vacated",
            "is hereby vacated",
            "are hereby vacated",
            "is sustained",
            "are sustained",
            "is hereby sustained",
            "are hereby sustained",
        ]

    def line_contains_key_phrase(self, text):
        phrase_result = []
        for denied_phrase in self.key_denied_phrase_collection:
            if denied_phrase in text:
                phrase_result.append(denied_phrase)
        for grant_phrase in self.key_granted_phrase_collection:
            if grant_phrase in text:
                phrase_result.append(grant_phrase)
        for other_phrase in self.other_factors:
            if other_phrase in text:
                phrase_result.append(other_phrase)
        return phrase_result

    def is_line_a_date(self, text):
        try:
            self.current_case_date = maya.parse(text).datetime()
        except:
            return False
        return True

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

    def determine_result(self, phrases):
        for phrase in phrases:
            try:
                if phrase in self.key_granted_phrase_collection:
                    return 'Granted'
                if phrase in self.key_denied_phrase_collection:
                    return 'Denied'
                if phrase is self.other_factors:
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

    def calculate_granted_rate(self):
        granted = 0
        total = 0
        no_result = 0
        with open('outputs/result.txt', 'w') as result_file:
            for case in self.case_list:
                case_date = maya.MayaDT.from_datetime(case[0])
                case_date = case_date.date
                result_file.writelines(f"{case[1]}: on {case_date} result: {case[2]}, with phrases: {case[3]}\n")
                total += 1
                if case[2] == 'Granted':
                    granted += 1
                if case[2] == '*******ERROR':
                    no_result += 1
            granted_rate = granted / total
            result_file.writelines(f"Cases with No result: {no_result} out of {total} cases.\n")
            result_file.writelines(f"Granted Rate: {granted_rate} out of {total} cases.")



    @staticmethod
    def report_error_cases():
        with open('outputs/result.txt', 'r') as result_text:
            with open('outputs/error.txt', 'w') as error_text:
                lines = result_text.readlines()
                for line in lines:
                    if '*******ERROR' in line:
                        error_text.writelines(line)

