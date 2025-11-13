import customtkinter

class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("wMusicSorter")
        customtkinter.set_appearance_mode("dark")

        self.__create_login_page()

    def __create_login_page(self):
        self.client_id_entry = customtkinter.CTkEntry(self, placeholder_text="Spotify Client ID")
        self.client_id_entry.pack(pady=20, padx=20)

        self.client_secret_entry = customtkinter.CTkEntry(self, placeholder_text="Spotify Client Secret")
        self.client_secret_entry.pack(pady=20, padx=20)

        button = customtkinter.CTkButton(self, text="Log In", command=self.login_event)
        button.pack(pady=20, padx=20)

    def login_event(self):
        print(self.client_id_entry.get())
        print(self.client_secret_entry.get())