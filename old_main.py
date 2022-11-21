import pyautogui as pg
import time
import pandas
import pyperclip
import tkinter as tk

EXCEL_NAME = "planner.xlsx"
POSITION_UPLOAD_BUTTON = pg.Point(x=1682, y=56)
POSITION_TITLE = pg.Point(x=985, y=269)
POSITION_UPLOAD_FILE = pg.Point(x=584, y=483)
POSITION_PUBLISH = pg.Point(x=1059, y=889)
POSITION_COPYRIGHT_CHECK = pg.Point(x=1093, y=726)
POSITION_PATH = pg.Point(x=325, y=47)
WAIT_PRESS_UPLOAD = 5
WAIT_HASHTAG_INTERVAL = 1.5
VIDEOS_FOLDER_PATH = r"H:\dospiesunamochila\videos"
   
def get_excel():
    df = pandas.read_excel(EXCEL_NAME)
    return df


def find_next_vids():
    df = get_excel()
    for i in range(len(df)):
        if df["uploaded"][i] == 0:
            return [df.loc[x] for x in range(i, i+4)]
    return None


def set_video_uploaded(objects=None):
    df = get_excel()
    
    for v in objects:
        df.loc[v.name, "uploaded"] = 1
    
    df.to_excel(EXCEL_NAME, index=False)


def write_tags(tags):
    if type(tags) == str:
        tags = tags.split(" ")

    time.sleep(1)
    for t in tags:
        pg.write(t, interval=0.1)
        time.sleep(WAIT_HASHTAG_INTERVAL)
        pg.press("enter")
        pg.press("backspace")


def copypaste(text):
    pyperclip.copy(text)
    pg.hotkey("ctrl", "v")


def upload():
    global next_vids
    next_vids = find_next_vids()
    # pg.moveTo(POSITION_UPLOAD_BUTTON)
    # pg.click()
    # time.sleep(WAIT_PRESS_UPLOAD)
    pg.moveTo(POSITION_UPLOAD_FILE)
    pg.click()
    time.sleep(1)
    pg.moveTo(POSITION_PATH)
    copypaste(VIDEOS_FOLDER_PATH)
    pg.press("enter")
    pg.press("enter")
    copypaste(next_vids["path"])
    pg.press("enter")
    time.sleep(1)
    pg.moveTo(POSITION_TITLE)
    pg.click()
    copypaste(next_vids["title"])
    pg.press("space")
    write_tags(next_vids["hashtags"])
    pg.moveTo(POSITION_COPYRIGHT_CHECK)
    pg.click()


def publish():
    global next_vids
    pg.moveTo(POSITION_PUBLISH)
    pg.click()
    set_video_uploaded(next_vids)


######
def run():
    upload()
    publish()

if __name__ == "__main__":
    next_vids = find_next_vids()
    set_video_uploaded(next_vids)