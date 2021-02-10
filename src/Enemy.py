from src.Covec import CoVec
from src.Deplacement import Deplacement
import pygame


class Enemy:
    def __init__(self, depla, sprit, tailleX, tailleY):
        self.sprite = pygame.image.load('images/' + sprit )
        self.image = pygame.Surface((tailleX, tailleY))
        self.rect = self.image.get_rect()
        self.rect.move_ip(depla.getDep().getX(), depla.getDep().getY())
        self.depla = depla
        self.alle = True

    def deplacementNormale(self, enemys):
        # mob pas immoblie
        if not self.depla.immobil():
            if self.alle and self.depla.presDeFin(self.rect.x, self.rect.y):
                # demitour et repositionnement à la fin
                self.alle = False
                self.rect.x = self.depla.getArri().getX()
                self.rect.y = self.depla.getArri().getY()
            if not self.alle and self.depla.presDeDep(self.rect.x, self.rect.y):
                # demitour et repositionnement au debut
                self.alle = True
                self.rect.x = self.depla.getDep().getX()
                self.rect.y = self.depla.getDep().getY()
            # déplacement en fonction de l'allée retour
            if self.alle:
                self.rect.move_ip(int(self.depla.getVit().getX()), int(self.depla.getVit().getY()))
            else:
                self.rect.move_ip(self.depla.getVit().getX()*-1, self.depla.getVit().getY()*-1)

    def getAlle(self):
        return self.alle

    # ne le prenez pas mal
    def getRect(self):
        return self.rect

    def getDepla(self):
        return self.depla


class Munition(Enemy):
    def __init__(self, depla, sprit, tailleX, tailleY):
        super().__init__(depla, sprit, tailleX, tailleY)

    def deplacementNormale(self, enemys):
        if self.depla.presDeFin(self.rect.x, self.rect.y):
            enemys.remove(self)
        else:
            self.rect.move_ip(int(self.depla.getVit().getX()), int(self.depla.getVit().getY()))


class Lanceur(Enemy):
    def __init__(self, depla, sprit, tailleX, tailleY, spritMun, tailleXMun, tailleYMun, distTire, frequence):
        super().__init__(depla, sprit, tailleX, tailleY)
        self.spritMun = spritMun
        self.tailleXMun = tailleXMun
        self.tailleYMun = tailleYMun
        self.distTire = distTire
        self.frequence = frequence
        self.cpt = 0

    def tirer(self,enemys):
        # calcul de la diréction du projectil en fonction de la direction
        temp = self.distTire % self.frequence
        temp = (self.distTire - temp) // self.frequence
        # mob et balle part de droite et vas à guauche
        if (super().getAlle() and super().getDepla().getVit().getX() < 0) or \
                (not super().getAlle() and super().getDepla().getVit().getX() > 0) or super().getDepla().immobil():
            enemys.append(
                Munition(Deplacement(CoVec(super().getRect().x, super().getRect().y),
                                     CoVec(super().getRect().x - self.distTire, super().getRect().y),
                                     CoVec(temp*-1, 0)),
                         self.spritMun, self.tailleXMun, self.tailleYMun))
        else:
        # mob et balle part de droite et vas à guauche
            enemys.append(
                Munition(Deplacement(CoVec(super().getRect().x, super().getRect().y),
                                     CoVec(super().getRect().x + self.distTire, super().getRect().y),
                                     CoVec(temp, 0)),
                         self.spritMun, self.tailleXMun, self.tailleYMun))

    def deplacementNormale(self, enemys):
        super().deplacementNormale(enemys)
        # cpt compteur pour tiré à frequence
        if self.cpt < self.frequence:
            self.cpt += 1
        else:
            self.tirer(enemys)
            self.cpt = 0


