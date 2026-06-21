# UGENE - Integrated Bioinformatics Tools.
# Copyright (C) 2008-2025 UniPro
# http://ugene.net
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

from copy import deepcopy


class AbstractAlignmentTaskSettings:
    RESULT_FILE_NAME = "resultFileName"
    ALGORITHM_NAME = "algorithmName"
    REALIZATION_NAME = "realizationName"
    IN_NEW_WINDOW = "setOpenPairwiseAlignmentResultInNewWindow"
    ALPHABET = "alphabet"

    def __init__(self, some_settings=None, copy_from=None):
        if copy_from is not None:
            # Copy constructor behavior
            self.algorithm_id = copy_from.algorithm_id
            self.realization_name = copy_from.realization_name
            self.in_new_window = copy_from.in_new_window
            self.msa_ref = copy_from.msa_ref
            self.alphabet = copy_from.alphabet
            self.result_file_name = copy_from.result_file_name
            self.custom_settings = deepcopy(copy_from.custom_settings)
        else:
            self.algorithm_id = ""
            self.realization_name = ""
            self.in_new_window = True
            self.msa_ref = MsaRef()
            self.alphabet = Alphabet()
            self.result_file_name = GUrl()
            self.custom_settings = some_settings or {}

    def get_custom_value(self, option_name, default_val=None):
        return self.custom_settings.get(option_name, default_val)

    def set_custom_value(self, option_name, val):
        self.custom_settings[option_name] = val

    def convert_custom_settings(self) -> bool:
        if self.ALGORITHM_NAME in self.custom_settings:
            self.algorithm_id = str(
                self.custom_settings[self.ALGORITHM_NAME]
            )
            del self.custom_settings[self.ALGORITHM_NAME]

        if self.REALIZATION_NAME in self.custom_settings:
            self.realization_name = str(
                self.custom_settings[self.REALIZATION_NAME]
            )
            del self.custom_settings[self.REALIZATION_NAME]

        if self.RESULT_FILE_NAME in self.custom_settings:
            value = self.custom_settings[self.RESULT_FILE_NAME]
            if isinstance(value, str):
                self.result_file_name = GUrl(value)
                del self.custom_settings[self.RESULT_FILE_NAME]

        if self.IN_NEW_WINDOW in self.custom_settings:
            self.in_new_window = bool(
                self.custom_settings[self.IN_NEW_WINDOW]
            )
            del self.custom_settings[self.IN_NEW_WINDOW]

        return True

    def append_custom_settings(self, settings: dict):
        for key, value in settings.items():
            self.custom_settings[key] = value

    def is_valid(self) -> bool:
        return (
            self.msa_ref.is_valid()
            and self.alphabet.is_valid()
            and (
                not self.result_file_name.is_empty()
                or not self.in_new_window
            )
        )

