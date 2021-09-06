from email import charset, message
import sys

from email.mime.text import MIMEText
import tkinter

from twisted.internet import reactor
from twisted.mail.smtp import sendmail
from twisted.python import log

# log.startLogging(sys.stdout)

import csv

from tkinter import *
from tkinter import filedialog

host = ''
csv_file = ''
msg = ''

def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    print(filename)



def save_info():
  global host      
  global csv_file
  global msg
  host = host1.get()
  csv_file = csv_file1.get()
  msg = mensaje1.get()
  screen.destroy()


if __name__ == "__main__":
    #
    # Desde GUI
    # 

    screen = Tk() # creación ventana
    screen.geometry("400x400") # forma ventana
    screen.title("Enviar Correo")
    heading = Label(text = "Por favor Ingrese los datos de su correo", bg = "grey", fg = "black", width = "500", height = "3    ")
    heading.pack()

    '''
    Campos Para el Host
    '''
    host_text = Label(text = "Ingrese el Email Server",) # El texto que indica
    host_text.place(x = 15, y = 70)
    host1 = StringVar() # Donde se va a escribir
    host_entry = Entry(textvariable = host1, width = "30")
    host_entry.place(x = 15, y = 100)

    '''
    Campos Para los receptores
    '''
    recipientes_text = Label(text = "Ingrese nombre de archivo con receptores",)
    recipientes_text.place(x = 15, y = 140)
    csv_file1 = StringVar() # Donde se va a escribir
    csv_file_entry = Entry(textvariable = csv_file1, width = "30")
    csv_file_entry.place(x = 15, y = 180)

    '''
    Campos Para el Mensaje
    '''
    mensaje_text = Label(text = "Mensaje * ",)
    mensaje_text.place(x = 15, y = 210)
    mensaje1 = StringVar()
    mensaje_entry = Entry(textvariable = mensaje1, width = "30")
    mensaje_entry.place(x = 15, y = 240)
        
    '''
    Campos Para el Boton de enviar
    '''
    send = Button(screen,text = "Envíar", width = "30", height = "2", command = save_info, bg = "grey")
    send.place(x = 15, y = 290)

    '''
    Main Lopp
    '''
    screen.mainloop()

    listRecipientes = []  
    with open(csv_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            print(row[0])
            listRecipientes.append(row[0])
        print(listRecipientes)


    host = host # 
    sender = "testEmisor1@localhost" # 

    msg = MIMEText(msg)
    msg["Subject"] = "Correo de prueba numero 435"
    msg["From"] = sender
    msg["To"] = ", ".join(listRecipientes)

    deferred = sendmail(host, sender, listRecipientes, msg, port=1234)
    deferred.addBoth(lambda result: reactor.stop())

    reactor.run()
