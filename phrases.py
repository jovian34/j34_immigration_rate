
class Phrases:
    def __init__(self):

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
