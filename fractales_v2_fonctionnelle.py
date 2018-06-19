# encoding=utf-8

import math
import struct
import array

tabDuree = []
tabHauteur = []
premiere_fois = True

def premiere_fois_methode():
     premiere_fois = False
     return premiere_fois

def musique(A, B, niveau, niveauMax):
# Genere recursivement les coordonnees des points

     if premiere_fois:
          if niveau == niveauMax:
               # raise ValueError("Attention! Le niveau est egal a niveauMax")
               print ("Attention! Le niveau est egal a niveauMax")
               input("Continue?")
               premiere_fois_methode()


     if niveau == niveauMax:    # Condition initiale
        duree = (B[0] - A[0])   # Distance sur l'axe des x entre A et B
        hauteur = A[1]          # Hauteur du point A

        tabDuree.append(math.trunc(duree))
        tabHauteur.append(math.trunc(hauteur))
        return

     else:
        h = math.trunc(48/(2**niveau))
        
        # Trouver C
        C = (A[0] + (B[0]-A[0])/2, A[1] + (B[1]-A[1])/2 + h)
       
        # Trouver D, E
        D = (A[0] + (B[0]-A[0])/3, A[1] + (B[1]-A[1])/3)
        E = (B[0] - (B[0]-A[0])/3, B[1] - (B[1]-A[1])/3)

        # Appels recursifs
        musique(A, D, niveau+1, niveauMax)
        musique(D, C, niveau+1, niveauMax)
        musique(C, E, niveau+1, niveauMax)
        musique(E, B, niveau+1, niveauMax)
 

def genererMIDI():
# Ecrit le fichier MIDI a partir des tableaux tabDuree et tabHauteur
     
     # Proprietes du fichier MIDI
     volume = 0x60
     dureeCroche = 128
     typeMIDI = 0
     tracks = 1
     
     fichier = open('musique.mdi', 'w+b')
     
     # Initialisation du buffer
          
     # Calculer le nombre maximum de bytes requis pour le timestamp
     dureeMax = max(tabDuree)
     nbBytes = math.trunc(math.ceil(math.log(128, dureeMax) + 1))
          
     # Allouer 4 bytes par note pour jouer, nbBytes+3 bytes par note pour arrêter, 
     # 22 espaces pour les headers et 4 pour le track out
     buff = array.array('B', [0] * ((4+nbBytes+3) * len(tabDuree) + 26))
     
     # MIDI Header
     struct.pack_into('>4BI3H', buff, 0, 0x4D, 0x54, 0x68, 0x64, 0x06, typeMIDI, tracks, dureeCroche)

     # Track Header
     struct.pack_into('4B', buff, 14, 0x4D, 0x54, 0x72, 0x6B)

     index = 22    # Garde la position du dernier chiffre mis dans le buffer

     # Track Data
     for i in range(len(tabDuree)):
     
          # Jouer la note
          struct.pack_into('4B', buff, index, 0, 0x90, tabHauteur[i], volume)
          index += 4
          
          # Timestamp: Inserer bytes supplementaires si duree > 128
          if tabDuree[i] >= 128:
               timestamp = convTimestamp(tabDuree[i])
               for j in range(len(timestamp)):
                   struct.pack_into('B', buff, index, timestamp[j])
                   index += 1

          # Arreter la note apres la duree donnee
          struct.pack_into('4B', buff, index, tabDuree[i]%128, 0x80, tabHauteur[i], volume)
          index += 4

     # Track Out 
     struct.pack_into('4B', buff, index, 0x00, 0xFF, 0x2F, 0x00)
     index += 4
     
     # Inscrire la longueur reelle du track data + track out dans le header (position 18)
     struct.pack_into('>I', buff, 18, index-22)

     # Ecrire le fichier
     fichier.write(buff)
     # Fermer le fichier
     fichier.close()
     
def convTimestamp(duree):
# Genere recursivment une liste avec les bytes supplementaires requis pour exprimer la duree > 128
    bytes = []
   
    if 1 <= duree//128 < 128:   # Condition initiale
        bytes.append(0x80+duree//128)
        return bytes
    
    elif duree//128 >=128:      # recursion
        convtimestamp(duree//128)
        bytes.append(0x80+(duree//128)%128)
        
    return bytes

def main():
# Fonction principale
     musique((0,0x24), (77760,0x24), 0, 5)

     # musique((0,0x24), (77760,0x24), 0, 0)
     genererMIDI();

main();
          
