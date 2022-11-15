##make object oriented 
import tkinter as tk
import pyautogui as pg
import time
import pandas
import pyperclip
import json
import os


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.jsonPath = "preferences.json"
        self.last_x, self.last_y = 0, 0
        self.msg_tutorial_config = """
        1. Abrir el navegador en la pagina de tiktok en la pagina de subir video
        2. mover el mouse a la posicion de cada boton pedido
        3. presionar Enter para ver la posicion del mouse
        4. copiar la posicion del mouse y pegarla en la caja de texto correspondiente
        5. presionar el boton aplicar
        """

        
        #window settings
        self.title("Tiktok Uploader")
        # self.geometry("120x100")
        # self.resizable(False, False)

        self._read_preferences()
        self._create_widgets()
        self._home()
        # self._startup_tiktok_page()
        

    # def _startup_tiktok_page(self): TODO
    #     if self.TIKTOK_URL:
    #         os.system(f"start {self.TIKTOK_URL}")

    
    def _clear_and_write_entry(self, entry, text):
        entry.delete(0, tk.END)
        entry.insert(0, text)

    def _create_widgets(self):
        #home widgets
        self.boton_upload = tk.Button(self, text="Upload", command=self._upload_video)
        self.boton_upload.config(bg="green", fg="white", font=("helvetica", 12, "bold"))

        #publish
        self.boton_publish = tk.Button(self, text=f"Publish", command=self._publish)
        self.boton_publish.config(bg="red", fg="white", font=("helvetica", 12, "bold"))

        #config
        self.boton_configurar = tk.Button(self, text="Config", command=self._edit_preferences)
        self.boton_configurar.config(bg="blue", fg="white", font=("helvetica", 12, "bold"))

        #volver
        self.boton_volver = tk.Button(self, text="Back", command=self._home)
        self.boton_volver.config(bg="blue", fg="white", font=("helvetica", 8, "bold"))

        #config widgets
          #entrys

            #wait_hashtag_interval
        self.label_wait_hashtag_interval = tk.Label(self, text="Wait hashtag interval")
        self.entry_wait_hashtag_interval = tk.Entry(self)
        
        
            #wait_press_upload
        self.label_wait_press_upload = tk.Label(self, text="Wait press upload")
        self.entry_wait_press_upload = tk.Entry(self)
        
            #excel_path
        self.label_excel_path = tk.Label(self, text="Excel path")
        self.entry_excel_path = tk.Entry(self)

            #videos_folder_path
        self.label_videos_folder_path = tk.Label(self, text="Videos folder path")
        self.entry_videos_folder_path = tk.Entry(self)

            #position_upload_button
        # self.label_position_upload_button = tk.Label(self, text="upload button")
        # self.entry_position_upload_button = tk.Entry(self)
        # self.button_copy_position_upload_button = tk.Button(self, text="Copy↑", command=lambda: self._clear_and_write_entry(self.entry_position_upload_button, f"{self.last_x} {self.last_y}"))

            #position_title
        self.label_position_title = tk.Label(self, text="caption")
        self.entry_position_title = tk.Entry(self)
        self.button_copy_position_title = tk.Button(self, text="Copy↑", command=lambda: self._clear_and_write_entry(self.entry_position_title, f"{self.last_x} {self.last_y}"))

            #position_upload_file
        self.label_position_upload_file = tk.Label(self, text="select file")
        self.entry_position_upload_file = tk.Entry(self)
        self.button_copy_position_upload_file = tk.Button(self, text="Copy↑", command=lambda: self._clear_and_write_entry(self.entry_position_upload_file, f"{self.last_x} {self.last_y}"))

            #position_publish
        self.label_position_publish = tk.Label(self, text="post")
        self.entry_position_publish = tk.Entry(self)
        self.button_copy_position_publish = tk.Button(self, text="Copy↑", command=lambda: self._clear_and_write_entry(self.entry_position_publish, f"{self.last_x} {self.last_y}"))

            #position_copyright_check
        self.label_position_copyright_check = tk.Label(self, text="copyright check")
        self.entry_position_copyright_check = tk.Entry(self)
        self.button_copy_position_copyright_check = tk.Button(self, text="Copy↑", command=lambda: self._clear_and_write_entry(self.entry_position_copyright_check, f"{self.last_x} {self.last_y}"))

            #position_path
        self.label_position_path = tk.Label(self, text="Position path")
        self.entry_position_path = tk.Entry(self)
        self.button_copy_position_path = tk.Button(self, text="Copy↑", command=lambda: self._clear_and_write_entry(self.entry_position_path, f"{self.last_x} {self.last_y}"))

          #extra
            #apply button
        self.boton_aplicar = tk.Button(self, text="Aplicar", command=lambda :self._set_preferences(from_config=True))
        self.boton_aplicar.config(bg="blue", fg="white", font=("helvetica", 12, "bold"))

            #message tutorial configuration
        
        self.message_tutorial = tk.Message(self, text=self.msg_tutorial_config)

            #coordinates message
        self.message_coordinates = tk.Message(self, text="coords: ")
        self.message_coordinates.config(bg="black", fg="white", font=("helvetica", 12, "bold"))

        self.message_config_saved = tk.Message(self, text="Saved")
        self.message_config_saved.config(bg="green", fg="black", font=("helvetica", 12, "bold"))

          #insert actual values into entrys
        self.entry_wait_hashtag_interval.insert(0, self.WAIT_HASHTAG_INTERVAL)
        self.entry_wait_press_upload.insert(0, self.WAIT_PRESS_UPLOAD)
        self.entry_excel_path.insert(0, self.EXCEL_PATH)
        self.entry_videos_folder_path.insert(0, self.VIDEOS_FOLDER_PATH)
        # self.entry_position_upload_button.insert(0, self.POSITION_UPLOAD_BUTTON)
        self.entry_position_title.insert(0, self.POSITION_TITLE)
        self.entry_position_upload_file.insert(0, self.POSITION_UPLOAD_FILE)
        self.entry_position_publish.insert(0, self.POSITION_PUBLISH)
        self.entry_position_copyright_check.insert(0, self.POSITION_COPYRIGHT_CHECK)
        self.entry_position_path.insert(0, self.POSITION_PATH)

    #menu
    def _clear_screen(self):
        for widget in self.winfo_children():
            widget.pack_forget()

        self.unbind("<Return>")

    #menu
    def _home(self):
        self._clear_screen()
        self.boton_upload.pack()
        self.boton_publish.pack()
        self.boton_configurar.pack()

    #menu
    def _edit_preferences(self):
        self._clear_screen()

        self.boton_volver.pack()

        self.label_wait_hashtag_interval.pack()
        self.entry_wait_hashtag_interval.pack()

        self.label_wait_press_upload.pack()
        self.entry_wait_press_upload.pack()

        self.label_excel_path.pack()
        self.entry_excel_path.pack()

        self.label_videos_folder_path.pack()
        self.entry_videos_folder_path.pack()

        # self.label_position_upload_button.pack()
        # self.entry_position_upload_button.pack()
        # self.button_copy_position_upload_button.pack()

        self.label_position_title.pack()
        self.entry_position_title.pack()
        self.button_copy_position_title.pack()

        self.label_position_upload_file.pack()
        self.entry_position_upload_file.pack()
        self.button_copy_position_upload_file.pack()

        self.label_position_publish.pack()
        self.entry_position_publish.pack()
        self.button_copy_position_publish.pack()

        self.label_position_copyright_check.pack()
        self.entry_position_copyright_check.pack()
        self.button_copy_position_copyright_check.pack()

        self.label_position_path.pack()
        self.entry_position_path.pack()
        self.button_copy_position_path.pack()
        
        self.boton_aplicar.pack()

        self.message_tutorial.pack()

        self.message_coordinates.pack()


        #bind
        self.bind("<Return>", self._on_key_press)


    #keypress
    def _on_key_press(self, event):
        x, y = pg.position()
        self.message_coordinates.config(text=f"coords:\n{x}  {y}")
        self.last_x, self.last_y = x, y

    #config json
    def _read_preferences(self):
        if "preferences.json" not in os.listdir():
            print("No preferences file found. Creating one...")
            self._set_preferences()
            self._read_preferences()

        with open("preferences.json", "r") as f:
            self.preferencesJson = json.load(f)

        #delays
        self.WAIT_HASHTAG_INTERVAL = self.preferencesJson["WAIT_HASHTAG_INTERVAL"]
        self.WAIT_PRESS_UPLOAD = self.preferencesJson["WAIT_PRESS_UPLOAD"]

        #dirs
        self.EXCEL_PATH = self.preferencesJson["EXCEL_PATH"]
        self.VIDEOS_FOLDER_PATH = self.preferencesJson["VIDEOS_FOLDER_PATH"]

        # self.POSITION_UPLOAD_BUTTON = pg.Point(**self.preferencesJson["POSITION_UPLOAD_BUTTON"])
        self.POSITION_TITLE = pg.Point(**self.preferencesJson["POSITION_TITLE"])
        self.POSITION_UPLOAD_FILE = pg.Point(**self.preferencesJson["POSITION_UPLOAD_FILE"])
        self.POSITION_PUBLISH = pg.Point(**self.preferencesJson["POSITION_PUBLISH"])
        self.POSITION_COPYRIGHT_CHECK = pg.Point(**self.preferencesJson["POSITION_COPYRIGHT_CHECK"])
        self.POSITION_PATH = pg.Point(**self.preferencesJson["POSITION_PATH"])
        
    #config json
    def _set_preferences(self, from_config=False):
        if from_config:
            self.preferencesJson = {
                "WAIT_HASHTAG_INTERVAL": float(self.entry_wait_hashtag_interval.get()),
                "WAIT_PRESS_UPLOAD": int(self.entry_wait_press_upload.get()),
                "EXCEL_PATH": self.entry_excel_path.get(),
                "VIDEOS_FOLDER_PATH": self.entry_videos_folder_path.get(),
                # "POSITION_UPLOAD_BUTTON": dict(zip(["x", "y"], self.entry_position_upload_button.get().split(" "))),
                "POSITION_TITLE": dict(zip(["x", "y"], self.entry_position_title.get().split(" "))),
                "POSITION_UPLOAD_FILE": dict(zip(["x", "y"], self.entry_position_upload_file.get().split(" "))),
                "POSITION_PUBLISH": dict(zip(["x", "y"], self.entry_position_publish.get().split(" "))),
                "POSITION_COPYRIGHT_CHECK": dict(zip(["x", "y"], self.entry_position_copyright_check.get().split(" "))),
                "POSITION_PATH": dict(zip(["x", "y"], self.entry_position_path.get().split(" ")))
            }
            with open(self.jsonPath , "w") as f:
                json.dump(self.preferencesJson, f, indent=4)
            self._read_preferences()
            #message "saved"
            self._clear_screen()
            self.message_config_saved.pack()
            self.after(1000, self._home)
        else:
            #default preferences
            self.preferencesJson = {
                "WAIT_HASHTAG_INTERVAL": 0.5,
                "WAIT_PRESS_UPLOAD": 1,
                "EXCEL_PATH": "planner.xlsx",
                "VIDEOS_FOLDER_PATH": ".\\videos",
                # "POSITION_UPLOAD_BUTTON": {"x": 0, "y": 0},
                "POSITION_TITLE": {"x": 10, "y": 10},
                "POSITION_UPLOAD_FILE": {"x": 0, "y": 0},
                "POSITION_PUBLISH": {"x": 0, "y": 0},
                "POSITION_COPYRIGHT_CHECK": {"x": 0, "y": 0},
                "POSITION_PATH": {"x": 0, "y": 0},
            }

            with open("planner.xlsx", "w") as f:
                pandas.DataFrame(columns=["uploaded", "filename" , "title", "hashtags"]).to_excel(f, index=False)

            with open(self.jsonPath , "w") as f:
                json.dump(self.preferencesJson, f, indent=4)

            os.mkdir("videos")


    #tiktok functionality

    def copypaste(self, text):
        pyperclip.copy(text)
        pg.hotkey("ctrl", "v")

    def _get_excel(self):
        df = pandas.read_excel(self.EXCEL_PATH)
        return df
    
    def _find_next_vid(self):
        df = self._get_excel()
        for i in range(len(df)):
            if df["uploaded"][i] == 0:
                return df.loc[i]
        return None
    
    def _set_video_uploaded(self, object):
        df = self._get_excel()
        df.loc[object.name, "uploaded"] = 1
        df.to_excel(self.EXCEL_PATH, index=False)

    def _write_tags(self, tags):
        if type(tags) == str:
            tags = tags.split(" ")

        time.sleep(1)
        for t in tags:
            pg.write(t, interval=0.1)
            time.sleep(self.WAIT_HASHTAG_INTERVAL)
            pg.press("enter")
            pg.press("backspace")
    
    def _upload_video(self):
        self.next_vid = self._find_next_vid()
        pg.moveTo(self.POSITION_UPLOAD_FILE)
        pg.click()
        time.sleep(1)
        pg.moveTo(self.POSITION_PATH)
        self.copypaste(self.VIDEOS_FOLDER_PATH)
        pg.press("enter")
        pg.press("enter")
        self.copypaste(self.next_vid["filename"])
        pg.press("enter")
        time.sleep(1)
        pg.moveTo(self.POSITION_TITLE)
        pg.click()
        self.copypaste(self.next_vid["title"])
        pg.press("space")
        self._write_tags(self.next_vid["hashtags"])
        pg.moveTo(self.POSITION_COPYRIGHT_CHECK)
        pg.click()
    
    def _publish(self):
        pg.moveTo(self.POSITION_PUBLISH)
        pg.click()
        self._set_video_uploaded(self.next_vid)
    
    


if __name__ == "__main__":
    app = App()
    app.mainloop()