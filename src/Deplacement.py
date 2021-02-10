class Deplacement:
    # dep, arri, vit sont des CoVec
    def __init__(self, dep, arri, vit):
        self.dep = dep
        self.arri = arri
        self.vit = vit

    def getDep(self):
        return self.dep

    def getArri(self):
        return self.arri

    def getVit(self):
        return self.vit

    def immobil(self):
        return self.vit.getX() == 0 and self.vit.getY() == 0

    def presDeFin(self, x, y):
        return (0 <= abs(x - self.arri.getX()) <= abs(self.vit.getX())) and (
                    0 <= abs(y - self.arri.getY()) <= abs(self.vit.getY()))

    def presDeDep(self, x, y):
        return ( 0 <= abs(x - self.dep.getX()) <= abs(self.vit.getX()) ) and ( 0 <= abs(y - self.dep.getY()) <= abs(self.vit.getY()) )
