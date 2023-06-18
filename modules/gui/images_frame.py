import customtkinter as ctk
from PIL import Image
import app
import modules.utils as utils
import os
from tkinter import filedialog
import shutil


class ImageFrame(ctk.CTkFrame):
    def __init__(self, **kwargs):
        super().__init__(
            master = kwargs["master"],
            width = kwargs["width"],
            height = kwargs["height"],
            border_width = kwargs["border_width"]
        )
        self.WIDTH = kwargs['width']
        self.HEIGHT = kwargs['height']
        self.BORDER_WIDTH = kwargs["border_width"]

        self.MARGIN_X = 5
        self.MARGIN_Y = 5
        self.MARGIN_IMAGE_Y = 20
        
        self.IMAGE_WIDTH = 100
        self.IMAGE_HEIGHT = self.HEIGHT - self.BORDER_WIDTH
        
        self.BUTTON_WIDTH = 30
        self.BUTTON_HEIGHT = 30
        
        self.IMAGE_PATH = kwargs["image_path"]
        self.IMAGE = ctk.CTkImage(
            dark_image = Image.open(self.IMAGE_PATH),
            size = (self.IMAGE_WIDTH, self.IMAGE_HEIGHT - self.MARGIN_IMAGE_Y)
        )
        ctk.CTkLabel(
            master = self,
            image = self.IMAGE,
            text = ''
        ).place(x = self.MARGIN_X, y = self.BORDER_WIDTH + self.MARGIN_IMAGE_Y // 2)
        
        self.SHOW_BUTTON = ctk.CTkButton(
            master = self,
            width = self.BUTTON_WIDTH,
            height = self.BUTTON_HEIGHT,
            image = ctk.CTkImage(dark_image = Image.open(utils.get_full_path(app.SETTINGS["image_frame_icons"][0])), size = (30, 30)),
            text = '',
            command = self.select_image
        )
        self.DELETE_BUTTON = ctk.CTkButton(
            master = self,
            width = self.BUTTON_WIDTH,
            height = self.BUTTON_HEIGHT,
            image = ctk.CTkImage(dark_image = Image.open(utils.get_full_path(app.SETTINGS["image_frame_icons"][2])), size = (30, 30)),
            text = '',
            command = self.delete_image
        )
        self.HIDE_BUTTON = ctk.CTkButton(
            master = self,
            width = self.BUTTON_WIDTH,
            height = self.BUTTON_HEIGHT,
            image = ctk.CTkImage(dark_image = Image.open(utils.get_full_path(app.SETTINGS["image_frame_icons"][1])), size = (30, 30)),
            text = '',
            command = self.hide_image
        )
        self.SAVE_BUTTON = ctk.CTkButton(
            master = self,
            width = self.BUTTON_WIDTH,
            height = self.BUTTON_HEIGHT,
            image = ctk.CTkImage(dark_image = Image.open(utils.get_full_path(app.SETTINGS["image_frame_icons"][3])), size = (30, 30)),
            text = '',
            command = self.save_image
        )
        
        
        self.SHOW_BUTTON.place(
            x = self.IMAGE_WIDTH + self.MARGIN_X * 2, 
            y = self.MARGIN_Y + self.HEIGHT // 2 - self.BUTTON_HEIGHT // 2 - 30
        )
        self.HIDE_BUTTON.place(
            x = self.IMAGE_WIDTH + self.BUTTON_WIDTH + self.MARGIN_X * 6,
            y = self.MARGIN_Y + self.HEIGHT // 2 - self.BUTTON_HEIGHT // 2 - 30
        )
        self.DELETE_BUTTON.place(
            # x = self.WIDTH // 2 + self.BUTTON_WIDTH // 2 + 10,
            x = self.IMAGE_WIDTH + self.MARGIN_X * 2,
            y = self.MARGIN_Y * 2 + self.HEIGHT // 2 - self.BUTTON_HEIGHT // 2 - 20 + self.BUTTON_HEIGHT
        )
        self.SAVE_BUTTON.place(
            x = self.IMAGE_WIDTH + self.BUTTON_WIDTH + self.MARGIN_X * 6,
            y = self.MARGIN_Y * 2 + self.HEIGHT // 2 - self.BUTTON_HEIGHT // 2 - 20 + self.BUTTON_HEIGHT
        )

    def select_image(self):
        app.main_app.IMAGE.IMAGE_PATH = self.IMAGE_PATH
        app.main_app.IMAGE.show_image()
    
    def hide_image(self):
        if app.main_app.IMAGE.IMAGE_PATH != app.main_app.IMAGE.START_IMAGE_PATH:
            app.main_app.IMAGE.IMAGE_LABEL.destroy()
            app.main_app.IMAGE.IMAGE_PATH = app.main_app.IMAGE.START_IMAGE_PATH
            app.main_app.IMAGE.show_image()
        
        
    def delete_image(self):
        self.destroy()
        # app.main_app.INFO_FRAME.destroy_lables()
        app.main_app.IMAGES_FRAME.IMAGES.remove(self.IMAGE_PATH)
        os.remove(self.IMAGE_PATH)
        self.hide_image()
        
        for image_frame in app.main_app.IMAGES_FRAME.winfo_children():
            image_frame.grid_forget()
        
        app.main_app.IMAGES_FRAME.show_list_images()
        
    def save_image(self):
        try:
            image_path = filedialog.asksaveasfilename(
                defaultextension = ".png",
                filetypes = app.SETTINGS["supported_export_types"],
                initialfile = os.path.split(self.IMAGE_PATH)[1]
            )
            shutil.copy2(
                src = self.IMAGE_PATH,
                dst = image_path
            )
        except FileNotFoundError: pass
    
    
            
class ImagesFrame(ctk.CTkScrollableFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.WIDTH = kwargs['width']
        self.HEIGHT = kwargs['height']
        self.MARGIN_X = 5
        self.MARGIN_Y = 5
        self.IMAGE_FRAME_WIDTH = self.WIDTH - self.MARGIN_Y * 2
        self.IMAGE_FRAME_HEIGHT = 120
        self.IMAGES = []
        
    
    def show_list_images(self):
        for i, image_path in enumerate(self.IMAGES):
            if image_path:
                image_frame = ImageFrame(
                    master = self,
                    width = self.WIDTH - self.MARGIN_X * 2,
                    height = self.IMAGE_FRAME_HEIGHT,
                    border_width = 1,
                    image_path = image_path
                )
                image_frame.grid(row = i, column = 0, padx = self.MARGIN_X, pady = self.MARGIN_Y)
