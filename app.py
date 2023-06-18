import customtkinter as ctk
from PIL import Image

import modules.commands as commands
import modules.gui as gui
import modules.utils as utils

#
SETTINGS = utils.read_json(
    json_path=utils.get_full_path('settings.json')
)
#
class App(ctk.CTk):
    def __init__(self):
        #
        super().__init__()

        self.WIDTH = SETTINGS["app_width"]
        self.HEIGHT = SETTINGS["app_height"]

        self.configure_sizes()
        self.protocol("WM_DELETE_WINDOW", commands.on_main_window_close)
        self.bind("<Configure>", self.on_resize_idle)  # Обработчик изменения размера окна
        self.color_theme_path = utils.get_full_path(SETTINGS['color_theme'])
        self.color_theme_colors = utils.read_json(
            json_path=self.color_theme_path
        )
        self.configure_app()
        self.create_windows()

        self.RESIZING = False

        self.IMAGE = gui.Imagee(
            master=self,
            width=self.IMAGE_WIDTH,
            height=self.IMAGE_HEIGHT,
            x=self.LISTBOX_WIDTH + self.MARGIN_X * 2,
            y=self.MARGIN_Y
        )

        self.SELECT_THEME = gui.SelectTheme(
            master=self,
            width=self.SELECT_THEME_WIDTH,
            height=self.SELECT_THEME_HEIGHT
        )
        self.SELECT_THEME.place(
            x=self.MARGIN_X,
            y=self.MARGIN_Y
        )

        self.tools_commands = (
            self.show_upload_window,
            self.IMAGE.crop_image,
            self.IMAGE.rotate_image,
            self.IMAGE.create_image,
            self.IMAGE.add_text,
            self.show_resize_window
        )

        self.filters_commands = (
            self.IMAGE.black_white_filter,
            self.IMAGE.contour_filter,
            self.IMAGE.blur_filter,
            self.IMAGE.detail_filter,
            self.IMAGE.edge_filter,
            self.IMAGE.emboss_filter,
            self.IMAGE.horror_filter,
        )

        #
        self.create_frames()
        self.place_frames()

        #
        self.create_tools_buttons()
        self.place_tools_buttons()

        self.create_filters_buttons()
        self.place_filters_buttons()

    def configure_app(self):
        ctk.set_default_color_theme(self.color_theme_path)
        self.configure(fg_color=self.color_theme_colors['CTk']['fg_color'][0])
        self.title("Редактор зображень")
        self.iconbitmap(utils.get_full_path("resources/images/icons/app_icon.ico"))
        self.resizable(False, False)
        self.center_app()

    def center_app(self):
        center_x = self.winfo_screenwidth() // 2 - self.WIDTH // 2
        center_y = self.winfo_screenheight() // 2 - self.HEIGHT // 2
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{center_x}+{center_y}")

    def configure_sizes(self):
        self.UPLOAD_WINDOW_WIDTH = 400
        self.UPLOAD_WINDOW_HEIGHT = 350
        self.BUTTONS_FRAME_WIDTH = self.WIDTH // 2
        self.BUTTONS_FRAME_HEIGHT = 65
        self.FILTERS_FRAME_WIDTH = self.WIDTH // 2
        self.FILTERS_FRAME_HEIGHT = 65
        self.MARGIN_X = 20
        self.MARGIN_Y = 20
        self.BTN_MARGIN_X = 22
        self.BTN_MARGIN_Y = 10
        self.LISTBOX_WIDTH = 250
        self.IMAGE_WIDTH = self.WIDTH - self.LISTBOX_WIDTH - self.MARGIN_X * 3
        self.IMAGE_HEIGHT = self.HEIGHT - self.BUTTONS_FRAME_HEIGHT - self.MARGIN_Y * 3

        self.TOOLS_BUTTONS_WIDTH = self.BUTTONS_FRAME_WIDTH // 6 - 20
        self.FILTERS_BUTTONS_WIDTH = self.BUTTONS_FRAME_WIDTH // 7 - 20
        self.BUTTON_HEIGHT = self.BUTTONS_FRAME_HEIGHT - 20

        self.INFO_FRAME_WIDTH = 250
        self.INFO_FRAME_HEIGHT = 150
        self.IMAGES_FRAME_WIDTH = 225
        self.SELECT_THEME_WIDTH = self.INFO_FRAME_WIDTH
        self.SELECT_THEME_HEIGHT = 20
        self.IMAGES_FRAME_HEIGHT = (
            self.HEIGHT
            - self.INFO_FRAME_HEIGHT
            - self.BUTTONS_FRAME_HEIGHT
            - self.MARGIN_Y * 6
            - self.SELECT_THEME_HEIGHT
            + 5
        )

    def create_tools_buttons(self):
        self.TOOLS_BUTTONS = []

        for image_path, command in zip(SETTINGS["tools_icons"], self.tools_commands):
            image_path = utils.get_full_path(image_path)

            self.TOOLS_BUTTONS.append(
                ctk.CTkButton(
                    master=self.BUTTONS_FRAME,
                    width=self.TOOLS_BUTTONS_WIDTH,
                    height=self.BUTTON_HEIGHT,
                    border_width=1,
                    corner_radius=6,
                    text="",
                    command=command,
                    image=ctk.CTkImage(dark_image=Image.open(image_path), size=(35, 35)),
                )
            )

    def create_filters_buttons(self):
        self.FILTERS_BUTTONS = []

        for image_path, command in zip(SETTINGS["filters_icons"], self.filters_commands):
            image_path = utils.get_full_path(image_path)

            self.FILTERS_BUTTONS.append(
                ctk.CTkButton(
                    master=self.FILTERS_FRAME,
                    width=self.FILTERS_BUTTONS_WIDTH,
                    height=self.BUTTON_HEIGHT,
                    border_width=1,
                    corner_radius=6,
                    text="",
                    command=command,
                    image=ctk.CTkImage(dark_image=Image.open(image_path), size=(35, 35)),
                )
            )

    def place_tools_buttons(self):
        for i, button in enumerate(self.TOOLS_BUTTONS):
            button.place(
                x=self.BTN_MARGIN_X + self.BTN_MARGIN_X // 2 * (i + 1) + self.TOOLS_BUTTONS_WIDTH * i - 12,
                y=self.BTN_MARGIN_Y
            )

    def place_filters_buttons(self):
        for i, filter in enumerate(self.FILTERS_BUTTONS):
            filter.place(
                x=self.BTN_MARGIN_X + self.BTN_MARGIN_X // 2 * (i + 1) + self.FILTERS_BUTTONS_WIDTH * i - 15,
                y=self.BTN_MARGIN_Y
            )

    def create_frames(self):
        self.BUTTONS_FRAME = ctk.CTkFrame(
            master=self,
            width=self.BUTTONS_FRAME_WIDTH - self.MARGIN_X,
            height=self.BUTTONS_FRAME_HEIGHT,
            corner_radius=8
        )
        self.FILTERS_FRAME = ctk.CTkFrame(
            master=self,
            width=self.FILTERS_FRAME_WIDTH - self.MARGIN_X * 2,
            height=self.FILTERS_FRAME_HEIGHT,
            corner_radius=8
        )

        self.IMAGES_FRAME = gui.ImagesFrame(
            master=self,
            width=self.IMAGES_FRAME_WIDTH,
            height=self.IMAGES_FRAME_HEIGHT,
        )

        self.INFO_FRAME = gui.InfoFrame(
            master=self,
            width=self.INFO_FRAME_WIDTH,
            height=self.INFO_FRAME_HEIGHT
        )

    def place_frames(self):
        self.BUTTONS_FRAME.place(
            x=self.MARGIN_X,
            y=self.HEIGHT - self.BUTTONS_FRAME_HEIGHT - self.MARGIN_Y,
        )

        self.FILTERS_FRAME.place(
            x=self.MARGIN_X + self.FILTERS_FRAME_WIDTH,
            y=self.HEIGHT - self.FILTERS_FRAME_HEIGHT - self.MARGIN_Y
        )

        self.IMAGES_FRAME.place(
            x=self.MARGIN_X,
            y=self.INFO_FRAME_HEIGHT + self.MARGIN_Y * 4
        )
        self.INFO_FRAME.place(
            x=self.MARGIN_X,
            y=self.MARGIN_Y * 2 + self.SELECT_THEME_HEIGHT
        )

    def create_windows(self):
        self.UPLOAD_WINDOW = None
        self.RESIZE_WINDOW = None

    def show_upload_window(self):
        if isinstance(self.UPLOAD_WINDOW, gui.UploadWindow):
            if not self.UPLOAD_WINDOW.DESTROYED:
                self.UPLOAD_WINDOW.destroy()

        self.UPLOAD_WINDOW = gui.UploadWindow(
            width=self.UPLOAD_WINDOW_WIDTH,
            height=self.UPLOAD_WINDOW_HEIGHT
        )
        self.UPLOAD_WINDOW.mainloop()

    def show_resize_window(self):
        if isinstance(self.RESIZE_WINDOW, gui.ResizeWindow):
            if not self.RESIZE_WINDOW.DESTROYED:
                self.RESIZE_WINDOW.destroy()

        self.RESIZE_WINDOW = gui.ResizeWindow()
        self.RESIZE_WINDOW.mainloop()

    def on_resize_idle(self, event):
        pass
        # if self.RESIZING:
        #     return
        # self.RESIZING = True

        # self.WIDTH = self.winfo_width()
        # self.HEIGHT = self.winfo_height()
        # self.configure_sizes()

        # self.IMAGE.IMAGE_LABEL.place(x=self.LISTBOX_WIDTH + self.MARGIN_X * 2, y=self.MARGIN_Y)

        # self.SELECT_THEME.configure(width=self.SELECT_THEME_WIDTH, height=self.SELECT_THEME_HEIGHT)
        # self.SELECT_THEME.place(x=self.MARGIN_X, y=self.MARGIN_Y)

        # for button in self.TOOLS_BUTTONS:
        #     button.configure(width=self.TOOLS_BUTTONS_WIDTH, height=self.BUTTON_HEIGHT)

        # for filter_button in self.FILTERS_BUTTONS:
        #     filter_button.configure(width=self.FILTERS_BUTTONS_WIDTH, height=self.BUTTON_HEIGHT)

        # self.BUTTONS_FRAME.configure(width=self.BUTTONS_FRAME_WIDTH - self.MARGIN_X, height=self.BUTTONS_FRAME_HEIGHT)
        # self.FILTERS_FRAME.configure(width=self.FILTERS_FRAME_WIDTH - self.MARGIN_X * 2, height=self.FILTERS_FRAME_HEIGHT)
        # self.IMAGES_FRAME.configure(width=self.IMAGES_FRAME_WIDTH, height=self.IMAGES_FRAME_HEIGHT)
        # self.INFO_FRAME.configure(width=self.INFO_FRAME_WIDTH, height=self.INFO_FRAME_HEIGHT)

        # self.IMAGE.resize_visible_image(self.IMAGE_WIDTH, self.IMAGE_HEIGHT)
        # self.place_tools_buttons()
        # self.place_filters_buttons()
        # self.place_frames()

        # self.RESIZING = False
            
main_app = App()
