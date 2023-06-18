import customtkinter as ctk



class InfoFrame(ctk.CTkFrame):
    def __init__(self, **kwargs):
        super().__init__(
            master = kwargs['master'],
            width = kwargs['width'],
            height = kwargs['height']
        ) 
        
        
        self.LABEL_WIDTH, self.LABEL_HEIGHT = 30, 20
        
        self.MARGIN_X = 10
        self.MARGIN_Y = 10
        
        self.IMAGE_SIZE = None
        self.IMAGE_MODE = None
        self.IMAGE_FORMAT = None
    
        self.SIZE_TEXTVARIABLE = ctk.StringVar()
        self.MODE_TEXTVARIABLE = ctk.StringVar()
        self.FORMAT_TEXTVARIABLE = ctk.StringVar()
        
        
        
        self.SIZE_LABEL = ctk.CTkLabel(
            master = self,
            width = self.LABEL_WIDTH, 
            height = self.LABEL_HEIGHT,
            textvariable = self.SIZE_TEXTVARIABLE
        )

        self.MODE_LABEL = ctk.CTkLabel(
            master = self,
            width = self.LABEL_WIDTH,
            height = self.LABEL_HEIGHT,
            textvariable = self.MODE_TEXTVARIABLE
        )
        
        self.FORMAT_LABEL = ctk.CTkLabel(
            master = self,
            width = self.LABEL_WIDTH,
            height = self.LABEL_HEIGHT,
            textvariable = self.FORMAT_TEXTVARIABLE
        )
        
        self.place_labels()
    
    
    def place_labels(self):
        self.SIZE_LABEL.place(x = self.MARGIN_X, y = self.MARGIN_Y)
        self.MODE_LABEL.place(x = self.MARGIN_X, y = self.LABEL_HEIGHT + self.MARGIN_Y)
        self.FORMAT_LABEL.place(x = self.MARGIN_X, y = self.LABEL_HEIGHT * 2 + self.MARGIN_Y)
    
    def destroy_lables(self):
        self.SIZE_LABEL.destroy()
        self.MODE_LABEL.destroy()
        self.FORMAT_LABEL.destroy()

    
    def show_info(self, pil_image):
        self.SIZE_TEXTVARIABLE.set(f"Розмір: {pil_image.size[0]}x{pil_image.size[1]}")
        self.MODE_TEXTVARIABLE .set(f"Кольорова модель: {pil_image.mode}")
        self.FORMAT_TEXTVARIABLE.set(f"Формат: {pil_image.format}")
        
    def get_info(self, pil_image):
        self.IMAGE_SIZE = pil_image.size
        self.IMAGE_MODE = pil_image.mode
        self.IMAGE_FORMAT = pil_image.format
    
    