#imports
from tkinter import *
from tkinter import filedialog
from cryptography.fernet import Fernet


#WHEN TESTING:
#If you opened the tkinter(gui) app and want to test again
#Close the app gui first before running
#the tkinter(gui) will not open if the program is already running in the background

#global var for key used for its paired file
key_pair = ""


#FUNCTIONS

def specific_key():
    global key_pair
    filename = filedialog.askopenfilename(title = "Open Text File",filetypes = [('Text Files', '*.txt')])
    fileread = open(filename,'rt')    
    fileread.close()

    key_pair = filename.split('/')[-1]

    if "Key" not in key_pair:
        #"Not a key" MESSAGE POPUP
        not_key = Tk()

        not_key.title("NOT A KEY")
        screen_width = not_key.winfo_screenwidth()
        screen_height = not_key.winfo_screenheight()
        msg_width = 200
        msg_height = 50
        x = (screen_width/2) - (msg_width/2)
        y = (screen_height/2) - (msg_height/2)
        not_key.geometry("{}x{}+{}+{}".format(msg_width,msg_height,int(x),int(y)))
        success = Label(not_key, text = "This file is not a key!")
        success.pack()

        not_key.mainloop()
    else:
        decryption_button.config(state='normal')
    


#Can only Encrypt text files
def file_encrypt():
    #Opens File Explorer
    filename = filedialog.askopenfilename(title = "Open Text File",filetypes = [('Text Files', '*.txt')])
    fileread = open(filename,'rt')    
    fileread.close()


    key = Fernet.generate_key()
    #Names the key relative to the name of file encrypted
    key_name = filename.split('/')[-1]
    #Check key name
    print(key_name)

    with open(f'Key to [{key_name}].txt', 'wb') as filekey:
        filekey.write(key)

    with open(f'Key to [{key_name}].txt', 'rb') as filekey:
        key = filekey.read()

    fernet = Fernet(key)

    with open(filename, 'rb') as file:
        original = file.read()
        encrypted = fernet.encrypt(original)

    with open(filename, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    
    #Encryption Success Popup
    en_success = Tk()

    en_success.title("Sucess!")
    screen_width = en_success.winfo_screenwidth()
    screen_height = en_success.winfo_screenheight()
    msg_width = 200
    msg_height = 50
    x = (screen_width/2) - (msg_width/2)
    y = (screen_height/2) - (msg_height/2)
    en_success.geometry("{}x{}+{}+{}".format(msg_width,msg_height,int(x),int(y)))
    success = Label(en_success, text = "Encryption Sucess")
    success.pack()

    en_success.mainloop()


#Can only Decrypt text files
#If the key and the file match it will decrypt may give useful message
def file_decrypt():
    #Opens File Explorer
    filename = filedialog.askopenfilename(title = "Open Text File",filetypes = [('Text Files', '*.txt')])
    fileread = open(filename,'rt')    
    fileread.close()

    # Load the previously generated key from 'filekey.key'
    with open(key_pair, 'rb') as filekey:
        key = filekey.read()

    # Initialize a Fernet object with the key
    fernet = Fernet(key)

    # Read the encrypted file
    with open(filename, 'rb') as enc_file:
        encrypted = enc_file.read()

    # Decrypt the data
    decrypted = fernet.decrypt(encrypted)

    # Write the decrypted data to a new file
    with open(filename, 'wb') as dec_file:
        dec_file.write(decrypted)

    #Decryption Success message popup
    de_success = Tk()

    de_success.title("Sucess!")
    screen_width = de_success.winfo_screenwidth()
    screen_height = de_success.winfo_screenheight()
    msg_width = 200
    msg_height = 50
    x = (screen_width/2) - (msg_width/2)
    y = (screen_height/2) - (msg_height/2)
    de_success.geometry("{}x{}+{}+{}".format(msg_width,msg_height,int(x),int(y)))
    success = Label(de_success, text = "Decryption Sucess")
    success.pack()

    de_success.mainloop()




#start of the app
app = Tk()
app.title("EnDe")

#this block of code makes the app always centered in screen when opened
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
app_width = 500
app_height = 500
x = (screen_width/2) - (app_width/2)
y = (screen_height/2) - (app_height/2)
app.geometry("{}x{}+{}+{}".format(app_width,app_height,int(x),int(y)))


#GUI section

#canvas for encryption
canvas_en = Canvas(app, width=498, height=248, highlightthickness=1, highlightbackground="red")
canvas_en.place(x=0, y=0)

encryption_label = Label(app, text="Encryption Section")
encryption_label.config(font=("Helvetica", 20))
encryption_label.place(x=10,y=10)

encryption_button = Button(app, text="Encrypt", fg="white", bg="gray", width=7,command=file_encrypt)
encryption_button.place(x=50, y=100)

label1 = Label(text = "Open a text file to encrypt")
label1.place(x=50,y=125)

# Add widgets to the Canvas
canvas_en.create_window(120, 20, window=encryption_label)
canvas_en.create_window(50, 200, window=encryption_button)
canvas_en.create_window(90, 230, window=label1)

#canvas for decryption
canvas_de = Canvas(app, width=498, height=248, highlightthickness=1, highlightbackground="green")
canvas_de.place(x=0, y=252)

decryption_label = Label(app, text="Decryption Section")
decryption_label.config(font=("Helvetica", 20))
decryption_label.place(x=10,y=10)

key_button = Button(app, text="Key", fg="white", bg="gray", width=7,command=specific_key)
key_button.place(x=50, y=150)

key_button_label = Label(text = "Upload the key first before decrypting")
key_button_label.config(fg='red')
key_button_label.place(x=50,y=100)

decryption_button = Button(app, text="Decrypt", fg="white", bg="gray", width=7,command=file_decrypt , state='disabled')
decryption_button.place(x=50, y=100)

label2 = Label(text = "Open a text file to Decrypt")
label2.place(x=50,y=125)



# Add widgets to the Canvas
canvas_de.create_window(120, 20, window=decryption_label)
canvas_de.create_window(50, 150, window=key_button)
canvas_de.create_window(120, 170, window=key_button_label)
canvas_de.create_window(50, 200, window=decryption_button)
canvas_de.create_window(90, 230, window=label2)

app.mainloop()