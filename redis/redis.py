#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 16:21:04 2018

@author: Mehdi Hennequin and Jeremy Bouin
"""
###########################################Imporation des bibliothèques#################
from tkinter import * #importation de la bibliothèque graphique tkinter
from tkinter import simpledialog #widget fenetre pop up
from tkinter import messagebox
import redis #importation de la bibliotheque redis pour base de données noSql
from random import randint #importation bibliothéque qui permet de générer un int aléatoirement
from datetime import datetime #importe la bibliothéque pour avoir la data actuelle
import time #importe la bibliothèque pour connaitre le temps actuel
import re
################################################################################


# Connexion a la base redis en local sur le port 6379 et la base 0.
r = redis.StrictRedis(host='localhost', port=6379, db=0)

############################################## Fonctions pour l'application

def addOperateur():##### fonction qui permet de rajouter un utilisateur, les utilisateurs sont ajoutés sous forme de set
    answer = simpledialog.askstring("Input", "Donner le nom et prénom de l'opérateur séparés d'un espace",parent=fenetre)## fenetre de dialogue pour rentrer nom et prénom
    hashname = "operateur:" + str(answer)
    r.set(hashname,answer)## on crée un set redis avec comme valeur le nom de l'opérateur
    messageinf = "L'opérateur " + str(answer) + " a été enregisté"##confirmation d'enregistrement
    messagebox.showinfo("Information", messageinf)
    

def buildoperateur():#cette fonction permet de générer au moins deux opérateurs au démarrage de l'application
    #car il n'est pas possible de traiter un appel s'il n'existe pas d'opérateur il est possible par la suite 
    #d'en rajouter avec le bouton ajouter operateur
    r.set("operateur:mehdiHennequin","mehdiHennequin")
    r.set("operateur:jeremyBouin","jeremyBouin")
    
    
def clic(evt):##  lorsque l'on clique avec la souris sur le tableau pour avoir information
    i=lcall.curselection()## Récupération de l'index de l'élément sélectionné
    j=lcallp.curselection()
    k=lop.curselection()
    if i:
        inf = lcall.get(i) ## On retourne l'élément (un string) sélectionné
    if j:
        inf = lcallp.get(j)
    if k:
        inf = lop.get(k)
    informat = r.hgetall(inf)##on récupére l'information sur la base de données redis avec la commande hgetall
    informat = str(informat)##on convertit l'information en string
    informat = informat.replace("b'",'')##on nettoie l'information
    informat = informat.replace("'",'')
    informat = informat.replace("{",'')
    informat = informat.replace("}",'')
    information.delete('1.0', END)##on supprime l'information précédente
    information.insert("end",informat)##on insére l'information dans la balise texte à la fin
    

def addcall() : ## fonction qui permet de rajouter un call qui est identifié par hashset dans redis avec comme valeur l'identifiant de l'appel
    code = randint(1,10000)##on crée on code identifiant l'appel
    numerocall = "0" + str(randint(111111111,799999999))##on crée un numéro de téléphone
    hashname = "call:noIdentify:" + str(code)##on crée le hash de redis
    lcall.insert(1,hashname)##on insére dans la liste box
    d = time.strftime("%H:%M:%S")##on crée la date de l'apel
    r.hset(hashname,"hours call",d)##on ajoute dans redis l'heure
    r.hset(hashname,"number phone",numerocall)##on ajoute dans redis le numéro de téléphone
    r.hset(hashname,"operateur","noIdentify")##on ajoute l'opérateur du numéro dans redis
    r.hset(hashname,"code",code)##on ajoute le code de l'apel dans redis
    
def processOp():##fonction qui permet de prendre un appel et de le mettre en cours de traitement
    i=lcall.curselection()## Récupération de l'index de l'élément sélectionné
    if i:
        inf = lcall.get(i)
        code = r.hget(inf,"code")##récupération du code de l'apel sur redis
        code = int(code)##transformatin en integer
        newname = "call:entraitement:" + str(code)##on crée le nouveau nom de l'appel
        r.rename(inf,newname)##on renomme le hashset de l'appel pour le passer en traitment
        l = r.keys("operateur:*")##on récupére la liste des opérateur
        choixoperateur = randint(0,len(l)-1)##on choisit un opérateur dans la liste au hasard
        r.hset(newname,"operateur",l[choixoperateur])## on met l'opérateur dans hashset de l'appel
        lcallp.insert(1,newname)##on insére le nouvelle appel dans le tableau des appels en cours de traitement
        lcall.delete(i)##on enléve l'appel du tableau des appels à traiter

        
    
def processend():##fonction qui permet de mettre un appel en traité, c'est à dire que l'opérateur à mis fin à l'apel
    j=lcallp.curselection()## Récupération de l'index de l'élément sélectionné
    i = lcall.curselection()
    if j:
        inf = lcallp.get(j)
        code = r.hget(inf,"code")
        code = int(code)
        newname = "call:finappel:" + str(code)
        r.rename(inf,newname)
        lop.insert(1,newname)
        lcallp.delete(j)
    if i :
        inf = lcall.get(i)
        code = r.hget(inf,"code")
        code = int(code)
        newname = "call:appelNontraiter:" + str(code)
        r.rename(inf,newname)
        lop.insert(1,newname)
        lcall.delete(i)
        
    
def returncall() :##fonction qui récupére au démarrage de l'application tous les appels
    allcall = r.keys('call:noIdentify:*')##
    return allcall

def returnend():##fonction qui récupére au démarrage de l'application les appels non traités
    allend = r.keys('call:appelNontraiter:*')##
    return allend

def returncp():##fonction qui récupére au démarrage de l'application les appels en traitement
    allcp = r.keys('call:entraitement:*')##
    return allcp
    
def listec():## fonction qui affiche au démarrage de l'application tous les appels
    l = returncall()##
    for i in range(0,len(l)):##
        lcall.insert(i,l[i])##


def listecp():##onction qui affiche au démarrage de l'application tous les appels non traité
    lo = returncp()##
    for j in range(0,len(lo)):##
        lcallp.insert(j,lo[j])##

def listeend():##onction qui affiche au démarrage de l'application tous les appels en traitement
    lend = returnend()##
    for j in range(0,len(lend)):##
        lop.insert(j,lend[j])##
    
##################################### Fin fonctions application   


##################################### Définition de la fenetre IHM en utilisant tkinter
fenetre = Tk()


panelprincipal = PanedWindow(fenetre, orient=VERTICAL,background="gray64")
panelprincipal.pack()
titre = PanedWindow (fenetre, orient=HORIZONTAL,background="gray64")
titre.pack()
secondpanel = PanedWindow(fenetre,orient=HORIZONTAL,background="gray64")
secondpanel.pack()

troisiemepanel = PanedWindow(fenetre,orient=HORIZONTAL,background="gray64")
troisiemepanel.pack()
panelprincipal.add(titre)
panelprincipal.add(secondpanel)
panelprincipal.add(troisiemepanel)


information = Text(panelprincipal)
information.config(width=47, height=5)
information.insert("end","Information de l'appel")
information.pack()
panelprincipal.add(information)


titre.add(Label(titre, text='Appels en traitement', background='gray80', anchor=CENTER,width=20))
titre.add(Label(titre, text='Liste des appels émis', background='gray95', anchor=CENTER,width=19) )
titre.add(Label(titre, text='Liste fin appel', background='gray80', anchor=CENTER,width=20))




addop=Button(troisiemepanel, text="Ajouter un opérateur", command= addOperateur)
addop.pack()
addcall=Button(troisiemepanel, text="Ajouter un appel", command= addcall)
addcall.pack()
procescall=Button(troisiemepanel, text="Traiter un appel", command= processOp)
procescall.pack()
endcall=Button(troisiemepanel, text="Fin appel", command= processend)
endcall.pack()
troisiemepanel.add(addop)
troisiemepanel.add(addcall)
troisiemepanel.add(procescall)
troisiemepanel.add(endcall)





lcallp = Listbox(secondpanel)

lcallp.pack()

lcall = Listbox(secondpanel)
lop = Listbox(secondpanel)
lcall.pack()
lop.pack()



secondpanel.add(lcallp)
secondpanel.add(lcall)
secondpanel.add(lop)

listec()
listecp()
listeend()
buildoperateur()


lcall.bind('<ButtonRelease-1>',clic)
lcallp.bind('<ButtonRelease-1>',clic)
lop.bind('<ButtonRelease-1>',clic)

fenetre.configure(background="gray90")
fenetre.mainloop()
