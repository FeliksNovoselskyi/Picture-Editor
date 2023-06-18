import os
import urllib.error

import validators
import wget

import app
import modules.utils as utils

from tkinter import messagebox
import requests

def load_image_from_url():
    url = app.main_app.UPLOAD_WINDOW.URL_ENTRY_BOX.get()
    content_type = None

    if validators.url(url):
        try:
            r = requests.get(url)
            content_type = r.headers.get("Content-Type")

            if content_type:
                if "image" in content_type:
                    try:
                        os.chdir(utils.get_full_path("resources/images/user_images"))
                        image_name = wget.download(url, bar = None)
                        image_path = utils.get_full_path(image_name)
                        app.main_app.IMAGES_FRAME.IMAGES.append(image_path)
                        os.chdir(utils.get_full_path("../../.."))
                    except urllib.error.HTTPError: pass
                    finally:
                        app.main_app.UPLOAD_WINDOW.destroy()
                        app.main_app.IMAGES_FRAME.show_list_images()
                else:
                    messagebox.showerror(
                        "Проблема із завантаженням",
                        "Цей URL існує, але він не містить зображення. Будь ласка, вкажіть коректний URL!"
                    )
            
        except requests.exceptions.ConnectionError:
            messagebox.showerror(
                "Проблема із завантаженням",
                "Будь ласка, вкажіть коректний URL до зображення!"
            )
    else:
        messagebox.showerror(
            "Проблема із завантаженням",
            "Цей URL не існує! Будь ласка, вкажіть коректний URL!"
        )


