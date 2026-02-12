class PairwiseAlignmentSmithWatermanTaskSettings:
    PA_SW_DEFAULT_RESULT_FILTER = "default"
    PA_SW_DEFAULT_PERCENT_OF_SCORE = 90

    def __init__(self):
        # --- Window / output configuration ---
        self.in_new_window = False
        self.result_file_name = None

        # --- Sequence references ---
        self.first_sequence_ref = None
        self.second_sequence_ref = None
        self.msa_ref = None

        # --- Runtime-configured components ---
        self.report_callback = None
        self.result_listener = None
        self.result_filter = None

        # --- Algorithm configuration ---
        self.percent_of_score = self.PA_SW_DEFAULT_PERCENT_OF_SCORE

        # --- Optional custom scoring parameters ---
        self.match_score = 2
        self.mismatch_penalty = -1
        self.gap_penalty = -2

    def convert_custom_settings(self):
        """
        Validates and finalizes settings before task creation.
        Returns True if settings are valid, otherwise False.
        """
        if not self.first_sequence_ref or not self.second_sequence_ref:
            return False

        if self.in_new_window and not self.result_file_name:
            return False

        if self.percent_of_score <= 0 or self.percent_of_score > 100:
            return False

        return True
