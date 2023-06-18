import customtkinter as ctk

class UrlEntryBox(ctk.CTkEntry):
    def __init__(self, *args, **kwargs):
        self.URL_STRING = ctk.StringVar(value = "Вставте посилання на зображення (URL)")
        super().__init__(*args, textvariable = self.URL_STRING, **kwargs)
    