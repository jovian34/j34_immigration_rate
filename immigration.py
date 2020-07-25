class ImmigrationCase:

    def __init__(self):
        self.case_dict = {}
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
        phrase_result = None
        for denied_phrase in self.key_denied_phrase_collection:
            if denied_phrase in text:
                phrase_result = denied_phrase
        for grant_phrase in self.key_granted_phrase_collection:
            if grant_phrase in text:
                phrase_result = grant_phrase
        return phrase_result

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
                        self.case_dict[curr_case] = key_phrases
                    curr_case = line.strip()
                    self.case_dict[curr_case] = "Unknown"
                    key_phrases = []
                    new_case = False
                elif line.strip() == "End of Document":
                    new_case = True
                else:
                    phrase = self.line_contains_key_phrase(line.strip())
                    if phrase:
                        key_phrases.append(phrase)
            self.case_dict[curr_case] = key_phrases

    def calculate_granted_rate(self):
        granted = 0
        total = 0
        no_result = 0
        with open('outputs/result.txt', 'w') as result_file:
            for case, result in self.case_dict.items():
                result_file.writelines(f"{case}: {result}")
                try:
                    if result[0] in self.key_granted_phrase_collection:
                        granted += 1
                        result_file.writelines(f"- GRANTED\n")
                    else:
                        result_file.writelines(f"- DENIED\n")
                except IndexError:
                    result_file.writelines(f"*******ERROR: {case} has no result*************\n")
                    no_result += 1
                total += 1

            granted_rate = granted / total
            result_file.writelines(f"Cases with No result: {no_result} out of {total} cases.\n")
            result_file.writelines(f"Granted Rate: {granted_rate} out of {total} cases.")


