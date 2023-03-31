import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                text_area.insert(tk.END, message + '\n')
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    message = f"{nickname}: {input_field.get()}"
    client.send(message.encode('ascii'))
    input_field.delete(0, tk.END)

def on_close():
    client.close()
    window.quit()

window = tk.Tk()
window.title("Chat App")

text_area = scrolledtext.ScrolledText(window)
text_area.configure(state='disabled')
text_area.pack()

input_field = tk.Entry(window)
input_field.pack()
input_field.bind('<Return>', lambda event: write())

send_button = tk.Button(window, text="Send", command=write)
send_button.pack()

window.protocol("WM_DELETE_WINDOW", on_close)

receive_thread = threading.Thread(target=receive)
receive_thread.start()

window.mainloop()