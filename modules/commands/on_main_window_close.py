import os
import shutil

import app
import modules.utils as utils


def on_main_window_close():
    app.main_app.destroy()
    images_path = utils.get_full_path('resources/images/user_images')
    shutil.rmtree(images_path)
    os.mkdir(images_path)
    
    