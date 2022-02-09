from src.gui.gui_logic.logic import Logic


class PopUpLogic(Logic):

    def __init__(self, my_view, parent_view, callback):
        super().__init__(my_view, parent_view)
        self.callback = callback
        self.parent_view = parent_view
        self.parent_view_logic = parent_view.get_view_logic()

    def change_title(self, new_title):
        self.my_view.title_label.set_title(new_title)

    def change_message(self, new_message):
        self.my_view.message_label.set_title(new_message)

    def change_button_text(self, new_text):
        self.my_view.button_label.set_title(new_text)

    def close_pop_up(self):
        if self.callback is not None:
            self.callback()
        self.back_to_parent_view()
