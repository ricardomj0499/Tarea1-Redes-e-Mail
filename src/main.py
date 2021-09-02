print("inicio main")
import sys
import os

# Obtener las entradas de la terminal
# ej:  python test.py arg1 arg2 arg3

#print('Number of Arguments: ', len(sys.argv))
#print('A: ', str(sys.argv))

print("mid main")

os.system("twistd -ny smtpclient-1.tac 'a'")

print("final main")


