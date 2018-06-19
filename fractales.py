"""
encoding=utf-8
TP01; IFT2015; musique fonction; MIDI; Koch
"""

import math
import struct
import array

# f: le fichier texte
f = open("fractalOutput.txt", "w")
# fb: le fichier binaire
fb = open("fractalOutputBinary.txt", "w+b")
# note = []

f.write("Header\n")

def musique(A, B, niveau, niveauMax):

    if niveau == niveauMax:
        duree = B[0] - A[0]
        dureeB = bytes(duree)
        hauteur = A[1]
        hauteurB = bytes(hauteur)
        """
        MIDI: 7F 90 3E 60 means: first wait 7F time units, 
        and then play on channel 0 - the musical note C at volume 60
        
        MIDI header:
        4D 54 68 64 00 00 00 06 00 01 00 01 00 80 4D 54 72 6B 00 00 00 0A
        MIDI end:
        00 FF 2F 00
        """
        note = (duree, 144, hauteur, 96)
        print (note)
        
        buff = array.array("B", range(40))
        struct.pack_into("4B", buff, 0, duree, 0x90, hauteur, 0x60)
        fb.write(buff)
        
        f.write(str(note) + "\n")
        
        # print(A, B)
        # return note
                
    else:
        dist = B[0] - A[0]
        h = math.trunc(48/2**niveau)
        # le pont de la droite passe par les points A et B
        pont = (B[1] - A[1])//(B[0] - A[0])
        # print (B[1], A[1], B[0], A[0])

        Cx = dist//2 + A[0]
        # Cy est egal a la hauteur du point milieu + h calcule la-dessus
        Cy = pont * (Cx - A[0]) + A[1] + h
        C = (Cx, Cy)
        # print(str(C))
        
        Dx = dist//3 + A[0]
        # Dy est calcule a partir de l'equation de la droite
        # passe pare les points A et B
        Dy = pont * (Dx - A[0]) + A[1]
        D = (Dx, Dy)
        # print(str(D))

        Ex = 2 * dist//3 + A[0]
        Ey = pont * (Ex - A[0]) + A[1]
        E = (Ex, Ey)
        # print(str(E))

        # niveau =+ 1

        musique(A, D, niveau+1, niveauMax)
        musique(D, C, niveau+1, niveauMax)
        musique(C, E, niveau+1, niveauMax)
        musique(E, B, niveau+1, niveauMax)



A = (0, 0)
B = (9, 9)

buffHead = array.array("B", range(30))
struct.pack_into("22B", buffHead, 0, 0x4D, 0x54, 0x68, 0x64, 0x00, 0x00, 0x00, 0x06, 0x00, 0x01, 0x00, 0x01, 0x00, 0x80, 0x4D, 0x54, 0x72, 0x6B, 0x00, 0x00, 0x00, 0x05)

fb.write(buffHead)

musique(A, B, 0, 1)

buffEnd = array.array("B", range(10))
struct.pack_into("4B", buffEnd, 0, 0x00, 0xFF, 0x2F, 0x00)
fb.write(buffEnd)

f.write("footer")
