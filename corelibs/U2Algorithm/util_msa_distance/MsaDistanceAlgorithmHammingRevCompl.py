class MsaDistanceAlgorithmHammingRevCompl(MsaDistanceAlgorithm):

    def __init__(self, factory, ma, parent=None):
        super().__init__(factory, ma, parent)

    def run(self):
        comp_tt = (
            AppContext.getDNATranslationRegistry()
            .lookupComplementTranslation(self.ma.getAlphabet())
        )

        assert comp_tt is not None

        trans = comp_tt
        n_seq = self.ma.getRowCount()

        revtransl = Msa()
        revtransl.setAlphabet(self.ma.getAlphabet())

        os = U2OpStatus2Log()

        for i in range(n_seq):
            if self.isCanceled():
                return

            arr = self.ma.getRow(i).toByteArray(os, self.ma.getLength())

            trans.translate(arr.data(), len(arr))
            TextUtils.reverse(arr.data(), len(arr))

            revtransl.addRow(self.ma.getRow(i).getName(), arr)

            if os.hasError():
                self.setError(
                    self.tr(
                        "An unexpected error has occurred during running "
                        "the Hamming reverse-complement algorithm."
                    )
                )
                return

        for i in range(n_seq):
            for j in range(i, n_seq):
                sim = 0
                for k in range(self.ma.getLength()):
                    if self.isCanceled():
                        return

                    if self.ma.charAt(i, k) == revtransl.charAt(j, k):
                        sim += 1

                self.lock.lock()
                try:
                    self.setDistanceValue(i, j, sim)
                finally:
                    self.lock.unlock()

            self.stateInfo.setProgress(i * 100 // n_seq)
