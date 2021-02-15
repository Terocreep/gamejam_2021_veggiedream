import json
# passer pas Score
class Storage:
    def __init__(self, nom):
        self.nom = nom
        self.nom_fichier = "score.json"
        with open(self.nom_fichier, 'r') as fichier:
            self.liste_score = json.load(fichier)

    def maj_info(self):
        with open(self.nom_fichier, 'r') as fichier:
            self.liste_score = json.load(fichier)

    # private
    def ordre(self, newData):
        nouvelList = []
        asRecopi = False
        for ligne in self.liste_score.get("rank"):
            if newData.get("score") >= ligne.get("score"):
                if not asRecopi:
                    nouvelList.append(newData)
                    asRecopi = True
            nouvelList.append(ligne)
        if not asRecopi:
            nouvelList.append(newData)
        self.liste_score = {"rank": nouvelList}

    def ecrire_info(self, score):
        newData = {"nom": self.nom, "score": score}
        #met le nouveau score dans la liste ordonée de self.liste_score
        self.ordre(newData)
        with open(self.nom_fichier, 'w') as fichier:
            json.dump(self.liste_score, fichier)
        self.maj_info()

    def getClassemnt(self):
        return self.liste_score.get("rank")


class Score:
    def __init__(self, pseudo):
        self.score = 0
        self.listVariation = []
        self.listVariation.append({"nom": "rien", "score": 0})
        self.storage = Storage(pseudo)

    def newVar(self, nom, score):
        for var in self.listVariation:
            if var.get("nom") == nom:
                print("encienne variation de score:" + var.get("nom") + " => " + var.get("score") + ", remplacé ")
                self.listVariation.remove(var)
        self.listVariation.append({"nom": nom, "score": score})

    def execVar(self, nom):
        estDans = False
        for var in self.listVariation:
            if var.get("nom") == nom:
                estDans = True
                self.score += var.get("score")
        if not estDans:
            print("la variation " + nom + " n'éxiste pas")

    def finPartie(self):
        self.storage.ecrire_info(self.score)

    def getScore(self):
        return self.score

    def getClassement(self):
        return self.storage.getClassemnt()
