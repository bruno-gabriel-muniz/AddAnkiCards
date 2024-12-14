from logging import Logger
from typing import Union

import customtkinter as ctk

from add_anki_cards.logging_main import get_logger


class Tooltip:
    def __init__(
        self,
        master_widget: ctk.CTk | ctk.CTkToplevel,
        widget: Union[ctk.CTkBaseClass],
        data_config: dict[str, Union[ctk.CTkFont, str, tuple]],
        text: str,
        logger: Logger = None,
        delay: int = 500,
    ) -> None:
        """
        Classe versátil para criar dic. de ferramenta (tooltips) em app's ctk.

        Args:
            master_widget: O widget pai para a tooltip.
            widget: O widget ao qual a tooltip está vinculada.
            data_config: Um dicionário contendo configurações para a tooltip:
                - `font`: A fonte do texto da tooltip.
                - `color_theme`: O tema de cores do texto da tooltip.
            text: O texto a ser exibido na tooltip.
        """
        if logger:
            self.logger = logger
        else:
            self.logger = get_logger('User_Default')
        self.master_widget = master_widget
        self.widget = widget
        self.data_config = data_config
        self.delay = delay
        self.text = text
        self.short_text = self.text[: self.text.find('\n')]
        self.tooltip_win = None
        if isinstance(self.widget, ctk.CTkButton):
            self.logger.info(
                f'Iniciando o tooltip do widget: {self.widget},'
                + f' {self.widget.cget("text")}'
            )
        elif isinstance(self.widget, (ctk.CTkEntry, ctk.CTkTextbox)):
            self.logger.info(
                f'Iniciando o tooltip do widget: {self.widget},'
                + f' {self.widget.cget("placeholder_text")}'
            )
        else:
            self.logger.info(
                f'Iniciando o tooltip do widget: {self.widget},'
                + f' {self.short_text}'
            )

        # Binds para mostrar o texto
        self.widget.bind('<Enter>', self._schedule_tooltip)
        self.widget.bind('<Leave>', self._hide_tooltip)

    def _schedule_tooltip(self, event=None):
        """Agenda a exibição do tooltip após o atraso definido."""
        self._after_id = self.widget.after(self.delay, self._show_tooltip)

    def _show_tooltip(self) -> None:
        """Met. q mostra o texto"""

        # verificando se a win tá aberta
        if self.tooltip_win is not None:
            return None
        self.logger.debug(f'Mostrando o tooltip: {self.short_text}')
        # Criando ela caso não esteja.
        x = self.widget.winfo_rootx() + 5
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tooltip_win = ctk.CTkToplevel(self.master_widget)
        self.tooltip_win.wm_overrideredirect(True)
        self.tooltip_win.geometry(f'+{x}+{y}')

        # Configurando o label da classe
        data_font = self.data_config['font']
        self.label = ctk.CTkLabel(
            self.tooltip_win,
            text=self.text,
            font=ctk.CTkFont(
                data_font[0], weight=data_font[1], size=data_font[2]
            ),
            text_color=self.data_config['color_theme'],
            corner_radius=5,
        )
        self.label.pack(padx=5, pady=2)

    def _hide_tooltip(self, event=None) -> None:
        """Met. q escode a dica."""
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None

        if self.tooltip_win:
            self.logger.debug(f'Escondendo o tooltip: {self.short_text}')
            self.tooltip_win.destroy()
            self.tooltip_win = None
