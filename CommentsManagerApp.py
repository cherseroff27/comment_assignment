import os
import sys
import tkinter as tk
from pathlib import Path
from CommentsManagerUI import CommentsManagerUI
from CommentsManagerUILogic import CommentsManagerUILogic
from CommentsGeneratorManager import CommentsGeneratorManager
from InitialDataConfigManager import InitialDataConfigManager
from archive.app import config_dir

from logger_config import Logger

logger = Logger.get_logger(__name__)

DEFAULT_DIR_NAMES = {
    'DEFAULT_BROWSER_PROFILES_DIR': "browser_profiles",
    'DEFAULT_CONFIGS_DIR': "configs",
}

CONFIG_NAMES = {
    "INITIAL_DATA_CONFIG_NAME": "initial_data_config.json",
}

class CommentsManagerApp:
    def __init__(self, default_paths: dict):
        self.root = tk.Tk()
        self.initial_data_config_manager = InitialDataConfigManager()
        self.comments_generator_manager = CommentsGeneratorManager()
        self.logic = CommentsManagerUILogic(
            initial_data_config_manager=self.config_manager,
            default_browser_profiles_dir=default_paths["DEFAULT_BROWSER_PROFILES_DIR"],
            comments_generator_manager=self.comments_generator_manager,
        )
        self.ui = CommentsManagerUI(
            root=self.root,
            logic=self.logic,
        )

    def run(self):
        self.root.mainloop()


def get_root_path():
    if getattr(sys, 'frozen', False):
        return Path(getattr(sys, '_MEIPASS', Path.cwd()))
    else:
        return Path(__file__).resolve().parent


def create_required_directories(root_path: Path):
    default_paths = {}

    for key in DEFAULT_DIR_NAMES:
        default_paths[key] = (root_path / DEFAULT_DIR_NAMES[key])

    for key in default_paths:
        default_paths[key].mkdir(parents=True, exist_ok=True)

    return default_paths


if __name__ == "__main__":
    root_dir_path = get_root_path()

    default_dir_paths = create_required_directories(root_dir_path)

    commentsManagerApp = CommentsManagerApp(
        default_paths = default_dir_paths
    )
    commentsManagerApp.run()

