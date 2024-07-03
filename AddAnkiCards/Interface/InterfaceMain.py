import customtkinter as ctk


class WindowMain(object):
    def __init__(self, dbConnect, Logger) -> None:
        '''Classe que representa as janelas do programa'''
        #
        # Iniciamos a janela
        self.Master = ctk.CTk()
        self.Master.resizable(0, 0)
        #
        # Definimos a cor do tema e o titulo
        self.Master.title('Add Anki Cards')
        self.colorTheme = '#009951'
        #
        # Fazemos o titulo da parte do ingles
        self.LabelEnglish = ctk.CTkLabel(
            self.Master, text='English', font=('Arial', 30)
        )
        self.LabelEnglish.grid(row=0, column=0, columns=2, padx=5, pady=5)
        #
        # Coletamos os dados dos cartoes e mostramos na janela
        # TODO: fazer uma funcao que busca as informacao no banco de dados
        InfoEnglish = ['Added Notes: n', 'Stored Notes: n', 'All Notes: n']
        self.labelEnglishInfo = ctk.CTkLabel(
            self.Master,
            text=f'{InfoEnglish[0]:>} | ' +
            f'{InfoEnglish[1]:<}\n{InfoEnglish[2]:^}',
        )
        self.labelEnglishInfo.grid(row=1, column=0, columns=2, padx=5, pady=5)
        #
        # Fazemos os botoes que vao adicionar e fazer os cartoes de ingles
        self.btnEnglishAdd = ctk.CTkButton(
            self.Master,
            height=70,
            text='Add Cards',
            fg_color=self.colorTheme,
        )
        self.btnEnglishAdd.grid(row=2, column=0, padx=5, pady=5)
        #
        #
        self.btnEnglishMake = ctk.CTkButton(
            self.Master,
            height=70,
            text='Make Cards',
            fg_color=self.colorTheme
        )
        self.btnEnglishMake.grid(row=2, column=1, padx=5, pady=5)
        #
        # Fazemos a divisoria
        ctk.CTkCanvas(self.Master, height=0, width=300).grid(
            row=3, column=0, columns=2, pady=5)
        #
        # E fazemos a mesma coisa para as opcoes e informacoes de informatica
        self.LabelMath = ctk.CTkLabel(
            self.Master, text='Math', font=('Arial', 30)
        )  # titulo
        self.LabelMath.grid(row=4, column=0, columns=2, padx=5, pady=5)
        #
        # Informacoes
        # TODO: fazer uma funcao que busca as informacao no banco de dados
        InfoMath = ['Added Cards: n', 'Stored Cards: n', 'All Cards: n']
        self.labelMathInfo = ctk.CTkLabel(
            self.Master,
            text=f'{InfoMath[0]:>} | ' +
            f'{InfoMath[1]:<}\n{InfoMath[2]:^}',
        )
        self.labelMathInfo.grid(row=5, column=0, columns=2, padx=5, pady=5)
        #
        # Botoes
        self.btnMathAdd = ctk.CTkButton(
            self.Master,
            height=70,
            text='Add Cards',
            fg_color=self.colorTheme,
        )
        self.btnMathAdd.grid(row=6, column=0, padx=5, pady=5)
        #
        #
        self.btnMathMake = ctk.CTkButton(
            self.Master,
            height=70,
            text='Make Cards',
            fg_color=self.colorTheme
        )
        self.btnMathMake.grid(row=6, column=1, padx=5, pady=5)
        self.Master.mainloop()


if __name__ == '__main__':
    WindowMain(None, None)
