class PhyTreeGeneratorTask(Task):
    def __init__(self, ma: Msa, settings: CreatePhyTreeSettings, task_flags: TaskFlags):
        super().__init__(
            PhyTreeGeneratorTask.tr("Calculating Phylogenetic Tree"),
            task_flags
        )

        self.inputMA = ma
        self.settings = settings
        self.result = None

        self.tpm = Task.Progress_Manual

    def getResult(self) -> PhyTree:
        return self.result

    def getSettings(self) -> CreatePhyTreeSettings:
        return self.settings


class PhyTreeGeneratorLauncherTask(Task):
    def __init__(self, ma: Msa, settings: CreatePhyTreeSettings):
        super().__init__(
            PhyTreeGeneratorLauncherTask.tr("Calculating Phylogenetic Tree"),
            TaskFlags_NR_FOSE_COSC
        )

        self.inputMA = ma.getCopy()
        self.settings = settings
        self.task = None

        self.tpm = Task.Progress_SubTasksBased

    RENAMED_ROW_PREFIX = "r"

    def prepare(self):
        registry = AppContext.getPhyTreeGeneratorRegistry()
        generator = registry.getGenerator(self.settings.algorithm)

        if generator is None:
            self.stateInfo.setError(
                self.tr(
                    f"Tree algorithm {self.settings.algorithm} is not found"
                )
            )
            return

        # Assign unique names to rows.
        # The row name is a string representation of the index + 'r' prefix.
        self.originalRowNameByIndex = self.inputMA.getRowNames()

        rows_count = self.inputMA.getRowCount()

        for i in range(rows_count):
            unique_row_name = f"{RENAMED_ROW_PREFIX}{i}"
            self.inputMA.renameRow(i, unique_row_name)

        self.task = generator.createCalculatePhyTreeTask(
            self.inputMA,
            self.settings
        )

        if not isinstance(self.task, PhyTreeGeneratorTask):
            raise TypeError("Not a PhyTreeGeneratorTask!")

        self.addSubTask(self.task)

    def report(self):
        # Equivalent of:
        # CHECK(!stateInfo.isCoR() && task != nullptr && !task->getStateInfo().isCoR(), ReportResult_Finished);
    
        if self.stateInfo.isCoR() or self.task is None or self.task.getStateInfo().isCoR():
            return ReportResult_Finished
    
        tree = self.task.getResult()
    
        # Equivalent of:
        # SAFE_POINT(tree != nullptr, "Tree is not present!", ReportResult_Finished);
    
        if tree is None:
            raise RuntimeError("Tree is not present!")
    
        nodes = tree.getNodesPreOrder()
    
        for node in nodes:
            ok = False
            row_name = node.name
    
            # CHECK_CONTINUE(rowName.startsWith(RENAMED_ROW_PREFIX));
            # Skip inner nodes.
            if not row_name.startswith(RENAMED_ROW_PREFIX):
                continue
            
            try:
                index_str = row_name[len(RENAMED_ROW_PREFIX):]
                index = int(index_str)
                ok = True
            except ValueError:
                ok = False
                index = -1
    
            # CHECK_EXT(...)
            if not (
                ok
                and 0 <= index < len(self.originalRowNameByIndex)
            ):
                self.setError(f"Failed to map row name: {row_name}")
                return ReportResult_Finished
    
            node.name = self.originalRowNameByIndex[index]
    
        self.result = tree
        return ReportResult_Finished

