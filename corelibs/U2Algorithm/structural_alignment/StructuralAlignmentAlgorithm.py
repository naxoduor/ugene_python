class BioStruct3DReference:
    def __init__(self, obj, chains, chainRegion, modelId):
        self.obj = obj
        self.chains = chains
        self.chainRegion = chainRegion
        self.modelId = modelId

    def print(self) -> str:
        s = self.obj.getGObjectName()

        if len(self.chains) == 1:
            chain_id = self.chains[0]
            s += f" chain {chain_id}"
            s += f" region {self.chainRegion.startPos + 1}..{self.chainRegion.endPos()}"
        else:
            s += " chains ["
            s += ",".join(str(c) for c in self.chains)
            s += "]"

        s += f" model {self.modelId}"
        return s


class StructuralAlignmentTask(Task):
    def __init__(self, algorithm, settings):
        super().__init__(
            "StructuralAlignmentTask",
            TaskFlag_ReportingIsSupported | TaskFlag_ReportingIsEnabled
        )
        self.algorithm = algorithm
        self.settings = settings
        self.result = None

    def run(self):
        self.result = self.algorithm.align(self.settings, self.stateInfo)

    def report(self):
        return ReportResult_Finished

    def generateReport(self) -> str:
        res = ""

        if not self.hasError():
            res += (
                "Structural alignment finished on "
                f"<b>{self.settings.ref.print()}</b> (reference) vs "
                f"<b>{self.settings.alt.print()}</b><br><br>"
            )
            res += f"<b>RMSD</b> = {self.result.rmsd}"

            res += "<table><tr><td>"
            res += "<b>Transform</b> = "
            res += "</td><td>"
            res += "<table>"
            res += "<tr>"
            for i in range(16):
                res += f"<td>{self.result.transform[i]}</td>"
                if (i + 1) % 4 == 0 and i < 15:
                    res += "</tr><tr>"
            res += "</tr>"
            res += "</table>"
            res += "</td></tr></table>"
        else:
            res += (
                "Structural alignment on "
                f"<b>{self.settings.ref.print()}</b> (reference) vs "
                f"<b>{self.settings.alt.print()}</b> failed"
            )

        return res