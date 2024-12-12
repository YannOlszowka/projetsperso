/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

import org.chocosolver.solver.Model;
import org.chocosolver.solver.Solution;
import org.chocosolver.solver.variables.BoolVar;
import org.chocosolver.solver.variables.IntVar;

public class JobShop {
    public static void main(String args[]){

//Création du modèle
Model mon_modele = new Model("JobShop");

//Les données du problème
//-----------------------
        int n = 3; // 3 pieces , 3 jobs
        int m = 3; // 3 operations et 3 machines
        int Dmax = 200; // horizon de taille 200 pour ne pas perdre de solution

        int[][] M = new int[n][m];
        int[][] P = new int[n][m];
        int[][] Tab = new int[n][m];

        M[0][0]=1; M[0][1]=3; M[0][2]=2;
        M[1][0]=1; M[1][1]=3; M[1][2]=2;
        M[2][0]=1; M[2][1]=3; M[2][2]=2;

        P[0][0]=10; P[0][1]=20; P[0][2]=5;
        P[1][0]=20; P[1][1]=5; P[1][2]=25;
        P[2][0]=4; P[2][1]=2; P[2][2]=15;

        Tab[0][0]=0; Tab[0][1]=1; Tab[0][2]=2;
        Tab[1][0]=3; Tab[1][1]=4; Tab[1][2]=5;
        Tab[2][0]=6; Tab[2][1]=7; Tab[2][2]=8;

        IntVar[] date_debut = new IntVar[n*m];
        for (int i=0; i<n; i++){
            for(int j=0; j<m; j++){
                int position = Tab[i][j];
                date_debut[position] = mon_modele.intVar("ES_"+i+"_"+j, 0, Dmax);
            }
        }

        IntVar[] durees = new IntVar[n*m];
        for (int i=0; i<n; i++){
            for(int j=0; j<m; j++){
                durees[i*m+j] = mon_modele.intVar("p_"+i+"_"+j, P[i][j],P[i][j]);
            }
        }

        IntVar[] date_fin = new IntVar[n*m];
        for (int i=0; i<n; i++){
            for(int j=0; j<m; j++){
                date_fin[i*m+j] = mon_modele.intVar("EF_"+i+"_"+j, 0, Dmax);
            }
        }

        BoolVar[][] b = new BoolVar[n*m][n*m];
        for (int i=0; i<n; i++){
            for(int j=0; j<m; j++){
                for (int u=0; u<n; u++){
                    for(int v=0; v<m; v++){
                        b[i*m+j][u*m+v] = mon_modele.boolVar("b_"+i+"_"+j+"_"+u+"_"+v);
                    }
                }
            }
        }

        IntVar OBJ = mon_modele.intVar("Cmax", 0, Dmax);

        //Contrainte 1.

        //Relation entre date de début et de fin

        int[] coeffs = new int[3];
        coeffs[0] = 1; //EF
        coeffs[1] = -1; //ES
        coeffs[2] = -1; //P

        for (int i=0; i<n; i++){
            for(int j=0; j<m; j++){
                int cour = Tab[i][j];
                IntVar[] colonne = new IntVar[3];
                    colonne[0] = date_fin[cour];
                    colonne[1] = date_debut[cour];
                    colonne[2] = durees[cour];
                mon_modele.scalar(colonne, coeffs, "=",0).post();
            }
        }

        // Relation entre la date de debut d'une operation sur une pièce
        // et la date de début de l'opération précédente sur la même pièce

        for (int i=0; i<n; i++){
            for(int j=1; j<m; j++){
                int prec = Tab[i][j-1];
                int cour = Tab[i][j];
                mon_modele.arithm(date_fin[prec],"<=",date_debut[cour]).post();
            }
        }


        //Contrainte 2. Contrainte de disjonction
        for(int i=0; i<n-1; i++){
            for(int j=0; j<m; j++){
                int ope_i = Tab[i][j];
                for(int u=i+1; u<n; u++){
                    for(int v=0; v<m; v++){
                        System.out.println(" i= "+i+" j= "+j+" u= "+u+" v= "+v);
                        int ope_u = Tab[u][v];
                        if (M[i][j]==M[u][v]){
                            mon_modele.ifThenElse(b[ope_i][ope_u],
                                    mon_modele.arithm(date_fin[ope_i],"<=",date_debut[ope_u]),
                                    mon_modele.arithm(date_fin[ope_u],"<=",date_debut[ope_i]));
                        }
                    }
                }
            }
        }

        //Contrainte 3. Déduction de la valeur de la variable Cmax
        for(int s=0; s<n; s++){
            mon_modele.arithm(date_fin[s*m+m-1],"<=",OBJ).post();
        }
        mon_modele.setObjective(Model.MINIMIZE,OBJ);

        //Affichage d'une solution
        System.out.println(mon_modele.toString());
        Solution solution = mon_modele.getSolver().findSolution();
        if(solution != null){
            System.out.println(solution.toString());
        }
    }
}
