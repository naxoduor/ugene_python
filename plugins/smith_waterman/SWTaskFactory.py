class SWTaskFactory:
    def __init__(self, alg_type):
        self.alg_type = alg_type

    def get_task_instance(self, config, task_name):
        return SWAlgorithmTask(config, task_name, self.alg_type)


class PairwiseAlignmentSmithWatermanTaskFactory(AbstractAlignmentTaskFactory):
    def __init__(self, alg_type):
        super().__init__()
        self.alg_type = alg_type

    def get_task_instance(self, settings):
        pairwise_settings = settings if isinstance(settings, PairwiseAlignmentTaskSettings) else None
        assert pairwise_settings is not None, "Pairwise alignment: incorrect settings"

        sw_settings = PairwiseAlignmentSmithWatermanTaskSettings(pairwise_settings)
        assert (not sw_settings.in_new_window or sw_settings.result_file_name), (
            "Pairwise alignment: incorrect settings, empty output file name"
        )

        if sw_settings.in_new_window:
            sw_settings.report_callback = SmithWatermanReportCallbackMAImpl(
                sw_settings.result_file_name.dir_path() + "/",
                sw_settings.result_file_name.base_file_name(),
                sw_settings.first_sequence_ref,
                sw_settings.second_sequence_ref,
                sw_settings.msa_ref,
            )
        else:
            if sw_settings.msa_ref.is_valid():
                sw_settings.report_callback = SmithWatermanReportCallbackMAImpl(
                    sw_settings.first_sequence_ref,
                    sw_settings.second_sequence_ref,
                    sw_settings.msa_ref,
                )

        sw_settings.result_listener = SmithWatermanResultListener()
        res_filter_reg = AppContext.get_sw_result_filter_registry()
        assert res_filter_reg is not None, "SWResultFilterRegistry is NULL."
        sw_settings.result_filter = res_filter_reg.get_filter(
            PairwiseAlignmentSmithWatermanTaskSettings.PA_SW_DEFAULT_RESULT_FILTER
        )
        sw_settings.percent_of_score = (
            PairwiseAlignmentSmithWatermanTaskSettings.PA_SW_DEFAULT_PERCENT_OF_SCORE
        )

        if sw_settings.convert_custom_settings():
            return PairwiseAlignmentSmithWatermanTask(sw_settings, self.alg_type)
        return None