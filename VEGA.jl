# Programme VEGA

using Shuffle
using SimpleRandom
using Plots

# Premiere fonction objectif

function z1(x)
  if x <= 1
    y = -x
  elseif 1 < x <= 3
    y = x-2
  elseif 3 < x <= 4
    y = 4-x
  else
    y = x-4
  end
  return y
end

# Deuxieme fonction objectif

function z2(x)
  y = (x-5)^(2)
  return y
end

# Algorithme VEGA

function VEGA(nIndividuals,nGenerations,Pc,Pm)
  #Initialisation
  m = 16 # Nombre de bits
  k = (nIndividuals/2) # Nombre d individus divise par le nombre d objectifs
  k = round.(Int,k) # k de type Int
  B = zeros(nIndividuals,m)
  X = zeros(nIndividuals,1)
  Y = zeros(nIndividuals,1)
  b = zeros(nIndividuals,1)
  #
  for i = 1:nIndividuals
    for j = 1:m
      B[i,j] = rand([0,1])
      Y[i,1] = Y[i,1] + B[i,j]*2^(j-1)
    end
  B = round.(Int, B)
  Y = round.(Int, Y)
  X[i,1] = (-5) + Y[i,1]*(15/(2^(m)-1))
  print("b(x) = ",B[i,:]," x = ", X[i,1]," z1(x) = ",z1(X[i,1])," z2(x) = ",z2(X[i,1])," \n ")
  end
  #
  print(" \n ")
  #
  # Affichage du graphe (z1(X),z2(X)) pour X a l initialisation
  #
  plot(z1.(X),z2.(X),color = :red,markershape=:circle, title="Espace objectif", xlab=" z1(X) ", ylab=" z2(X) " , legend=:topleft,label="Initialisation",linetype=:scatter)
  #
  for i = 1:nGenerations
    #PickIndividuals
    #
    Xpick = X
    S1 = zeros(k,m)
    S2 = zeros(k,m)
    X1 = zeros(k,1)
    X2 = zeros(k,1)
    #
    # Definition de la sous population S1
    #
    for i = 1:k
      for j = 1:2*k
        if minimum(minimum.([z1.(Xpick)])) == z1(Xpick[j,1])
          S1[i,:] = B[j,:]
          X1[i,1] = Xpick[j,1]
          Xpick[j,1] = 10
        end
      end
    end
    #
    # Definition de la sous population S2
    #
    for i = 1:k
      for j = 1:2*k
        if minimum(minimum.([z2.(Xpick)])) == z2(Xpick[j,1])
          S1[i,:] = B[j,:]
          X2[i,1] = Xpick[j,1]
          Xpick[j,1] = -5
        end
      end
    end
    #
    # Shuffle de S
    #
    S = zeros(nIndividuals,m)
    #
    for i = 1:k
      S[i,:] = S1[i,:]
    end
    #
    for i = k+1:nIndividuals
      S[i,:] = S2[i-k,:]
    end
    #
    Scat =
    S = S[shuffle(1:nIndividuals), :]
    S = round.(Int,S)
    #
    #
    # Evolution
    #
    # Definition aleatoire du vecteur des coupes
    Cut = zeros(k)
    for i = 1:k
      Cut[i] = rand(1:1:m-1)
    end
    Cut = round.(Int,Cut)
    #
    # Definition de la matrice des individus issus d'un crossover selon S et le vecteur Cut
    Sc = S
    for i = 1:k
      Sc[2i-1,Cut[i]+1:m] = S[2i,Cut[i]+1:m]
      Sc[2i,Cut[i]+1:m] = S[2i-1,Cut[i]+1:m]
    end
    #
    # Definition aleatoire du vecteur Bit indiquant sur quels bits ont lieu les mutations
    Bit = zeros(nIndividuals)
    for i = 1:nIndividuals
      Bit[i] = rand(1:1:m)
    end
    Bit = round.(Int,Bit)
    #
    # Definition de la matrice des individus issus d'un crossover et d'une mutation selon Sc et le vecteur Bit
    Scm = Sc
    for i = 1:nIndividuals
      if Scm[i,Bit[i]] == 0
        Scm[i,Bit[i]] = 1
      else Scm[i,Bit[i]] == 1
        Scm[i,Bit[i]] = 0
      end
    end
    #
    # Definition de la matrice des individus issus d'une mutation selon S et le vecteur Bit
    Sm = S
    for i = 1:nIndividuals
      if Sm[i,Bit[i]] == 0
        Sm[i,Bit[i]] = 1
      else Sm[i,Bit[i]] == 1
        Sm[i,Bit[i]] = 0
      end
    end
    #
    # La variable Hc vaut 0 avec probabilite 1-Pc
    # Elle vaut 1 avec probabilite Pc
    Hc = RV{Int, Float64}()
    Hc[0] = 1-Pc
    Hc[1] = Pc
    #
    # La variable Hm vaut 0 avec probabilite 1-Pm
    # Elle vaut 1 avec probabilite Pm
    Hm = RV{Int, Float64}()
    Hm[0] = 1-Pm
    Hm[1] = Pm
    #
    # Modification de la population B decrivant que crossovers et mutations ont eu
    # lieu pour la generation d individus, selon les probabilites Pc et Pm
    for i = 1:nIndividuals
      for j = 1:m
        C1 = random_choice(Hc)
        C2 = random_choice(Hm)
        if C1 == 0 & C2 == 0
          B[i,j] = S[i,j]
        elseif C1 == 0 & C2 == 1
          B[i,j] = Sm[i,j]
        elseif C1 == 1 & C2 == 0
          B[i,j] == Sc[i,j]
        else C1 == 1 & C2 == 1
          B[i,j] == Scm[i,j]
        end
      end
    end
    #
    # Actualisation de B et de X
    Y = zeros(nIndividuals,1)
    for i = 1:nIndividuals
      for j = 1:m
        Y[i,1] = Y[i,1] + B[i,j]*2^(j-1)
      end
      B = round.(Int, B)
      Y = round.(Int, Y)
      X[i,1] = (-5) + Y[i,1]*(15/(2^(m)-1))
    end
  end
  #
  # Affichage des informations relatives aux individus et a leurs elements
  # associes dans Xpe et Ype, a l issue du process generationnel
  # Affichage des approximations obtenues
  for i = 1:nIndividuals
    print("b(x) = ",B[i,:]," x = ", X[i,1]," z1(x) = ",z1(X[i,1])," z2(x) = ",z2(X[i,1])," \n ")
  end
  #
  # Superposition des graphes (z1(X),z2(X)) pour X a l intialisation et X a la fin de l'algorithme
  plot!(z1.(X),z2.(X),color =:yellow ,markershape=:star, label="N-ième génération", linetype=:scatter)
  #
end
