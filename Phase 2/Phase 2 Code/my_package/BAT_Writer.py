class BAT_Writer:
    def writeToBAT(BAT):
        bat = BAT + ""

        with open("BAT.txt", "a") as file:
            file.write(bat)
