import customtkinter as ctk
from PIL import Image
import app


class ShowButton(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.IMAGE = None
        self.LABEL = None

    def show_image(self):
        self.destroy_image()
        
        current_item = list(app.main_app.IMAGES_LISTBOX.curselection())[0]
        image_path = app.main_app.IMAGES_LISTBOX.ADDED_IMAGES[current_item] 
        
        self.IMAGE = ctk.CTkImage(
            dark_image = Image.open(image_path),
            size = (app.main_app.IMAGE_FRAME_WIDTH, app.main_app.IMAGE_FRAME_HEIGHT)
        ) 
        
        self.LABEL = ctk.CTkLabel(master = app.main_app, image = self.IMAGE, text = '')
        
        self.LABEL.place(x = app.main_app.INFO_FRAME_WIDTH + 25, y = 10)
    
    def destroy_image(self):
        if isinstance(self.LABEL, ctk.CTkLabel):
            self.LABEL.destroy()
            self.LABEL = None