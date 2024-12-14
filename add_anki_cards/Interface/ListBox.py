from CTkListbox import CTkListbox


class ListBox(CTkListbox):
    '''Classe adapitada para comportar o scroll do mouse.'''

    def __init__(self, parent, **kwargs):
        '''Iniciação da classe com alterações para o scroll.'''
        super().__init__(parent, **kwargs)

        # Bind de todos os eventos para a mesma função
        self.bind_all('<MouseWheel>', self._on_mouse_scroll)  # Windows/macOS
        self.bind_all('<Button-4>', self._on_mouse_scroll)    # Linux scroll up
        # Linux scroll down
        self.bind_all('<Button-5>', self._on_mouse_scroll)

    def _on_mouse_scroll(self, event=None) -> None:
        """Manipula o scroll do mouse em diferentes sistemas operacionais."""
        if hasattr(event, 'num'):  # Linux: evento tem atributo `num`
            if event.num == 4:  # Scroll up
                self._parent_canvas.yview_scroll(-1, 'units')
            elif event.num == 5:  # Scroll down
                self._parent_canvas.yview_scroll(1, 'units')
        # Windows/macOS: evento tem atributo `delta`
        elif hasattr(event, 'delta'):
            self._parent_canvas.yview_scroll(
                -1 * (event.delta // 120),
                'units',
            )
