import numpy as np

def f(x):
	if x < 2300 :
		return 0
	if 2300<= x <2500 :
		return 1
	if 2500<= x <3000 :
		return 2
	if 3000 <= x :
		return 3

def df(x):
	return 1

# les données
X = np.array([  [4,24,2954,11,1/6],
                [0,25,1910,13,1/4],
                [4,33,1997,15,1/5],
                [4,39,2852,12,1/5],
				[0,29,1988,9,1/4],
                [0,39,2040,12,1/6],
                [0,52,2000,14,1/6],
                [0,35,2067,10,1/4],
				[0,52,1963,13,1/6],
                [0,36,1875,15,1/5],
                [0,45,1934,14,1/7],
                [0,58,2134,18,1/7],
				[4,53,3501,20,1/6],
                [4,32,3191,13,1/6],
                [0,42,2047,18,1/7]])
X_t = np.transpose(X)

print("X = ")
print (X)
print("X_t = ")
print (X_t)
# la sortie
t = np.array([[2,0,0,3,0,0,0,2,1,0,0,0,0,2,0]])
print("t = ")
print (t)

# initialisation des poids
W = np.array([  [1],
                [1/50],
                [1],
				[1/20],
				[1]])

print("W = ")
print (W)

for iter in range(10000):
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
	o = np.ones((1, 15))

	for i in range(15):
		o[0, i] = f(a[0, i])


	print ("t = ")
	print (t)

	print ("o = ")
	print (o)

	# erreur
	epsilon  = t - o
	print ("epsilon  = ")

	print(epsilon)


# mise à jour des poids
print("mise a jour des poids")
print("X_t = ")

print(X_t)

Epsilon_W = (1/10000)*np.dot(X_t, epsilon.T);
print("Epsilon_W = ")
print(Epsilon_W)

print("W = ")
print(W)

W = W + Epsilon_W

print("W = ")
print(W)

# donne la valeur du neurone
for i in range(15):
	o[0, i] = f(a[0, i])

print ("t = ")
print (t)
print ("o = ")
print (o)
print ("fin")