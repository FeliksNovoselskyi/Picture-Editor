import customtkinter as ctk
import modules.utils as utils
from PIL import Image, ImageFilter, ImageTk, ImageDraw, ImageFont
import app
# import os
import shutil
from tkinter import messagebox

class Imagee:
    def __init__(self, master, width, height, x, y):
        
        self.WIDTH = width
        self.HEIGHT = height
        self.MASTER = master
        self.X = x
        self.Y = y

        self.CROP_X1 = None
        self.CROP_Y1 = None
        self.CROP_X2 = None
        self.CROP_Y2 = None
        
        self.CREATED_IMAGES = 0
        self.ADDED_TEXT = False
        
        
        self.IMAGE_PATH = utils.get_full_path('resources/images/dev/default.png')
        self.START_IMAGE_PATH = utils.get_full_path('resources/images/dev/default.png')
        self.PIL_IMAGE = Image.open(self.IMAGE_PATH)
        
        self.START_IMAGE = ctk.CTkImage(
            dark_image=self.PIL_IMAGE,
            size=(self.WIDTH, self.HEIGHT)
        )
        
        self.IMAGE_LABEL = None
        self.IMAGE = None
        self.show_image()
    
    def bind_crop_image(self, unbind=False):
        if not unbind:
            self.IMAGE_LABEL.bind("<Button-1>", self.on_crop_mouse_down)
            self.IMAGE_LABEL.bind("<B1-Motion>", self.on_crop_mouse_drag)
            self.IMAGE_LABEL.bind("<ButtonRelease-1>", self.on_crop_mouse_up)
        else:
            self.IMAGE_LABEL.unbind("<Button-1>") 
            self.IMAGE_LABEL.unbind("<B1-Motion>")
            self.IMAGE_LABEL.unbind("<ButtonRelease-1>")
    
    def bind_add_text(self, unbind = False):
        if not unbind:
            self.IMAGE_LABEL.bind("<Button-1>", self.on_add_text_mouse_down)
        else:
            self.IMAGE_LABEL.unbind("<Button-1>")
    
    def on_crop_mouse_down(self, event):
        self.select_zone = ctk.CTkFrame(
            master=self.IMAGE_LABEL,
            width=20,
            height=20,
            fg_color='white',
            bg_color='transparent',
            border_width=2,
            border_color="red"
        )
        
        self.CROP_X1 = int(event.x * self.PIL_IMAGE.width / app.main_app.IMAGE_WIDTH)
        self.CROP_Y1 = int(event.y * self.PIL_IMAGE.height / app.main_app.IMAGE_HEIGHT)
        
        self.select_zone.place(x=event.x, y=event.y)
    
    def on_crop_mouse_drag(self, event):
        new_width = event.x - self.select_zone.winfo_x()
        new_height = event.y - self.select_zone.winfo_y()
        
        self.select_zone.configure(
            width=new_width,
            height=new_height
        )
            
    def on_crop_mouse_up(self, event):
        self.CROP_X2 = int(event.x * self.PIL_IMAGE.width / app.main_app.IMAGE_WIDTH)
        self.CROP_Y2 = int(event.y * self.PIL_IMAGE.height / app.main_app.IMAGE_HEIGHT)
        
        self.bind_crop_image(unbind=True)
        self.select_zone.destroy()
        
        self.PIL_IMAGE = self.PIL_IMAGE.crop((self.CROP_X1, self.CROP_Y1, self.CROP_X2, self.CROP_Y2))
        self._handle_image()
    
    def on_add_text_mouse_down(self, event):
        if not self.ADDED_TEXT:
            self.ADDED_TEXT = True
            self.bind_add_text(unbind = True)
            self.position = (
                int(event.x * self.PIL_IMAGE.width / app.main_app.IMAGE_WIDTH),
                int(event.y * self.PIL_IMAGE.height / app.main_app.IMAGE_HEIGHT)
            )
            self.TEXT_ENTRY_BOX = ctk.CTkEntry(
                master = self.IMAGE_LABEL,
                width = 250,
                height = 60,
                corner_radius = 0
            )
            
            self.TEXT_ENTRY_BOX.place(x = event.x, y = event.y)
        
            self.CONFIRM_BUTTON = ctk.CTkButton(
                master = self.IMAGE_LABEL,
                width = 40,
                height = 40,
                text = "",
                corner_radius = 0,
                image = ctk.CTkImage(dark_image = Image.open('resources/images/buttons/tools/confirm.png'), size = (35, 35)),
                command = self.add_text_to_image
            )
                
            self.CANCEL_BUTTON = ctk.CTkButton(
                master = self.IMAGE_LABEL,
                width = 40,
                height = 40,
                text = '',
                corner_radius = 0,
                image = ctk.CTkImage(dark_image = Image.open('resources/images/buttons/tools/cancel.png'), size = (35, 35)),
                command = self.on_cancel_add_text 
            )
            
            self.CONFIRM_BUTTON.place(
                x = event.x + self.TEXT_ENTRY_BOX._current_width - self.CANCEL_BUTTON._current_width * 2 - 10,
                y = event.y + self.TEXT_ENTRY_BOX._current_height + 10
            )
            
            self.CANCEL_BUTTON.place(
                x = event.x + self.TEXT_ENTRY_BOX._current_width - self.CANCEL_BUTTON._current_width,
                y = event.y + self.TEXT_ENTRY_BOX._current_height + 10
            )
    
    def add_text_to_image(self):
        image_with_text = self.PIL_IMAGE.copy()
        draw = ImageDraw.Draw(image_with_text)
        font = ImageFont.truetype(utils.get_full_path("resources/fonts/times_new_roman.ttf"), 50)
        draw.text(self.position, self.TEXT_ENTRY_BOX.get(), font=font, fill='black')
        self.PIL_IMAGE = image_with_text
        self.TEXT_ENTRY_BOX.destroy()
        self.bind_add_text(unbind = True)
        self._handle_image()
        self.ADDED_TEXT = False


    def on_cancel_add_text(self):
        self.TEXT_ENTRY_BOX.destroy()
        self.CONFIRM_BUTTON.destroy()
        self.CANCEL_BUTTON.destroy()
        self.bind_add_text(unbind = True)
        self.ADDED_TEXT = False

    def show_image(self):
        if not self.IMAGE_LABEL:
            self.IMAGE_LABEL = ctk.CTkLabel(
                master=self.MASTER,
                text='',
                image=self.START_IMAGE
            )
        else:
            self.PIL_IMAGE = Image.open(self.IMAGE_PATH)
            app.main_app.INFO_FRAME.show_info(self.PIL_IMAGE)
            self.IMAGE = ctk.CTkImage(
                dark_image=self.PIL_IMAGE,
                size=(self.WIDTH, self.HEIGHT)
            )
            self.IMAGE_LABEL = ctk.CTkLabel(
                master=self.MASTER,
                text='',
                image=self.IMAGE
            )
        self.IMAGE_LABEL.place(
            x=self.X,
            y=self.Y
        )
    
    def _handle_image(self):
        self.IMAGE_LABEL.destroy()
        
        if self.IMAGE_PATH != self.START_IMAGE_PATH:
            self.PIL_IMAGE.save(self.IMAGE_PATH)
        
        app.main_app.IMAGES_FRAME.show_list_images()
        self.show_image()
    
    def rotate_image(self):   
        self.PIL_IMAGE = self.PIL_IMAGE.rotate(-90, expand=True)
        self._handle_image()
        
    def crop_image(self):
        self.bind_crop_image()
        
    def create_image(self): 
        dst_path = utils.get_full_path(f'resources/images/user_images/new_image_{self.CREATED_IMAGES}.png')
        shutil.copy2(
            src=self.START_IMAGE_PATH,
            dst=dst_path
        )
        app.main_app.IMAGES_FRAME.IMAGES.append(dst_path)
        self.CREATED_IMAGES += 1
        self._handle_image()
    
    def resize_image(self):
        try:
            new_width = int(app.main_app.RESIZE_WINDOW.WIDTH_ENTRY_BOX.get())
            new_height = int(app.main_app.RESIZE_WINDOW.HEIGHT_ENTRY_BOX.get())

            if new_width >= 10_000 or new_height >= 10_000:
                messagebox.showwarning(
                    "Помилка зміни розміру",
                    "Увага! Ви не можете змінити розмір зображення, якщо ширина або висота досягає 10 000 пікселів, чи більше! Це може сказатися на вашій системі!"
                )
            else:
                self.PIL_IMAGE = self.PIL_IMAGE.resize(
                    size = (new_width, new_height)       
                )
                self._handle_image()
        
        except ValueError:
            messagebox.showerror(
                "Помика зміни розміру",
                "Будь ласка, вкажіть коректні розмірі!"
            )
        finally:
            app.main_app.RESIZE_WINDOW.destroy()
        
    def resize_visible_image(self, new_width, new_height):
        self.IMAGE = ctk.CTkImage(
            dark_image=self.PIL_IMAGE,
            size=(new_width, new_height)
        )
        self.IMAGE_LABEL.configure(image=self.IMAGE)
    

    def black_white_filter(self):
        self.PIL_IMAGE = self.PIL_IMAGE.convert("L")
        self._handle_image()
    
    def contour_filter(self):
        self.PIL_IMAGE = self.PIL_IMAGE.filter(ImageFilter.CONTOUR)
        self._handle_image()
    
    def blur_filter(self):
        self.PIL_IMAGE = self.PIL_IMAGE.filter(ImageFilter.BLUR)
        self._handle_image()

    def detail_filter(self):
        self.PIL_IMAGE = self.PIL_IMAGE.filter(ImageFilter.DETAIL)
        self._handle_image()
        
    def edge_filter(self):
        self.PIL_IMAGE = self.PIL_IMAGE.filter(ImageFilter.EDGE_ENHANCE)
        self._handle_image()

    def emboss_filter(self):
        self.PIL_IMAGE = self.PIL_IMAGE.filter(ImageFilter.EMBOSS)
        self._handle_image()
        
    def horror_filter(self):
        self.PIL_IMAGE = self.PIL_IMAGE.filter(ImageFilter.FIND_EDGES)
        self._handle_image()
    
    def add_text(self):
        self.bind_add_text()
