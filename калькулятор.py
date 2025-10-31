import time

import customtkinter
import webbrowser
from PIL import Image
import json

version = '1.1'

win = customtkinter.CTk()
win.title('калькулятор с переменными. '+version)
win.iconbitmap("data/icon.ico")
win.geometry('800x500')
win_x, win_y = win.geometry().split('+')[0].split('x')

FORBIDDEN_NAMES = ['False', 'None', 'True', 'and', 'or', 'not', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']

import math

# Словарь для передачи в eval()
MATH_FUNCTIONS = {
    # Тригонометрические функции
    'sin': math.sin,         # Синус
    'cos': math.cos,         # Косинус
    'tan': math.tan,         # Тангенс
    'asin': math.asin,       # Арксинус
    'acos': math.acos,       # Арккосинус
    'atan': math.atan,       # Арктангенс

    # Гиперболические функции (для инженерии и физики)
    'sinh': math.sinh,
    'cosh': math.cosh,
    'tanh': math.tanh,

    # Логарифмы и экспонента
    'log': math.log,         # Натуральный логарифм (log(x))
    'log10': math.log10,     # Логарифм по основанию 10
    'exp': math.exp,         # Экспонента (e в степени x)
    'pow': math.pow,         # Возведение в степень (pow(x, y) = x**y)

    # Дополнительные функции и константы
    'sqrt': math.sqrt,       # Квадратный корень
    'pi': math.pi,           # Константа Пи (3.14159...)
    'e': math.e,             # Константа Эйлера (2.71828...)
    'abs': abs,              # Абсолютное значение (из встроенных функций)
    'round': round,          # Округление (из встроенных функций)
}

histore_image = customtkinter.CTkImage(Image.open('data/histore.png'), Image.open('data/histore.png'), size=(40, 40))
save_image = customtkinter.CTkImage(Image.open('data/save.png'), Image.open('data/save.png'), size=(40, 40))

ran = True
def update():
    win_x, win_y = map(int, win.geometry().split('+')[0].split('x'))

    try:
        d = dict()
        try:
            for i in text_box_ctk.get('1.0', 'end-1c').split('\n'):
                d[i.split('=')[0]] = eval(i.split('=')[1], {'__builtins__': None}, d)

            di = d.items()
            ds = ''
            for k, v in di:
                ds += f'{k}={v}  '
            dict_Label_ctk.configure(text=ds)
        except: pass

        # --- ПРОВЕРКА ЗАПРЕЩЕННЫХ ИМЕН ---
        for k in d:
            if k in FORBIDDEN_NAMES:
                raise ValueError(f"'{k}' является зарезервированным словом.")
        # for k in FORBIDDEN_NAMES:
        #     if k in entry_ctk.get():
        #         raise ValueError(f"'{k}' является зарезервированным словом.")

        d.update(MATH_FUNCTIONS)
        answer_Label_ctk.configure(text='= ' + str(round(eval(entry_ctk.get(), {'__builtins__': None}, d), 15)))
    except Exception as e: answer_Label_ctk.configure(text='Error: ' + str(e))

    entry_ctk.configure(width=win_x-20-50)
    text_box_ctk.configure(width=win_x//2-20, height=win_y-120); text_box_ctk.place(x=win_x//2+10, y=150)
    histore_text_box_ctk.configure(width=win_x//2-10, height=win_y-120); histore_text_box_ctk.place(x=10, y=150)
    help_button_ctk.place(x=win_x - 40, y=win_y - 40)
    histore_button_ctk.place(x=win_x - 50, y=10)
    save_button_ctk.place(x=win_x - 50, y=60)

    win.after(100, update)


def on_enter(a):
    if not 'Error' in answer_Label_ctk._text:
        histore_text_box_ctk.insert('0.0', entry_ctk.get() + ' '  + answer_Label_ctk._text + '\n')
        entry_ctk.delete('0', 'end')
        entry_ctk.insert('0', answer_Label_ctk._text[2::])

histor_count = 0

def on_up(a):
    global histor_count
    t = histore_text_box_ctk.get('1.0', 'end-1c').split('\n')
    if histor_count > 1:
        histor_count -= 1
        entry_ctk.delete('0', 'end')
        entry_ctk.insert('0', t[histor_count-1].split(' =')[0])

def on_down(a):
    global histor_count
    t = histore_text_box_ctk.get('1.0', 'end-1c').split('\n')
    if histor_count < len(t):
        histor_count += 1
        entry_ctk.delete('0', 'end')
        entry_ctk.insert('0', t[histor_count-1].split(' =')[0])

def on_any_key(a):
    global histor_count
    if a.char != '': histor_count=0

def open_histore():
    global histore_CTkOptionMenu, frame_histore
    win_x, win_y = map(int, win.geometry().split('+')[0].split('x'))
    try:
        with open('data/histore.json', 'r', encoding='utf-8') as file:
            histore_dict = dict(json.load(file))
    except:
        with open('data/histore.json', 'w', encoding='utf-8') as file:
            json.dump(dict(), file)
            histore_dict = dict()
    frame_histore = customtkinter.CTkFrame(win, 300, win_x)
    frame_histore.pack(side='right'); frame_histore.pack_propagate(False)
    histore_CTkOptionMenu = customtkinter.CTkOptionMenu(frame_histore, values=list(histore_dict.keys()), command=lambda v: open_histore2(v, histore_dict))
    histore_CTkOptionMenu.pack(pady=10)

def open_histore2(v, histore_dict):
    data = histore_dict[v]
    entry_ctk.delete(0, customtkinter.END)
    entry_ctk.insert(0, data['e'])
    text_box_ctk.delete("1.0", "end")
    text_box_ctk.insert("1.0", data['b'])
    frame_histore.destroy()

def save_in_histore():
    # {"31.10.2025":{e:'', b:''} }
    new = {str(entry_ctk.get()):{'e':entry_ctk.get(), 'b':text_box_ctk.get('0.0', 'end')}}
    try:
        with open('data/histore.json', 'r', encoding='utf-8') as file:
            histore_dict = dict(json.load(file))
            histore_dict.update(new)
    except: histore_dict = new

    with open('data/histore.json', 'w', encoding='utf-8') as file:
        json.dump(histore_dict, file, indent=4, ensure_ascii=False) # ensure_ascii=False

entry_ctk = customtkinter.CTkEntry(win, width=780, height=50, font=(None, 30)); entry_ctk.place(x=10, y=10)
entry_ctk.bind("<Return>", on_enter); entry_ctk.bind('<Up>', on_up); entry_ctk.bind('<Down>', on_down); entry_ctk.bind('<Key>', on_any_key)
answer_Label_ctk = customtkinter.CTkLabel(win, font=(None, 30)); answer_Label_ctk.place(x=10, y=70)
dict_Label_ctk = customtkinter.CTkLabel(win, font=(None, 30)); dict_Label_ctk.place(x=10, y=110)
text_box_ctk = customtkinter.CTkTextbox(win, 380, 380, font=(None, 30)); text_box_ctk.place(x=400, y=150)
histore_text_box_ctk = customtkinter.CTkTextbox(win, 380, 380, font=(None, 30)); histore_text_box_ctk.place(x=0, y=150)
help_button_ctk = customtkinter.CTkButton(win, 40, 40, font=(None, 30), text='?', command=lambda: webbrowser.open("https://drive.google.com/drive/folders/14-Rg0btuw20MMrWbaBTAtgdaoYBpsaMm?usp=sharing"))
histore_button_ctk = customtkinter.CTkButton(win, 1, 1, text='', image=histore_image, command=open_histore, fg_color='#dddddd')
save_button_ctk = customtkinter.CTkButton(win, 1, 1, text='', image=save_image, command=save_in_histore, fg_color='#dddddd')

update()

win.mainloop()

