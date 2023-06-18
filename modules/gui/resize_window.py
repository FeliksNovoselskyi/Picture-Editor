import customtkinter as ctk
import app
import modules.utils as utils

class ResizeWindow(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.WIDTH = 350
        self.HEIGHT = 150
        
        self.MARGIN_X = 10
        self.MARGIN_Y = 10
        
        self.iconbitmap(utils.get_full_path("resources/images/icons/resize.ico"))
        
        self.DESTROYED = False

        center_x = self.winfo_screenwidth() // 2 - self.WIDTH // 2
        center_y = self.winfo_screenheight() // 2 - self.HEIGHT // 2
        
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{center_x}+{center_y}")
        self.resizable(False, False)
        self.title("Зміна розміру зображеня")
        
        self.RESIZE_BUTTON = ctk.CTkButton(
            master = self,
            width = 330,
            height = 75,
            text = "Змінити розмір",
            command = app.main_app.IMAGE.resize_image
        )
        self.RESIZE_BUTTON.place(
            x = self.MARGIN_X,
            y = self.HEIGHT - 82
        )
        
        self.WIDTH_ENTRY_BOX = ctk.CTkEntry(
            master = self,
            width = 160,
            height = 50,
            placeholder_text = "Ширина"
        )
        
        self.HEIGHT_ENTRY_BOX = ctk.CTkEntry(
            master = self,
            width = 160,
            height = 50,
            placeholder_text = "Висота"
            
        )
        
        self.WIDTH_ENTRY_BOX.place(x = self.MARGIN_X, y = self.MARGIN_Y)
        self.HEIGHT_ENTRY_BOX.place(x = self.MARGIN_X * 2 + 160, y = self.MARGIN_Y)
    
    def destroy(self):
        self.DESTROYED = True
        super().destroy()
