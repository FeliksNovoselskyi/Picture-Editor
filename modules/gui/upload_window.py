import customtkinter as ctk

import modules.commands as commands
import modules.gui as gui
import modules.utils as utils

class UploadWindow(ctk.CTk):
    def __init__(self, width, height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.iconbitmap(utils.get_full_path("resources/images/icons/create.ico"))
        
        self.WIDTH = width
        self.HEIGHT = height
        self.DESTROYED = False
        
        self.TAB_VIEW = ctk.CTkTabview(
            master = self,
            width = self.WIDTH,
            height = self.HEIGHT,
            border_width = 4
        )
            
        self.CHOOSE_IMAGE_FRAME = self.TAB_VIEW.add("Обрати зображення з ПК")
        self.LOAD_URL_IMAGE_FRAME = self.TAB_VIEW.add("Завантажити зображення з URL")
        
        choose_img_button = ctk.CTkButton(
            master = self.CHOOSE_IMAGE_FRAME,
            width = 190,
            height = 65,
            text = "Обрати...",
            command = commands.choose_image
        )
        choose_img_button.place(
            x = self.WIDTH // 2 - 95,
            y = self.HEIGHT // 2 - 65,    
        )
        
        load_url_img_button = ctk.CTkButton(
            master = self.LOAD_URL_IMAGE_FRAME,
            width = 190,
            height = 30,
            text = "Завантажити",
            command = commands.load_image_from_url
        )
        load_url_img_button.place(
            x = self.WIDTH // 2 - 95,
            y = 150
        )
        
        self.URL_ENTRY_BOX = gui.UrlEntryBox(
            master = self.LOAD_URL_IMAGE_FRAME, 
            width = self.WIDTH - 30,
            height = 30
        )
        
        self.WARNING_STRING = ctk.StringVar(value = "")
        self.WARNING_LABEL = ctk.CTkLabel(
            master = self.LOAD_URL_IMAGE_FRAME,
            width = 15,
            height = 15,
            textvariable = self.WARNING_STRING,
            text = ""
        )
        
        self.WARNING_LABEL.place(x = self.WIDTH // 2 - 20,  y = 70)
        
        self.URL_ENTRY_BOX.place(x = self.WIDTH // 2 - (self.WIDTH - 20) // 2, y = 110)
        
        self.TAB_VIEW.place(x = 0, y = 0)
        
        center_x = self.winfo_screenwidth() // 2 - self.WIDTH // 2
        center_y = self.winfo_screenheight() // 2 - self.HEIGHT // 2
        
        #
        self.geometry(f'{self.WIDTH}x{self.HEIGHT}+{center_x}+{center_y}')
        self.resizable(False, False)
        self.title("Завантаження картинки")
    
    def destroy(self):
        self.DESTROYED = True
        super().destroy()