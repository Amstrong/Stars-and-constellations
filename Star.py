class Star(object):
    """description of class"""
    def __init__(self,x,y,z,nHD,brillo,nHR,nombres):
        super().__init__()
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.nHD = int(nHD)
        self.brillo = float(brillo)
        self.nHR = int(nHR)
        self.nombres = nombres
    
    def getX(self, size):
        n = (size*0.9)
        return int((self.x+1)*(n/2))+int(size*0.05)

    def getY(self, size):
        n = (size*0.9)
        return int((1-self.y)*(n/2))+int(size*0.05)

"""for key in costelaciones:
    print(key, ":", costelaciones[key])
    print()

print(costelaciones.get(str('Casiopea').casefold()))
for star in stars:
    print('(',star.getX(n),',',star.getY(n),') nombres:',star.nombres)"""