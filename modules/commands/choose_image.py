import os
import shutil
from tkinter import filedialog

import app
import modules.utils as utils


def choose_image(): 
    try:
        with filedialog.askopenfile(mode = 'r',
                                    filetypes = app.SETTINGS["supported_import_types"]
                                    ) as image:
            
            image_path = image.name
            images_path = utils.get_full_path("resources/images/user_images")
            shutil.copy2(image_path, images_path)
            
            image_name = os.path.split(image_path)[1]
            image_path = utils.get_full_path(os.path.join(f"resources/images/user_images/{image_name}"))
            
            if image_path not in app.main_app.IMAGES_FRAME.IMAGES:
                app.main_app.IMAGES_FRAME.IMAGES.append(image_path)
            app.main_app.IMAGES_FRAME.show_list_images()
            
    except TypeError: pass
    except FileNotFoundError: pass
    
    finally:
        app.main_app.UPLOAD_WINDOW.destroy()
