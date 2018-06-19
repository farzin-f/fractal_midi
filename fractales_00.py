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
fb = open("fractalOutputBinary.txt", "wb")
# note = []

def musique(A, B, niveau, niveauMax):

    if niveau == niveauMax:
        duree = B[0] - A[0]
        hauteur = A[1]
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
        header = [0x4D, 0x54, 0x68, 0x64, 0x00, 0x00, 0x00, 0x06, 0x00, 0x01, 0x00, 0x01, 0x00, 0x80, 0x4D, 0x54, 0x72, 0x6B, 0x00, 0x00, 0x00, 0x0A]
        end = [0x00, 0xFF, 0x2F, 0x00]

        buff = array.array("i", range(20))
        struct.pack_into("4f", buff, 0, duree, 0x90, hauteur, 0x60)
        fb.write(buff)        
        f.write(str(note) + "\n")
        
        # print(A, B)
        # return note
                
    else:
        
        # coordonnees = ""
        # note = []
        
        dist = B[0] - A[0]
        h = math.trunc(48/2**niveau)
        # le pont de la droite passe par les points A et B
        pont = (B[1] - A[1])/(B[0] - A[0])
        # print (B[1], A[1], B[0], A[0])

        Cx = dist/2 + A[0]
        # Cy est egal a la hauteur du point milieu + h calcule la-dessus
        Cy = pont * (Cx - A[0]) + A[1] + h
        C = (Cx, Cy)
        # print(str(C))
        
        Dx = dist/3 + A[0]
        # Dy est calcule a partir de l'equation de la droite
        # passe pare les points A et B
        Dy = pont * (Dx - A[0]) + A[1]
        D = (Dx, Dy)
        # print(str(D))

        Ex = 2 * dist/3 + A[0]
        Ey = pont * (Ex - A[0]) + A[1]
        E = (Ex, Ey)
        # print(str(E))

        # niveau =+ 1
        # print(niveau)

        # coordonnees += (str(A)+"\n"+str(D)+"\n"+str(C)+"\n"+str(E)+"\n"+str(B)+"\n")
        # b = struct.pack("10f", A[0],A[1],D[0],D[1],C[0],C[1],E[0],E[1],B[0],B[1])
        # fb.write(b)

        # struct.pack_into(fmt,buffer,offset,v1,v2,...)
        # buff = array.array("c", " "*40)
        # struct.pack_into("10f", buff, 0, A[0],A[1],D[0],D[1],C[0],C[1],E[0],E[1],B[0],B[1])

        

        # f.write(coordonnees)
        
        musique(A, D, niveau+1, niveauMax)
        musique(D, C, niveau+1, niveauMax)
        musique(C, E, niveau+1, niveauMax)
        musique(E, B, niveau+1, niveauMax)



A = (0.0, 0.0)
B = (9.0, 9.0)
musique(A, B, 0, 2)

# buff = array.array("f", " "*40)
# struct.pack_into("40f", buff, 0, )
# fb.write(buff)
# f.write(note)
