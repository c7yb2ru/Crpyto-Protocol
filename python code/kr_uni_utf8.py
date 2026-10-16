import tkinter as tk
from tkinter import messagebox


def korean_to_unicode():
    input_txt = entry.get()
    try:
        unicode_txt = ' '.join(f"U+{ord(char):04X}" for char in input_txt)
        result_label.config(text="UTF-8: " + unicode_txt)
    except Exception as e:
        messagebox.showerror('Error', str(e))

def unicode_to_korean():
    input_txt = entry.get()
    try:
        # 입력된 텍스트를 공백으로 분리하여 각 유니코드 코드 포인트를 얻습니다
        unicode_chars = input_txt.split()
        # 각 유니코드 코드 포인트를 문자로 변환합니다
        korean_txt = ''.join(chr(int(char[2:], 16)) for char in unicode_chars if char.startswith("U+"))
        result_label.config(text="Korean: " + korean_txt)
    except Exception as e:
        messagebox.showerror('Error', str(e))

window = tk.Tk()
window.title('한글 <-> 유니코드')

input_label = tk.Label(window, text='한글 또는 유니코드 입력')
input_label.pack()
entry = tk.Entry(window, width=50)
entry.pack()

convert_to_unicode_button = tk.Button(window, text='한글 -> 유니코드', command=korean_to_unicode)
convert_to_unicode_button.pack()

convert_to_korean_button = tk.Button(window, text='유니코드 -> 한글', command=unicode_to_korean)
convert_to_korean_button.pack()

result_label = tk.Label(window, text='')
result_label.pack()

window.mainloop()


#유니코드로 인코딩된 암호문을 디코딩 
#3바이트 값으로 출력후 디코딩 