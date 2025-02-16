class CBA_Writer:
    def writeToCBA(CBA):
        cba = CBA + ""

        with open("CBA.txt", "a") as file:
            file.write(cba)
