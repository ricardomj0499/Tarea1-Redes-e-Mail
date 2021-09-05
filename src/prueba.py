print("inicio prueba")
import sys

print('Number of Arguments: ', len(sys.argv))

try:
    d = sys.argv.index('-d')
    s = sys.argv.index('-s')
    p = sys.argv.index('-p')

    dominios = sys.argv[d+1]
    mailStorage = sys.argv[s+1]
    port = sys.argv[p+1]
except NameError as e:
    print(e)

