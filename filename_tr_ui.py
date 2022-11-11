import asyncio
import glob
import ntpath
import os
import random
import shutil
import sys
import tkinter as tk
import time
from tkinter import filedialog

import mtranslate as mtranslate
from tqdm import tqdm

total = 0
err = 0
translator = mtranslate





def rename(path):
    path = path + "\\"
    label4.config(text="Progress :")
    files = glob.glob(path + "*")
    i = 0
    for file in tqdm(files):
        total_files = len(files)
        if isEnglish(file):
            print(file)
        else:
            i = i + 1
            label4.config(text=f"Progress : {i}/{total_files}")
            old_name = file
            try:
                file_base = ntpath.basename(file)
                file_arr = os.path.splitext(file_base)
                file_name = file_arr[0]
                file_ext = file_arr[1]
                temp = file_name
                file_name = file_name.replace('[', '(')
                file_name = file_name.replace(']', ')')
                try:
                    translated = translator.translate(file_name)
                except:
                    time.sleep(3)
                    print('error occured.trying again')
                    try:
                        if (random.randint(1, 20) == 10):
                            time.sleep(0.3)
                        translated = translator.translate(file_name)
                    except:
                        time.sleep(5)
                        translated = translator.translate(file_name)
                translated = translated.replace(':', '-')
                translated = translated.replace('/', '-')
                new_name = ntpath.dirname(file) + "\\" + translated
                new_name = new_name + "__" + temp + file_ext
            except:
                print("Translating error")
                global err
                err += 1
                sys.stdout.flush()
                i = i - 1
                pass
                continue
            try:
                # print(str(i)+"  :renaming " + str(old_name) + " to " + str(new_name))
                new_name = new_name.replace('"', '')
                new_name = new_name.replace('?', '7')
                sys.stdout.flush()
            except:
                try:
                    # print("renaming XXX to " + str(new_name))
                    sys.stdout.flush()
                except:
                    print("renaming XXX to YYY")
                    sys.stdout.flush()
                    pass
            try:
                shutil.move(old_name, new_name)
            except:
                time.sleep(.1)
                try:
                    shutil.move(old_name, new_name)
                except:
                    print('\n\terror renaming to ' + new_name)
            time.sleep(.300)

    global total
    total += i
    label4.config(text="Completed!!!")
    print(str(i) + " files translated")

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global var, dir
    filename = filedialog.askdirectory()
    var.set(filename)
    dir = filename
    print(filename)

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def translate():
    dir = entry1.get()
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, rename, dir)
    # rename(path=dir)


root = tk.Tk()
var = tk.StringVar()
canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Filename Translator')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Type your Directory * :')
label2.config(font=('helvetica', 10))
canvas1.create_window(80, 50, window=label2)

button2 = tk.Button(text="Browse", command=browse_button)
canvas1.create_window(300, 50, window=button2)

entry1 = tk.Entry(root, width=60, textvariable=var)
canvas1.create_window(200, 70, window=entry1)

label4 = tk.Label(root, text='')
label4.config(font=('helvetica', 10))

canvas1.create_window(70, 130, window=label4)


button1 = tk.Button(text='Start', command=translate, bg='brown', fg='white',
                    font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 200, window=button1)

root.mainloop()
