from src.gui.gui_logic.logic import Logic
from src.constants import constant
from src.management.game_managers.neat_training_manager import NeatTrainingManager
from src.gui.gui_view.pop_up_view import PopUpView


class BotsTrainingMenuLogic(Logic):

    def __init__(self, my_view, parent_view):
        super().__init__(my_view, parent_view)

    def train_new_neat_bots(self):
        neat_training_manager = NeatTrainingManager(constant.TRAINING_MAX_FPS, constant.VISUALIZE_TRAINING, self.my_view.window)
        neat_training_manager.run()

    def train_saved_neat_bots(self):
        neat_training_manager = NeatTrainingManager(constant.TRAINING_MAX_FPS, constant.VISUALIZE_TRAINING, self.my_view.window)
        try:
            neat_training_manager.load_population()
            neat_training_manager.run()
        except IOError as e:
            pop_up_view = PopUpView(self.my_view, 'Warning', 'You did not save any neat bots', 'ok', None)
            pop_up_view.display_menu()
