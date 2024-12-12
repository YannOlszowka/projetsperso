from constraint import *
from numpy import zeros

problem = Problem()


k = 3  # nb de pieces
n = 3  # nb de machines et d operations

# Temps de traitement par les machines des operations j sur les pieces i
P = zeros((k,n), int)
P[0][0] = 10
P[0][1] = 20
P[0][2] = 5
P[1][0] = 20
P[1][1] = 5
P[1][2] = 25
P[2][0] = 4
P[2][1] = 2
P[2][2] = 15

# Toutes les pieces passent sur les machines dans le meme ordre
M = zeros((k,n), int)
M[0][0] = 1
M[0][1] = 3
M[0][2] = 2
M[1][0] = 1
M[1][1] = 3
M[1][2] = 2
M[2][0] = 1
M[2][1] = 3
M[2][2] = 2

# On definit un horizon de planification assez large pour pouvoir traiter le probleme sans qu il en restreigne
# l ensemble des solutions
x = 0
for i in range(3):
    for j in range(3):
        x = x + P[i][j]

D = x

def conjonction(sti, stj, dureej):
   valeurj = int(dureej)
   if (sti>=stj+valeurj):
       return True
   else:
       return False

def disjonction(sti,dureei, stj, dureej):
   valeur1 = int( dureei)
   valeur2 = int(dureej)
   if ( (stj >= sti+valeur1) or (sti >= stj+valeur2) ):
       return True
   else:
       return False


def calculer_cout(cout, f1, f2, f3, d1, d2, d3):
    valeur1 = int(d1)
    valeur2 = int(d2)
    valeur3 = int(d3)

    if (cout == f1 + d1) or (cout == f2 + d2) or (cout == f3 + d3):
        return True
    else:
        return False

# On ajoute au probleme les variables representant les dates de debut de chaque operation j sur chaque piece i
# Avec range(s,D) pour domaine car le debut de la j ieme operation ne peut qu etre plus tard que la somme des durees de traitement
# des operations precedentes
for i in range (k):
    s = 0
    for j in range (n):
        nom = "st_"+str(i)+"_"+str(j)
        problem.addVariable(nom, range(s, D))
        print(str(nom)+">="+str(s))
        s = s+ P[i][j]

# On ajoute au probleme les variables representant les P[i][j] pour tous les couples (piece,operation)
for i in range (k):
    for j in range (n):
        nom = "duree_"+str(i)+"_"+str(j)
        print(str(nom)+"="+str(P[i][j]))
        problem.addVariable(nom, range(P[i][j], P[i][j]+1))

Cmax = "Cout maximum"
problem.addVariable(Cmax, range(0, D))

# On ajoute au probleme la contrainte de conjonction pour toutes les pieces i
for i in range(0,3):
    for j in range(1,3):
        nom_prec = "st_"+str(i)+"_"+str(j-1)
        nom = "st_"+str(i)+"_"+str(j)

        duree_prec = "duree_"+str(i)+"_"+str(j-1)

        print(str(nom)+">="+str(nom_prec))
        problem.addConstraint(conjonction, ([nom,nom_prec, duree_prec]))

# On ajoute au probleme la contrainte de disjonction qui s applique aux couples (piece,operation) qui ont lieu sur la meme machine
for i in range(k-1):
    for j in range(n):
        for i2 in range(i+1,k):
            for j2 in range(n):
                nom = "st_"+str(i)+"_"+str(j)
                nom2 = "st_"+str(i2)+"_"+str(j2)
                duree = "duree_"+str(i)+"_"+str(j)
                duree2 = "duree_"+str(i2)+"_"+str(j2)
                if (M[i][j]==M[i2][j2]):
                   problem.addConstraint(disjonction, ([nom,duree,nom2, duree2]))

# On ajoute au probleme la contrainte qui calcule le cout maximum
cout = "Cout maximum"
nom = "st_"+str(0)+"_"+str(2)
nom2 = "st_"+str(1)+"_"+str(2)
nom3 = "st_"+str(2)+"_"+str(2)
duree = "duree_"+str(0)+"_"+str(2)
duree2 = "duree_"+str(1)+"_"+str(2)
duree3 = "duree_"+str(2)+"_"+str(2)

problem.addConstraint(calculer_cout, ([cout, nom,nom, nom2, duree, duree2, duree3]))

# On trouve une solution
solutions = problem.getSolution()

# On affiche la solution trouvee avec l affichage par defaut
print("-- affichage par défaut --")
print(solutions)

# On affiche la solution trouvee de maniere plus lisible et esthetique
print("-- affichage detaille --")
nom = "Cout maximum"
valeur = solutions[nom]
print("cout = "+str(valeur))

for i in range(k):
    for j in range(n):
        nom = 'st_'+str(i)+'_'+str(j)
        valeur = solutions[nom]
        print(valeur," \t ",end='')
    print(" \n ")

print("\n fin...")

