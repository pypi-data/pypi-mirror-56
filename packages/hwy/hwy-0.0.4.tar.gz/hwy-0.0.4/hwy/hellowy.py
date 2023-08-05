 
import sys
def balaba():
    if len(sys.argv) > 2:
        name = sys.argv
    elif len(sys.argv)==2:
        name = sys.argv[1]
    elif len(sys.argv)==1:
        name = 'wy'


    print("hello {}!".format(name))

 