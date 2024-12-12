import numpy as np

def f(x):
	return x

def df(x):
	return 1

# les données
X = np.array([  [10,19,13],
                [12,20,16],
                [11,19,20],
                [5,3,6],
				[4,12,8],
                [23,34,35],
                [40,44,49],
                [51,43,52],
				[26,17,24],
                [31,30,25],
                [8,36,23],
                [25,7,15],
				[12,10,11],
                [6,4,8],
                [64,54,60]])
X_t = np.transpose(X)

print("X = ")
print (X)
print("X_t = ")
print (X_t)
# la sortie
t = np.array([[12,14,13,6,7,35,47,48,24,32,22,13,13,7,58]])
print("t = ")
print (t)

# initialisation des poids
W = np.array([  [1/3],
                [1/3],
                [1/3]])

print("W = ")
print (W)

for iter in range(1000):
	# évaluation pour toutes les entrées simultanément
	print("W_T = ")
	print (W.T)
	print("X_t = ")
	print (X_t)

	# donne la valeur d'entree dans le neurone
	a = np.dot(W.T, X_t)

	print ("a = ")
	print (a)

	# donne la valeur de sortie du neurone
	o = a
	print ("t = ")
	print (t)

	print ("o = ")
	print (o)

	# erreur
	epsilon  = t - o
	print ("epsilon  = ")

	print(epsilon)

# le delta = erreur
derivee_de_f = 1
print("derivee_de_f = ")
print(derivee_de_f)

delta = epsilon * 1
print("delta = ")
print(delta)

# mise à jour des poids
print("mise a jour des poids")
print("X_t = ")

print(X_t)
print("delta = ")
print(delta)

Delta_W = (1/100000)*np.dot(X_t, delta.T);
print("Delta_W = ")
print(Delta_W)

print("W = ")
print(W)

W = W + Delta_W

print("W = ")
print(W)

# évaluation pour toutes les entrées simultanément
a = np.dot(W.T, X_t)
# donne la valeur du neurone
o = a

print ("t = ")
print (t)
print ("o = ")
print (o)
print ("fin")