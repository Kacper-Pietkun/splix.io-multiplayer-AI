class Logic:
    def __init__(self, my_view, parent_view):
        self.my_view = my_view
        self.parent_view = parent_view

    def back_to_parent_view(self):
        if self.parent_view is not None:
            self.my_view.reset_view()
            self.parent_view.reset_view()
            self.parent_view.display_menu()
