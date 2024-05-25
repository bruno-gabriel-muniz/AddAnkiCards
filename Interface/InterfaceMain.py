import customtkinter as ctk


class mainAddCards():
    def __init__(self) -> None:
        self.winStart = ctk.CTk()
        self.winStart.title("Start Menu")
        self.winStart.geometry("360x120")
        self.winStart.resizable(0, 0)

        NamePrograman = ctk.CTkLabel(self.winStart, text="Add Cards Anki\n" +
                                                         "From: 'Estudando e programando'"
                                     ).grid(row=0,
                                            column=0,
                                            columns=2)
        btnMakeMath = ctk.CTkButton(self.winStart, text="Make Cards Math",
                                    command=self.makeWinMath).grid(row=1,
                                                                   column=0,
                                                                   padx=20,
                                                                   pady=10)
        btnMakeIngles = ctk.CTkButton(self.winStart, text="Make Cards English",
                                      command=self.makeWinEnglish).grid(row=1,
                                                                        column=1,
                                                                        padx=20,
                                                                        pady=10)
        btnMakeCardsAnki = ctk.CTkButton(self.winStart, text="Add Cards In Anki",
                                         command=self.makeAddCards).grid(row=2,
                                                                         column=0,
                                                                         columns=2,
                                                                         pady=10)
        self.winStart.mainloop()

    def makeWinMath(self):
        winMat = ctk.CTk()
        winMat.title("Make Cards Math")

    def makeWinEnglish(self):
        winEnglish = ctk.CTk()
        winEnglish.title("Make Cards English")
        btnMakeCards = ctk.CTkButton(winEnglish, 120, 28, text="Novos Cartões",
                                     command=self.winNewCards).grid(row=0,
                                                                    column=2,
                                                                    padx=30)

    def winNewCards(self):
        winEnglishNewCards = ctk.CTk()

    def makeAddCards(self):
        winAddCards = ctk.CTk()
        winAddCards.title("Add Cards Anki")


Teste = mainAddCards()
