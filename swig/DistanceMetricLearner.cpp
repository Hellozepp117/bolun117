//DistanceMetricLearner.cpp

#include<strstream>
#include <fstream>
#include <iostream>
#include <ilcplex/ilocplex.h>
#include <string>
#include <algorithm>
#include <map>

using namespace std;

ILOSTLBEGIN

typedef IloArray<IloNumArray>    NumMatrix;
typedef IloArray<IloNumVarArray> NumVarMatrix;
typedef IloArray<NumMatrix>   Num3Matrix;

class DistanceMetricLearner
{

	private:
		double epsilon;
		double epsilon_up;
		double epsilon_low;
		IloInt n;
		IloInt d;
		double Maxi_epsilon;
		double temp_priv;
		int i_p, j_p, k_p;
		bool features_bool=0;
		bool labels_raw_bool=0;
		bool outliers_bool=0;
		bool features_raw_bool=0;
		bool Matrix_B_bool=0;
		bool Matrix_D_bool=0;
		bool R_bool = 0;
		bool epsilon_loop_bool = 0;
		bool outliers_num_bool = 0;
		bool outliers_change_flag = 0;
		double ** features;
		int *labels_raw;
		int *outliers;
		int *outliers_num;
		double *features_raw;
		double ** Matrix_B;
		double ** Matrix_D;
		double *R;
		double *epsilon_loop;
		std::map<int, string> D_ij_map;
		std::map<int, string> D_ik_map;
		std::map<int, string> D_ij_ub_map;
		std::map<int, string> D_ij_lb_map;


		// Distance metric parameters
		bool include_first_order_terms=0; // ¡°a¡± vector
		bool include_second_order_terms=1; // ¡°B¡± vector; Note that in all our experiments, this will always be true
		bool include_third_order_terms=0; // ¡°C¡± matrix
		bool enforce_diagonal_dominance=0; // ¡°a¡± vector



	public:

		void Set_distance_option(bool a, bool b, bool c, bool e)// set Distance metric parameters
		{
			include_first_order_terms = a; // ¡°a¡± vector
			include_second_order_terms = b; // ¡°B¡± vector; Note that in all our experiments, this will always be true
			include_third_order_terms = c; // ¡°C¡± matrix
			enforce_diagonal_dominance = e; // ¡°a¡± vector
		}


		/*void temp_set_parameters()//temp
		{
			n = 8; d = 2; 
			labels_raw_bool = 1;
			labels_raw = new int[n];
			labels_raw[8] = { 1, 1, 0, 0, 0, 0, 1, 0 };
			features_bool = 1;
			features = new double*[n];
			for (int i = 0; i < n; i++)
				features[i] = new double[d];
			features[][2] = { 1, 0.233, 0.681, 0.976, 0.76, 0.547, 0.662, 0.315, 0.383, 0.721, 0.341, 0.702, 0, 0.709, 0.565, 0.204 };

		}*/

		void release_dynamic_memory()
		{
			if (features_bool != 0)
			{
				for (int i = 0; i < n; i++)
					delete[]features[i];
				delete[]features;
			}
			if (Matrix_B_bool != 0)
			{
				for (int i = 0; i < d; i++)
					delete[]Matrix_B[i];
				delete[]Matrix_B;
			}
			if (Matrix_D_bool != 0)
			{
				for (int i = 0; i < d; i++)
					delete[]Matrix_D[i];
				delete[]Matrix_D;
			}
			if (labels_raw_bool != 0)
			{
				delete[]labels_raw;
			}
			if (features_raw_bool != 0)
			{
				delete[]features_raw;
			}
			if (outliers_bool != 0)
			{
				delete[]outliers;
			}
			if (R_bool != 0)
			{
				delete[]R;
			}
			if (outliers_num_bool != 0)
			{
				delete[]outliers_num;
			}
			if (epsilon_loop_bool != 0)
			{
				delete[]epsilon_loop;
			}

		}


		int CountLines(char *filename)//acquire lines of the file
		{
			ifstream ReadFile;
			int line = 0;
			string temp;
			ReadFile.open(filename, ios::in);
			if (ReadFile.fail())//fail to open file, return 0
			{
				return 0;
			}
			else
			{
				while (getline(ReadFile, temp))
				{
					line++;
				}
				return line;
			}
			ReadFile.close();
		}

		int count_d(char* str)
		{
			int count=0;
			char *pstr;
			pstr = str;
			while (*pstr != 0)
			{
				if (*pstr == '.')
				{
					count++;
				}
				pstr++; 
			}
			return count;
		}

		void Read_data(char *filename)
		{
			ifstream file;
			file.open(filename, ios::in);
			int line;
			if (file.fail())
			{
				cout << "file does not exist!" << endl;
				file.close();
				cin.get();
				cin.get();
			}
			else
			{
				n = CountLines(filename);
				//n = 500;//testing
				cout << "n=" << n << endl;
				string *buff = new string[n];
				string div = ":";
				string space = " ";
				for (int i = 0; i < n; i++)
				{
					getline(file, buff[i]);
					string_replace(buff[i], div, space);
				}
				file.close(); //close file


				//count_dimension
				char *ch = new char[buff[0].size() + 1];
				strcpy(ch, buff[0].c_str());
				d = count_d(ch);

				//load data
				double ** data_raw;
				data_raw = new double*[n];
				for (int i = 0; i < n; i++)
				{
					data_raw[i] = new double[d+1];
					for (int j = 0; j < d+1; j++)
						data_raw[i][j] = 0;
				}

				for (int j,i = 0; i < n; i++)
				{
					ch = new char[buff[i].size() + 1];
					strcpy(ch, buff[i].c_str());
					j = 0;
					for (int k=0;;k++)
					{
						data_raw[i][k]=atof(ch + j);
						if (k == d)
							break;
						j++;
						for (;;j++)
						{
							if (ch[j] == ' ')
								break;
						}

					}
				}

				// read data
				labels_raw_bool = 1;
				labels_raw = new int[n];
				for (int i = 0; i < n; i++)
				{
					labels_raw[i]= data_raw[i][0] ;
				}

				features_bool = 1;
				features = new double*[n];
				for (int i = 0; i < n; i++)
					features[i] = new double[d];

				for (int i = 0; i < n; i++)
				{
					for (int j = 0; j < d; j++)
					{
						features[i][j] = data_raw[i][j+1];
					}
				}




				//output test
				/*
				cout << "labels:"<< endl;
				for (int i = 0; i < n; i++)
				{
					cout<<labels_raw[i]<<"\t";
				}
				cout << endl;

				cout << "features:" << endl;
				for (int i = 0; i < n; i++)
				{
					for (int j = 0; j < d; j++)
					{
						cout << features[i][j] << "\t";
					}
					cout << endl;
				}


				for (int i = 0; i < n; i++)
					delete[]data_raw[i];
				delete[]data_raw;
				delete[]ch;
				cin.get();
				cin.get();
				*/
				
			}
		}

		void Set_LP_dimension()
		{
			printf("Please insert the value of dimension: ");
			cin >> d;
		}

		int string_replace(string &s1, const string &s2, const string &s3)
		{
			string::size_type pos = 0;
			string::size_type a = s2.size();
			string::size_type b = s3.size();
			while ((pos = s1.find(s2, pos)) != string::npos)
			{
				s1.replace(pos, a, s3);
				pos += b;
			}
			return 0;
		}

		void Set_LP_obs()
		{
			printf("Please insert the # of observastions: ");
			cin >> n;


			////
			printf("Please insert the labels of observastions(divided by space): \n");
			labels_raw_bool = 1;
			labels_raw = new int[n];
			for (int i = 0; i < n; i++)
			{
				cin >> labels_raw[i];
			}

			//////////////////////

			printf("Please insert the data of observastions(ignore the dimension,with numbers divided by space): \n");

			features_raw_bool = 1;
			features_raw = new double[n*d];

			for (int i = 0; i < n*d; i++)
				cin >> features_raw[i];

			///////////
			features_bool = 1;
			features = new double*[n];
			for (int i = 0; i < n; i++)
				features[i] = new double[d];

			for (int i = 0; i < n; i++)
			{
				for (int j = 0; j < d; j++)
				{
					features[i][j] = features_raw[d * i+j];
				}
			}

			
		}

		void Set_LP_epsilon()
		{
			int k;
			double temp;
			printf("Option 1.Please insert ratio of MAX_epsilon(make sure you have run FindMaxEpsilon() ). \n");
			printf("Option 2.Please insert the value of epsilon. £¨1 or 2£©:\n");
			cin >> k;
			if (k == 2)
			{
				printf("Please insert the value of epsilon: ");
				cin >> epsilon;
			}
			if (k == 1)
			{
				cout << "Max epsilon =" << Maxi_epsilon << endl;
				printf("Please insert the ratio: ");
				cin >> temp;
				epsilon = temp*Maxi_epsilon;
			}
		}

		void Reset_Outliers()
		{
			outliers_bool = 1;
			outliers = new int[n];
			for (int i = 0; i < n; i++)
				outliers[i] = 0;
		}

		void Detect_Outliers()
		{
			double *intemp;
			double *outtemp;
			int *outliers_temp;
			double temp = 999, temp2 = 999, eps=0.0000001;
			intemp = new double[n];
			outtemp = new double[n];
			outliers_temp = new int[n];


			DistanceMetricLearner:Set_Matrix_D_with(Matrix_B);
			for (int i = 0; i < n; i++)
			{
				temp = 999, temp2 = 999;
				if (outliers[i] == 0)
				{
					for (int j = 0; j < n; j++)
					{
						if (outliers[j] == 0)
						{
							if ((i != j) && (labels_raw[i] != labels_raw[j]) && (temp>Matrix_D[i][j]))
							{
								temp = Matrix_D[i][j];
								outtemp[i] = temp;
							}
							if ((i != j) && (labels_raw[i] == labels_raw[j]) && (temp2>Matrix_D[i][j]))
							{
								temp2 = Matrix_D[i][j];
								intemp[i] = temp2;
							}

						}
					}

				}
			}

			for (int i = 0; i < n; i++)
				outliers_temp[i] = outliers[i];

			for (int i = 0; i < n; i++)
			{
				if (intemp[i] + eps> outtemp[i])
					outliers_temp[i] = 1;
			}


			outliers_change_flag = 0;
			for (int i = 0; i < n; i++)
			{
				if (outliers_temp[i] != outliers[i])
				{
					outliers_change_flag = 1;
					outliers[i] = outliers_temp[i];
				}
			}
			delete[]intemp;
			delete[]outtemp;
			delete[]outliers_temp;

			cout << "detect outliers:" << endl;
			for (int i = 0; i < n; i++)
			{
				if (outliers[i] == 1)
					cout << i << "\t";
			}
			cout << endl;

		}

		void reinsert_outliers_MILP()
		{
			IloEnv env;
			try {
				//definition of variables
				IloModel model(env, "MILP");
				IloNum M = 1;
				IloNum Rho = 2;
				IloNumArray labels(env, n);
				for (int i = 0; i < n; i++)
				{

					labels[i] = labels_raw[i];

				}

				////////////define y_ij;
				NumVarMatrix y(env, n);
				for (int i = 0; i < n; i++)
				{

					y[i] = (IloNumVarArray(env, n, 0, 1, ILOINT));
				}


				////////////define z_i;
				IloNumVarArray z(env, n, 0, 1, ILOINT);

				////////////define lambda_i;
				IloNumVarArray lambda(env, n, 0, IloInfinity, ILOFLOAT);


				//constraint D_ij
				for (int i = 0; i < n; i++)
				{
					for (int j = 0; j < n; j++)
						Matrix_D[i][j] = 0;

				}
				for (int i = 0; i < n; i++)
				{
						for (int j = 0; j < n; j++)
						{
							if (i != j)
							{
								for (int k = 0; k < d; k++)
								{
									Matrix_D[i][j] += (features[i][k] - features[j][k]) * (features[i][k] - features[j][k]) * Matrix_B[k][k];
								}
								for (int p = 0; p < d - 1; p++)
								{
									for (int l = p + 1; l < d; l++)
									{
										Matrix_D[i][j] += 2 * (features[i][p] - features[j][p])* (features[i][l] - features[j][l]) * Matrix_B[p][l];
									}
								}
							}
						}
					
				}


				//Main constraint
				//(1):
				for (int i = 0; i < n; i++)
				{
					IloExpr temp1(env);
					for (int j = 0; j < n; j++)
					{
						if ((labels[i] == labels[j]) && (i != j))
							temp1 += Matrix_D[i][j] * y[i][j];
					}

					for (int k = 0; k < n; k++)
					{
						if (labels[i] != labels[k])
						{
							model.add(temp1 + lambda[i] <= Matrix_D[i][k] + M * (z[i] + z[k]));
						}
					}
					temp1.end();
				}

				//(2)
				for (int i = 0; i < n; i++)
				{
					model.add(lambda[i] <= 1-z[i]);
				}

				//(3)
				for (int i = 0; i < n; i++)
				{
					if (outliers[i] == 0)
						model.add(z[i] == 0);
				}
				
				//(4)
				for (int i = 0; i < n; i++)
				{
					IloExpr temp2(env);
					for (int j = 0; j < n; j++)
					{
						if ((labels[i] == labels[j]) && (i != j))
							temp2 += y[i][j];
					}
					model.add(temp2 == 1);

					temp2.end();
				}

				//(5)
				for (int i = 0; i < n; i++)
				{
					for (int j = 0; j < n; j++)
					{
						if ((labels[i] == labels[j]) && (i != j))
							model.add(y[i][j]+z[j] <= 1);
					}

				}


				//OBJ
				IloExpr obj(env);

				for (int i = 0; i < n; i++)
				{

						obj += (lambda[i]-Rho*z[i]);
				}

				model.add(IloMaximize(env, obj));
				obj.end();

				//solve
				IloCplex cplex(env);
				cplex.solve();

				//output


				/////////get Obj
				cplex.out() << "Objective value = " << cplex.getObjValue() << endl;

				/////////get outliers
				cout << "reinsert outliers:" << endl;
				for (int i = 0; i < n; i++)
				{
					if (outliers[i] != cplex.getValue(z[i]))
						cout << i << "\t";
				}
				cout << endl;


				for (int i = 0; i < n; i++)
				{
					outliers[i] = cplex.getValue(z[i]);
				}

				cout << "outliers:" << endl;
				for (int i = 0; i < n; i++)
				{
					if (outliers[i] == 1)
						cout << i << "\t";
				}
				cout << endl;



			}
			catch (IloException& ex) {
				cerr << "Error: " << ex << endl;
			}

			env.end();

		}


		void Set_Euclidean_Matrix_B()
		{
			for (int i = 0; i < d; i++)
			{
				for (int j = 0; j < d; j++)
				{
					if (i == j)
						Matrix_B[i][j] = 1;
					else
						Matrix_B[i][j] = 0;
				}
			}
		}
		void Calculate_min_D_ij_without_O(int i)
		{

				temp_priv = 999;
				if (outliers[i] == 0)
				{
					for (int j = 0; j < n; j++)
					{
						if (outliers[j] == 0)
						{
							if ((i != j) && (labels_raw[i] == labels_raw[j]) && (temp_priv>Matrix_D[i][j]))
							{
								temp_priv = Matrix_D[i][j];
								i_p = i;
								j_p = j;
							}
						}
					}
				}

		}

		void Set_D_ij_Constraint_map(IloEnv env, IloModel model, IloNumVarArray a, NumVarMatrix B, IloNumVarArray D_array, int idx, int i, int j)
		{

				IloExpr D_ij_temp(env);
				for (int k = 0; k < d; k++)
				{
					if (include_first_order_terms)
					{
						D_ij_temp += fabs(features[i][k] - features[j][k]) * a[k];
					}
					D_ij_temp += (features[i][k] - features[j][k]) * (features[i][k] - features[j][k]) * B[k][0];
				}
				for (int p = 0; p < d - 1; p++)
				{
					for (int l = p + 1; l < d; l++)
					{
						D_ij_temp += 2 * (features[i][p] - features[j][p])* (features[i][l] - features[j][l]) * B[p][l - p];
					}
				}
				model.add(D_array[idx] == D_ij_temp);
				D_ij_temp.end();		

		}

		void Calculate_min_D_ik_without_O(int i)
		{
				temp_priv = 999;
				if (outliers[i] == 0)
				{
					for (int k = 0; k < n; k++)
					{
						if (outliers[k] == 0)
						{
							if ((labels_raw[i] != labels_raw[k]) && (temp_priv>Matrix_D[i][k]))
							{
								temp_priv = Matrix_D[i][k];
								i_p = i;
								k_p = k;
							}
						}
					}
				}

		}

		bool Find_in_Map(int i, int j, std::map<int, string> mymap)
		{
			int t = i*n + j;
			string str;
			str = to_string(t);
			map<int, string>::iterator itr;
			for (itr = mymap.begin(); itr != mymap.end(); itr++)
			{
				if (str.compare(itr->second) == 0)
				{
					return 1;
					break;
				}
			}
			return 0;
		}

		void Find_min_D_ij_without_O(int i)
		{

				temp_priv = 999;
				if (outliers[i] == 0)
				{
					for (int j = 0; j < n; j++)
					{
						if (outliers[j] == 0)
						{
							if ((i != j) && (temp_priv>Matrix_D[i][j]))
							{
								temp_priv = Matrix_D[i][j];
								i_p = i;
								j_p = j;
							}
						}
					}
				}

		}

		void Find_max_D_ij_without_O(int i)
		{

				temp_priv = -999;
				if (outliers[i] == 0)
				{
					for (int j = 0; j < n; j++)
					{
						if (outliers[j] == 0)
						{
							if ((i != j) && (temp_priv<Matrix_D[i][j]))
							{
								temp_priv = Matrix_D[i][j];
								i_p = i;
								j_p = j;
							}
						}
					}
				}

		}


		void Set_Matrix_D_with(double ** Matrix_B)
		{
			DistanceMetricLearner::Initialize_Matrix_D();
			for (int i = 0; i < n; i++)
			{
				for (int j = 0; j < n; j++)
				{
					if (i != j)
					{
						for (int k = 0; k < d; k++)
						{
							Matrix_D[i][j] += (features[i][k] - features[j][k]) * (features[i][k] - features[j][k]) * Matrix_B[k][k];
						}
						for (int p = 0; p < d - 1; p++)
						{
							for (int l = p + 1; l < d; l++)
							{
								Matrix_D[i][j] += 2 * (features[i][p] - features[j][p])* (features[i][l] - features[j][l]) * Matrix_B[p][l];
							}
						}
					}
				}
			}
		}


		void Print_outliers()
		{
			cout << "outliers:" << endl;
			for (int i = 0; i < n; i++)
			{
				if (outliers[i] == 1)
					cout << i << "\t";
			}
			cout << endl;
		}

		void Calculate_Ri()
		{
			R_bool = 1;
			R = new double[n];
			for (int i = 0; i < n; i++)
				R[i] = 0;

			double temp, temp2;
			for (int i = 0; i < n; i++)
			{
				temp = 999, temp2 = 999;
				if (outliers[i] == 1)
				{
					for (int j = 0; j < n; j++)
					{
						if (outliers[j] == 0)
						{
							if ((i != j) && (labels_raw[i] != labels_raw[j]) && (temp>Matrix_D[i][j]))
							{
								temp = Matrix_D[i][j];
							}
							if ((i != j) && (labels_raw[i] == labels_raw[j]) && (temp2 > Matrix_D[i][j]))
							{
								temp2 = Matrix_D[i][j];
							}
						}
					}
					R[i] = temp / temp2;
				}
			}

		}


		void calculate_D_ij_with_outliers()
		{
			for (int i = 0; i < n; i++)
			{
				if (outliers[i] == 1)
				{
					for (int j = 0; j < n; j++)
					{
						if (outliers[j] != 1)
						{
							Matrix_D[i][j] = 0;
							for (int k = 0; k < d; k++)
							{
								Matrix_D[i][j] += (features[i][k] - features[j][k]) * (features[i][k] - features[j][k]) * Matrix_B[k][k];
							}
							for (int p = 0; p < d - 1; p++)
							{
								for (int l = p + 1; l < d; l++)
								{
									Matrix_D[i][j] += 2 * (features[i][p] - features[j][p])* (features[i][l] - features[j][l]) * Matrix_B[p][l];
								}
							}
						}
					}
				}
			}
		}


		void reinsert_outliers()
		{
			
			for (;;)
			{
				
				////calculate D_ij with outliers
				DistanceMetricLearner::calculate_D_ij_with_outliers();

				/////calculate Ri
				DistanceMetricLearner::Calculate_Ri();

				////reinsert by order, until Ri<1;
				double temp = 0;
				int ii = 0;
				for (int i = 0; i < n; i++)
				{
					if ((outliers[i] == 1) && (temp < R[i]))
					{
						temp = R[i];
						ii = i;
					}


				}
				if (R[ii]>1)
					outliers[ii] = 0;

				/////output

				if (R[ii] <= 1)
				{
					cout << "Nothing to re-insert" << endl;
					cout << "Largest R[" << ii << "] = " << temp << endl;
					break;
				}
				else
					cout << "Re-insert point " << ii << "\n" << "R[" << ii << "] = " << temp << endl;
			}
			cout << "outliers:" << endl;
			for (int i = 0; i < n; i++)
			{
				if (outliers[i] == 1)
					cout << i << "\t";
			}
			cout << endl;




		}

		void Initialize_Matrix_B()
		{
			Matrix_B_bool = 1;
			Matrix_B = new double*[d];
			for (int i = 0; i < d; i++)
				Matrix_B[i] = new double[d];

			for (int i = 0; i < d; i++)
			{
				for (int j = 0; j < d; j++)
				{
					Matrix_B[i][j] = 0;
				}
			}
		}

		void Initialize_Matrix_D()
		{
			Matrix_D_bool = 1;
			Matrix_D = new double*[n];
			for (int i = 0; i < n; i++)
			{
				Matrix_D[i] = new double[n];
				for (int j = 0; j < n; j++)
					Matrix_D[i][j] = 0;
			}

		}

		void Matrix_D_clear()
		{
			for (int i = 0; i < n; i++)
			{
				for (int j = 0; j < n; j++)
					Matrix_D[i][j] = 0;
			}
		}

		void Get_Matrix_B_from_sol( NumVarMatrix B, IloCplex cplex)
		{
			for (int i = 0; i < d; i++)
			{
				for (int j = 0; j < d - i; j++)
				{
					Matrix_B[i][j + i] = cplex.getValue(B[i][j]);
				}
			}
		}

		void Print_sol_B(IloEnv env)
		{
			env.out() << " - Solution B: " << endl;

			for (int i = 0; i < d; i++)
			{
				for (int j = 0; j < d; j++)
				{
					env.out() << Matrix_B[i][j] << "\t";
				}
				env.out() << "\n";
			}
			env.out() << endl;
		}

		void Get_Matrix_D_from_sol(NumVarMatrix D, IloCplex cplex)
		{

			for (int i = 0; i < n; i++)
			{
				if (outliers[i] == 0)
				{
					for (int j = 0; j < n; j++)
					{
						if (outliers[j] == 0)
							Matrix_D[i][j] = cplex.getValue(D[i][j]);
					}
				}
			}
		}

		void Set_new_pair_in_D_ij_map(int i, int j)
		{
			int sig = 0;
			int maptemp = 0;
			string strsig;
			sig = i*n + j;
			strsig = to_string(sig);
			maptemp = D_ij_map.size();
			D_ij_map.insert(std::make_pair(maptemp, strsig));
		}
		void Set_new_pair_in_D_ik_map(int i, int j)
		{
			int sig = 0;
			int maptemp = 0;
			string strsig;
			sig = i*n + j;
			strsig = to_string(sig);
			maptemp = D_ik_map.size();
			D_ik_map.insert(std::make_pair(maptemp, strsig));
		}
		void Set_new_pair_in_D_ij_lb_map(int i, int j)
		{
			int sig = 0;
			int maptemp = 0;
			string strsig;
			sig = i*n + j;
			strsig = to_string(sig);
			maptemp = D_ij_lb_map.size();
			D_ij_lb_map.insert(std::make_pair(maptemp, strsig));
		}
		void Set_new_pair_in_D_ij_ub_map(int i, int j)
		{
			int sig = 0;
			int maptemp = 0;
			string strsig;
			sig = i*n + j;
			strsig = to_string(sig);
			maptemp = D_ij_ub_map.size();
			D_ij_ub_map.insert(std::make_pair(maptemp, strsig));
		}

		void Set_B_constraint_17(IloEnv env, IloModel model, NumVarMatrix B, NumVarMatrix B_plus)// Generate constraints linking B and the auxiliary variables as specified in (17)
		{
			for (int k = 0; k < d; k++)
			{
				IloExpr B_plus_temp(env);
				B_plus_temp = B[k][0];
				for (int i = 0; i < k; i++)
				{
					B_plus_temp -= B_plus[i][k - i];
				}

				for (int j = k + 1; j < d; j++)
				{
					B_plus_temp -= B_plus[k][j - k];
				}
				model.add(B_plus_temp >= 0);//Constraints 17a
				B_plus_temp.end();
				for (int l = k + 1; l < d; l++)
				{
					model.add(B_plus[k][l - k] >= B[k][l - k]);//Constraints 17b
					model.add(B_plus[k][l - k] >= -B[k][l - k]);//Constraints 17c
					model.add(B_plus[k][l - k] >= 0);//Constraints 17d
				}

			}

		}

		void Set_D_constraint(IloEnv env, IloModel model, IloNumVarArray a, NumVarMatrix B, NumVarMatrix D)
		{
			for (int i = 0; i < n; i++)
			{
				if (outliers[i] == 0)
				{
					for (int j = 0; j < n; j++)
					{
						if (outliers[j] == 0)
						{
							IloExpr D_ij_temp(env);
							for (int k = 0; k < d; k++)
							{
								if (include_first_order_terms)
								{
									D_ij_temp += fabs(features[i][k] - features[j][k]) * a[k];
								}
								D_ij_temp += (features[i][k] - features[j][k]) * (features[i][k] - features[j][k]) * B[k][0];
							}
							for (int p = 0; p < d - 1; p++)
							{
								for (int l = p + 1; l < d; l++)
								{
									D_ij_temp += 2 * (features[i][p] - features[j][p])* (features[i][l] - features[j][l]) * B[p][l - p];
								}
							}
							model.add(D[i][j] == D_ij_temp);
							D_ij_temp.end();
						}
					}
				}
			}

		}

		void Find_Max_epsilon()
		{
			IloEnv env;

			try {
				//definition of variables
				IloModel model(env, "maxeps");
				IloNumArray labels(env, n);
				for (int i = 0; i < n; i++)
				{

					labels[i] = labels_raw[i];

				}
				////////////define vector a;
				IloNumVarArray a(env, d, -IloInfinity, IloInfinity, ILOFLOAT);
				////////////define Matrix B:
				NumVarMatrix B(env, d);
				if (include_second_order_terms)
				{
					for (int i = 0; i < d; i++)
					{
						B[i] = (IloNumVarArray(env, d - i, -IloInfinity, IloInfinity, ILOFLOAT));//// define half top-right of the matrix B without overdefine variables
					}
				}

				if (enforce_diagonal_dominance && include_second_order_terms)
				{
					// Generate auxiliary variables as stated 
					NumVarMatrix B_plus(env, d);
					for (int i = 0; i < d; i++)
					{
						B_plus[i] = (IloNumVarArray(env, d - i, -IloInfinity, IloInfinity, ILOFLOAT));
					}

					// Generate constraints linking B and the auxiliary variables as specified in (17)
					DistanceMetricLearner::Set_B_constraint_17(env,model, B, B_plus);

				}


				NumVarMatrix D(env, n);
				for (int i = 0; i < n; i++)
				{
					D[i] = (IloNumVarArray(env, n, 0.0, 1.0, ILOFLOAT));
				}
				IloNumVar Max_Epsilon(env, 0, IloInfinity);

				//Constraints:

				/////////////////////////////////////////////////////////Method without 3_D_Matrix. We can just put expressions into the constraints.

				DistanceMetricLearner::Set_D_constraint(env ,model, a, B, D);
				
				

				/////////////////////////////////////////////////////////Method without 3_D_Matrix.end();



				//Main constraint
				for (int i = 0; i < n; i++)
				{
					if (outliers[i] == 0)
					{
						for (int k = 0; k < n; k++)
						{
							if (outliers[k] == 0)
							{
								if (labels[i] != labels[k])
								{
									model.add(Max_Epsilon <= D[i][k]);
								}
							}
						}
					}
				}

				//OBJ
				IloExpr obj(env);
				obj = Max_Epsilon;
				model.add(IloMaximize(env, obj));
				obj.end();

				//solve
				IloCplex cplex(env);
				cplex.extract(model);
				cplex.exportModel("maxeps.lp");
				cplex.solve();

				//output


				///////////get B

				DistanceMetricLearner::Initialize_Matrix_B();

				DistanceMetricLearner::Get_Matrix_B_from_sol(B,cplex);

				DistanceMetricLearner::Print_sol_B(env);

				//////////get D_ij
				DistanceMetricLearner::Initialize_Matrix_D();

				DistanceMetricLearner::Get_Matrix_D_from_sol(D, cplex);

				///print max epsilon
				cplex.out() << "Objective value epsilon = " << cplex.getObjValue() << endl;
				Maxi_epsilon = cplex.getObjValue();

			}
			catch (IloException& ex) {
				cerr << "Error: " << ex << endl;
			}

			env.end();


		}

		void learn_metric_LP()
		{
			IloEnv env;
			try {
				//definition of variables
				IloModel model(env, "LP");
				IloNumVarArray t(env, n, 0, IloInfinity, ILOFLOAT);
				IloNumArray labels(env, n);
				for (int i = 0; i < n; i++)
				{

					labels[i] = labels_raw[i];

				}

				////////////define vector a;
				IloNumVarArray a(env, d, -IloInfinity, IloInfinity, ILOFLOAT);

				////////////define matrix B;
				NumVarMatrix B(env, d);
				if (include_second_order_terms)
				{
					for (int i = 0; i < d; i++)
					{;
						B[i] = (IloNumVarArray(env, d-i, -IloInfinity, IloInfinity, ILOFLOAT));//// define half top-right of the matrix B without overdefine variables
					}
				}

				if (enforce_diagonal_dominance && include_second_order_terms) 
				{
					// Generate auxiliary variables as stated 
					NumVarMatrix B_plus(env, d);
					for (int i = 0; i < d; i++)
					{
						B_plus[i] = (IloNumVarArray(env, d - i, -IloInfinity, IloInfinity, ILOFLOAT));
					}

					// Generate constraints linking B and the auxiliary variables as specified in (17)
					DistanceMetricLearner::Set_B_constraint_17(env, model, B, B_plus);
				}

				NumVarMatrix D(env, n);
				for (int i = 0; i < n; i++)
				{
					D[i] = (IloNumVarArray(env, n, 0.0, 1.0, ILOFLOAT));
				}

				//Constraints:


				/*///////////////////////////////////////////////////////////////////////Method with 3_D_Matrix_Delta;//
				//Constraint: d_ij_as_function_of_features_and_B
				//define Delta[n][n][d]:
				Num3Matrix Delta(env, n);
				for (int i = 0; i < n; i++)
				{
				Delta[i] = NumMatrix(env, n);

				for (int j = 0; j < n; j++)
				{
				Delta[i][j] = IloNumArray(env, d);

				for (int k = 0; k < d; k++)
				{
				Delta[i][j][k] = features[i][k] - features[j][k];
				cout << Delta[i][j][k] << endl;
				}
				}
				}


				for (int i = 0; i < n; i++)
				{
				for (int j = 0; j < n; j++)
				{
				IloExpr D_ij_temp(env);
				for (int k = 0; k < d; k++)
				{
				D_ij_temp += Delta[i][j][k] * Delta[i][j][k]*B[k][0];
				}
				for (int p = 0; p < d-1; p++)
				{
				for (int l = p+1; l < d; l++)
				{
				D_ij_temp += 2 * Delta[i][j][p] * Delta[i][j][l] * B[p][l-p];
				}
				}
				model.add(D[i][j] == D_ij_temp);
				D_ij_temp.end();
				}
				}*/
				//////////////////////////////////////////////////////////////////////////Method with 3_D_Matrix_Delta.end();




				/////////////////////////////////////////////////////////Method without 3_D_Matrix. We can just put expressions into the constraints.

				DistanceMetricLearner::Set_D_constraint(env, model, a, B, D);

				/////////////////////////////////////////////////////////Method without 3_D_Matrix.end();



				//Main constraint
				//(1):
				for (int i = 0; i < n; i++)
				{
					if (outliers[i] == 0)
					{
						for (int k = 0; k < n; k++)
						{
							if ((labels[i] != labels[k]) && (outliers[k] == 0))
							{
								model.add(t[i] + epsilon <= D[i][k]);
							}
						}
					}
				}

				//(2)
				for (int i = 0; i < n; i++)
				{
					if (outliers[i] == 0)
					{
						for (int j = 0; j < n; j++)
						{
							if ((labels[i] == labels[j]) && (i != j) && (outliers[j] == 0))
							{
								model.add(t[i] <= D[i][j]);
							}
						}
					}
				}

				//OBJ
				IloExpr obj(env);

				for (int i = 0; i < n; i++)
				{
					if (outliers[i] == 0)
						obj += t[i];
				}

				model.add(IloMaximize(env, obj));
				obj.end();

				//solve
				IloCplex cplex(env);
				cplex.extract(model);
				cplex.exportModel("LP.lp");
				cplex.solve();

				//output

				///////////get B
				DistanceMetricLearner::Initialize_Matrix_B();

				DistanceMetricLearner::Get_Matrix_B_from_sol(B, cplex);

				DistanceMetricLearner::Print_sol_B(env);


				//////////get D_ij

				DistanceMetricLearner::Initialize_Matrix_D();

				DistanceMetricLearner::Get_Matrix_D_from_sol(D, cplex);


				/////////get Obj
				cplex.out() << "Objective value = " << cplex.getObjValue() << endl;


			}
			catch (IloException& ex) {
				cerr << "Error: " << ex << endl;
			}

			env.end();

		}


		void learn_metric_LP_fast(bool erase_map)
		{
			IloEnv env;
			try {
				//definition of variables
				IloModel model(env, "LP_fast");
				IloNumVarArray t(env, n, 0, IloInfinity, ILOFLOAT);
				IloNumArray labels(env, n);
				for (int i = 0; i < n; i++)
				{

					labels[i] = labels_raw[i];

				}

				////////////define vector a;
				IloNumVarArray a(env, d, -IloInfinity, IloInfinity, ILOFLOAT);

				////////////define matrix B;
				NumVarMatrix B(env, d);
				if (include_second_order_terms)
				{
					for (int i = 0; i < d; i++)
					{
						B[i] = (IloNumVarArray(env, d - i, -IloInfinity, IloInfinity, ILOFLOAT));//// define half top-right of the matrix B without overdefine variables
					}
				}

				if (enforce_diagonal_dominance && include_second_order_terms)
				{
					// Generate auxiliary variables as stated 
					NumVarMatrix B_plus(env, d);
					for (int i = 0; i < d; i++)
					{
						B_plus[i] = (IloNumVarArray(env, d - i, -IloInfinity, IloInfinity, ILOFLOAT));
					}

					// Generate constraints linking B and the auxiliary variables as specified in (17)
					DistanceMetricLearner::Set_B_constraint_17(env, model, B, B_plus);
				}

				////////////define vector D;
				IloNumVarArray D_ij_array(env);
				IloNumVarArray D_ik_array(env);
				IloNumVarArray D_array_ub(env);
				IloNumVarArray D_array_lb(env);

				///initialization of iterations
				double threshold = 0.00000001;

				double *t_sol;
				t_sol = new double[n];


				///set B as Euclidean distance
				DistanceMetricLearner::Initialize_Matrix_B();
				DistanceMetricLearner::Set_Euclidean_Matrix_B();



				//initialize D_start
				DistanceMetricLearner::Set_Matrix_D_with(Matrix_B);

				
				///Set initial contraints d_ij

				for (int i = 0; i < n; i++)
				{
				DistanceMetricLearner::Calculate_min_D_ij_without_O(i);
				DistanceMetricLearner::Set_new_pair_in_D_ij_map(i_p, j_p);
				D_ij_array.add(IloNumVar(env, -IloInfinity, IloInfinity, ILOFLOAT));
				int ttt = D_ij_map.size() ;
				DistanceMetricLearner::Set_D_ij_Constraint_map(env, model, a, B, D_ij_array, D_ij_map.size()-1, i_p, j_p);
				model.add(t[i] <= D_ij_array[D_ij_map.size() - 1]);

				
				///Set initial contraints d_ik
				DistanceMetricLearner::Calculate_min_D_ik_without_O(i);
				DistanceMetricLearner::Set_new_pair_in_D_ik_map(i_p, k_p);
				D_ik_array.add(IloNumVar(env, -IloInfinity, IloInfinity, ILOFLOAT));
				DistanceMetricLearner::Set_D_ij_Constraint_map(env, model, a, B, D_ik_array, D_ik_map.size()-1, i_p, k_p);
				model.add(t[i]+ epsilon <= D_ik_array[D_ik_map.size() - 1]);


				///Set initial lower bound d_ij
				DistanceMetricLearner::Find_min_D_ij_without_O(i);
				DistanceMetricLearner::Set_new_pair_in_D_ij_lb_map(i_p, j_p);

				D_array_lb.add(IloNumVar(env, 0, IloInfinity, ILOFLOAT));
				DistanceMetricLearner::Set_D_ij_Constraint_map(env, model, a, B, D_array_lb, D_ij_lb_map.size()-1, i_p, j_p);
				
				///Set initial upper bound d_ij
				DistanceMetricLearner::Find_max_D_ij_without_O(i);
				DistanceMetricLearner::Set_new_pair_in_D_ij_ub_map(i_p, j_p);

				D_array_ub.add(IloNumVar(env, -IloInfinity, 1, ILOFLOAT));
				DistanceMetricLearner::Set_D_ij_Constraint_map(env, model, a, B, D_array_ub, D_ij_ub_map.size()-1, i_p, j_p);

				}


				//OBJ
				IloExpr exp(env);

				for (int i = 0; i < n; i++)
				{
					if (outliers[i] == 0)
						exp += t[i];
				}

				IloObjective obj = IloMaximize(env, exp);
				model.add(obj);
				exp.end();

				//solve
				IloCplex cplex(env);
				cplex.extract(model);
				cplex.exportModel("LP_fast.lp");
				cplex.solve();




				bool flag = 0;
				///////////////////////////////////start iteration:
				for (;;)
				{
					flag = 1;
					///get B* and ti*
					DistanceMetricLearner::Get_Matrix_B_from_sol(B, cplex);

					for (int i = 0; i < n; i++)
					{
						t_sol[i] = 0;
						if (outliers[i] == 0)
							t_sol[i] = cplex.getValue(t[i]);
					}




					///calculate new D_ij

					DistanceMetricLearner::Matrix_D_clear();
					DistanceMetricLearner::Set_Matrix_D_with(Matrix_B);

					///check violated constraints

					//V0
					for (int i = 0; i < n; i++)
					{
						if (outliers[i] == 0)
						{
							temp_priv = -999999;
							for (int j = 0; j < n; j++)
							{
								if ((i != j) && (outliers[j] == 0) && (labels_raw[i] == labels_raw[j]))
								{
									if ((temp_priv < t_sol[i] - Matrix_D[i][j]) && (1 - DistanceMetricLearner::Find_in_Map(i, j, D_ij_map)))
									{
										temp_priv = t_sol[i] - Matrix_D[i][j];
										i_p = i; j_p = j;
									}
								}
							}

							if (temp_priv > threshold)
							{
								DistanceMetricLearner::Set_new_pair_in_D_ij_map(i_p, j_p );
								D_ij_array.add(IloNumVar(env, -IloInfinity, IloInfinity, ILOFLOAT));
								DistanceMetricLearner::Set_D_ij_Constraint_map(env, model, a, B, D_ij_array, D_ij_map.size()-1, i_p, j_p);
								model.add(t[i] <= D_ij_array[D_ij_map.size() - 1]);

								flag = 0;
							}

							//V1
							temp_priv = -999999;
							for (int k = 0; k < n; k++)
							{
								if ((outliers[k] == 0) && (labels_raw[i] != labels_raw[k]))
								{
									if ((temp_priv < t_sol[i] + epsilon - Matrix_D[i][k]) && (1 - DistanceMetricLearner::Find_in_Map(i, k, D_ik_map)))
									{
										temp_priv = t_sol[i] + epsilon - Matrix_D[i][k];
										i_p = i; k_p = k;
									}
								}
							}

							if (temp_priv > threshold)

							{
								DistanceMetricLearner::Set_new_pair_in_D_ik_map(i_p, k_p);
								D_ik_array.add(IloNumVar(env, -IloInfinity, IloInfinity, ILOFLOAT));
								DistanceMetricLearner::Set_D_ij_Constraint_map(env, model, a, B, D_ik_array, D_ik_map.size()-1, i_p, k_p);
								model.add(t[i] + epsilon <= D_ik_array[D_ik_map.size() - 1]);

								flag = 0;
							}

							
							//V2:lower bound

							temp_priv = 999999;
							for (int j = 0; j < n; j++)
							{
								if ((i != j) && (outliers[j] == 0))
								{
									if ((temp_priv > Matrix_D[i][j]) && (1 - DistanceMetricLearner::Find_in_Map(i, j, D_ij_lb_map)))
									{
										temp_priv = Matrix_D[i][j];
										i_p = i; j_p = j;
									}
								}
							}

							if (temp_priv < 0 - threshold)
							{
								DistanceMetricLearner::Set_new_pair_in_D_ij_lb_map(i_p, j_p);

								D_array_lb.add(IloNumVar(env, 0, IloInfinity, ILOFLOAT));
								DistanceMetricLearner::Set_D_ij_Constraint_map(env, model, a, B, D_array_lb, D_ij_lb_map.size()-1, i_p, j_p);

								flag = 0;
							}


							//V3:upper bound

							temp_priv = -999999;
							for (int j = 0; j < n; j++)
							{
								if ((i != j) && (outliers[j] == 0))
								{
									if ((temp_priv < Matrix_D[i][j]) && (1 - DistanceMetricLearner::Find_in_Map(i, j, D_ij_ub_map)))
									{
										temp_priv = Matrix_D[i][j];
										i_p = i; j_p = j;
									}
								}
							}

							if (temp_priv > 1 + threshold)
							{

								DistanceMetricLearner::Set_new_pair_in_D_ij_ub_map(i_p, j_p);

								D_array_ub.add(IloNumVar(env, -IloInfinity, 1, ILOFLOAT));
								DistanceMetricLearner::Set_D_ij_Constraint_map(env, model, a, B, D_array_ub, D_ij_ub_map.size()-1, i_p, j_p);
								flag = 0;
							}


						}
					}


					if (flag != 0)
					{
						break;
					}

					///modify obj in each iteration
					/*
					model.remove(obj);
					IloExpr newexp(env);
					for (int i = 0; i < n; i++)
					{
					if (outliers[i] == 0)
					newexp += t[i];
					}

					obj = IloMaximize(env, newexp);
					model.add(obj);
					newexp.end();
					*/

					///re_solve the model
					cplex.extract(model);
					cplex.exportModel("LP_fast.lp");
					cplex.solve();




				}

				/////// final output

				//get Obj
				cplex.out() << "Objective value = " << cplex.getObjValue() << endl;

				//get Matrix_B
				DistanceMetricLearner::Get_Matrix_B_from_sol(B, cplex);
				DistanceMetricLearner::Print_sol_B(env);
				//get outliers
				//DistanceMetricLearner::Print_outliers();


				if (erase_map)
				{
					D_ij_map.erase(D_ij_map.begin(), D_ij_map.end());
					D_ik_map.erase(D_ik_map.begin(), D_ik_map.end());
					D_ij_ub_map.erase(D_ij_ub_map.begin(), D_ij_ub_map.end());
					D_ij_lb_map.erase(D_ij_lb_map.begin(), D_ij_lb_map.end());

				}




				////release dynamic memory
				delete[]t_sol;
				/*delete[]O_alleged;

				*/

			}
			catch (IloException& ex) {
				cerr << "Error: " << ex << endl;
			}

			env.end();



		}
		void learn_metric_LP_fast_algorithm2()
		{
			IloEnv env;
			try {
				//definition of variables
				IloModel model(env, "LP_fast");
				IloNumVarArray t(env, n, 0, 1, ILOFLOAT);
				IloNumArray labels(env, n);
				for (int i = 0; i < n; i++)
				{

					labels[i] = labels_raw[i];

				}

				////////////define vector a;
				IloNumVarArray a(env, d, -IloInfinity, IloInfinity, ILOFLOAT);

				////////////define matrix B;
				NumVarMatrix B(env, d);
				if (include_second_order_terms)
				{
					for (int i = 0; i < d; i++)
					{
						;
						B[i] = (IloNumVarArray(env, d - i, -IloInfinity, IloInfinity, ILOFLOAT));//// define half top-right of the matrix B without overdefine variables
					}
				}

				if (enforce_diagonal_dominance && include_second_order_terms)
				{
					// Generate auxiliary variables as stated 
					NumVarMatrix B_plus(env, d);
					for (int i = 0; i < d; i++)
					{
						B_plus[i] = (IloNumVarArray(env, d - i, -IloInfinity, IloInfinity, ILOFLOAT));
					}

					// Generate constraints linking B and the auxiliary variables as specified in (17)
					for (int k = 0; k < d; k++)
					{
						IloExpr B_plus_temp(env);
						B_plus_temp = B[k][0];
						for (int i = 0; i < k; i++)
						{
							B_plus_temp -= B_plus[i][k - i];
						}

						for (int j = k + 1; j < d; j++)
						{
							B_plus_temp -= B_plus[k][j - k];
						}
						model.add(B_plus_temp >= 0);//Constraints 17a
						B_plus_temp.end();
						for (int l = k + 1; l < d; l++)
						{
							model.add(B_plus[k][l - k] >= B[k][l - k]);//Constraints 17b
							model.add(B_plus[k][l - k] >= -B[k][l - k]);//Constraints 17c
							model.add(B_plus[k][l - k] >= 0);//Constraints 17d
						}

					}
				}

				////////////define matrix D;
				NumVarMatrix D(env, n);
				for (int i = 0; i < n; i++)
				{
					D[i] = (IloNumVarArray(env, n, -IloInfinity, IloInfinity, ILOFLOAT));
				}

				for (int i = 0; i < n; i++)
				{
					if (outliers[i] == 0)
					{
						for (int j = 0; j < n; j++)
						{
							if (outliers[j] == 0)
							{
								IloExpr D_ij_temp(env);
								for (int k = 0; k < d; k++)
								{
									if (include_first_order_terms)
									{
										D_ij_temp += fabs(features[i][k] - features[j][k]) * a[k];
									}

									D_ij_temp += (features[i][k] - features[j][k]) * (features[i][k] - features[j][k]) * B[k][0];
								}
								for (int p = 0; p < d - 1; p++)
								{
									for (int l = p + 1; l < d; l++)
									{
										D_ij_temp += 2 * (features[i][p] - features[j][p])* (features[i][l] - features[j][l]) * B[p][l - p];
									}
								}
								model.add(D[i][j] == D_ij_temp);
								D_ij_temp.end();
							}
						}
					}
				}


				///initialization of iterations
				double threshold = 0.00000001;
				Matrix_B_bool = 1;
				Matrix_B = new double*[d];
				for (int i = 0; i < d; i++)
					Matrix_B[i] = new double[d];

				for (int i = 0; i < d; i++)
				{
					for (int j = 0; j < d; j++)
					{
						Matrix_B[i][j] = 0;
					}
				}

				Matrix_D_bool = 1;
				Matrix_D = new double*[n];
				for (int i = 0; i < n; i++)
					Matrix_D[i] = new double[n];

				double *t_sol;
				t_sol = new double[n];
				R_bool = 1;
				R = new double[n];

				int *O_alleged;
				O_alleged = new int[n];

				int ** V0_0;
				V0_0 = new int*[n];
				for (int i = 0; i < n; i++)
					V0_0[i] = new int[n];
				for (int i = 0; i < n; i++)
				{
					for (int j = 0; j < n; j++)
						V0_0[i][j] = 0;
				}



				int ** V1_0;
				V1_0 = new int*[n];
				for (int i = 0; i < n; i++)
					V1_0[i] = new int[n];
				for (int i = 0; i < n; i++)
				{
					for (int j = 0; j < n; j++)
						V1_0[i][j] = 0;
				}



				int ** V2_0;
				V2_0 = new int*[n];
				for (int i = 0; i < n; i++)
					V2_0[i] = new int[n];
				for (int i = 0; i < n; i++)
				{
					for (int j = 0; j < n; j++)
						V2_0[i][j] = 0;
				}



				int ** V3_0;
				V3_0 = new int*[n];
				for (int i = 0; i < n; i++)
					V3_0[i] = new int[n];
				for (int i = 0; i < n; i++)
				{
					for (int j = 0; j < n; j++)
						V3_0[i][j] = 0;
				}





				///set B as Euclidean distance

				//initialize B_start
				for (int i = 0; i < d; i++)
				{
					for (int j = 0; j < d; j++)
					{
						if (i == j)
							Matrix_B[i][j] = 1;
						else
							Matrix_B[i][j] = 0;
					}
				}

				//initialize D_start
				for (int i = 0; i < n; i++)
				{
					for (int j = 0; j < n; j++)
						Matrix_D[i][j] = 0;

				}
				for (int i = 0; i < n; i++)
				{
					for (int j = 0; j < n; j++)
					{
						if (i != j)
						{
							for (int k = 0; k < d; k++)
							{
								Matrix_D[i][j] += (features[i][k] - features[j][k]) * (features[i][k] - features[j][k]) * Matrix_B[k][k];
							}
							for (int p = 0; p < d - 1; p++)
							{
								for (int l = p + 1; l < d; l++)
								{
									Matrix_D[i][j] += 2 * (features[i][p] - features[j][p])* (features[i][l] - features[j][l]) * Matrix_B[p][l];
								}
							}
						}
					}
				}

				//detect first outliers
				Detect_Outliers();



				///Set initial contraints d_ij
				double temp;
				int ii, jj, kk;
				for (int i = 0; i < n; i++)
				{
					temp = 999;
					if (outliers[i] == 0)
					{
						for (int j = 0; j < n; j++)
						{
							if (outliers[j] == 0)
							{
								if ((i != j) && (labels_raw[i] == labels_raw[j]) && (temp>Matrix_D[i][j]))
								{
									temp = Matrix_D[i][j];
									ii = i;
									jj = j;
								}
							}
						}
						model.add(t[i] <= D[ii][jj]);
						V0_0[ii][jj] = 1;
					}
				}


				///Set initial contraints d_ik
				for (int i = 0; i < n; i++)
				{
					temp = 999;
					if (outliers[i] == 0)
					{
						for (int k = 0; k < n; k++)
						{
							if (outliers[k] == 0)
							{
								if ((labels_raw[i] != labels_raw[k]) && (temp>Matrix_D[i][k]))
								{
									temp = Matrix_D[i][k];
									ii = i;
									kk = k;
								}
							}
						}
						model.add(t[i] + epsilon <= D[ii][kk]);
						V1_0[ii][kk] = 1;
					}
				}

				///Set initial lower bound d_ij
				for (int i = 0; i < n; i++)
				{
					temp = 999;
					if (outliers[i] == 0)
					{
						for (int j = 0; j < n; j++)
						{
							if (outliers[j] == 0)
							{
								if ((i != j) && (temp>Matrix_D[i][j]))
								{
									temp = Matrix_D[i][j];
									ii = i;
									jj = j;
								}
							}
						}
						model.add(0 <= D[ii][jj]);
						V2_0[ii][jj] = 1;
					}
				}

				///Set initial upper bound d_ij
				for (int i = 0; i < n; i++)
				{
					temp = -999;
					if (outliers[i] == 0)
					{
						for (int j = 0; j < n; j++)
						{
							if (outliers[j] == 0)
							{
								if ((i != j) && (temp<Matrix_D[i][j]))
								{
									temp = Matrix_D[i][j];
									ii = i;
									jj = j;
								}
							}
						}
						model.add(1 >= D[ii][jj]);
						V3_0[ii][jj] = 1;
					}
				}


				for (int i = 0; i < n; i++)
				{
					for (int j = 0; j < n; j++)
					{
						if (i != j)
						{
							if (V0_0[i][j] == 1)
								model.add(t[i] <= D[i][j]);
							if (V1_0[i][j] == 1)
								model.add(t[i] + epsilon <= D[i][j]);
							if (V2_0[i][j] == 1)
								model.add(t[i] <= D[i][j]);
							if (V3_0[i][j] == 1)
								model.add(t[i] <= D[i][j]);
						}
					}
				}



				//OBJ
				IloExpr exp(env);

				for (int i = 0; i < n; i++)
				{
					if (outliers[i] == 0)
						exp += t[i];
				}

				IloObjective obj = IloMaximize(env, exp);
				model.add(obj);
				exp.end();

				//solve
				IloCplex cplex(env);
				cplex.extract(model);
				cplex.exportModel("LP_fast.lp");
				cplex.solve();
				///////////////////////////////////////////////////////////////////////////////// testing output

				//get Obj
				cplex.out() << "Objective value = " << cplex.getObjValue() << endl;

				//get Matrix_B
				for (int i = 0; i < d; i++)
				{
					for (int j = 0; j < d - i; j++)
					{
						Matrix_B[i][j + i] = cplex.getValue(B[i][j]);
					}
				}
				env.out() << " - Solution B: " << endl;

				for (int i = 0; i < d; i++)
				{
					for (int j = 0; j < d; j++)
					{
						env.out() << Matrix_B[i][j] << "\t";
					}
					env.out() << "\n";
				}
				env.out() << endl;

				//get outliers
				cout << "outliers:" << endl;
				for (int i = 0; i < n; i++)
				{
					if (outliers[i] == 1)
						cout << i << "\t";
				}
				cout << endl;

				for (int i = 0; i < n; i++)
				{
					t_sol[i] = 0;
					if (outliers[i] == 0)
						t_sol[i] = cplex.getValue(t[i]);
				}

				cout << "t_sol:" << endl;
				for (int i = 0; i < n; i++)
				{
					cout << t_sol[i] << "\t";
				}
				cout << endl;


				///////////////////////////////////////////////////////////////////////////////// testing output end



				bool flag = 0;
				///////////////////////////////////start iteration:
				for (;;)
				{
					flag = 1;
					///get B* and ti*
					for (int i = 0; i < d; i++)
					{
						for (int j = 0; j < d - i; j++)
						{
							Matrix_B[i][j + i] = cplex.getValue(B[i][j]);
						}
					}

					for (int i = 0; i < n; i++)
					{
						t_sol[i] = 0;
						if (outliers[i] == 0)
							t_sol[i] = cplex.getValue(t[i]);
					}

					////////////////////////////////////////////////////////////test
					cout << "t_sol:" << endl;
					for (int i = 0; i < n; i++)
					{
						cout << t_sol[i] << "\t";
					}
					cout << endl;
					////////////////////////////////////////////////////////////test end



					///calculate new D_ij
					for (int i = 0; i < n; i++)
					{
						for (int j = 0; j < n; j++)
							Matrix_D[i][j] = 0;

					}
					for (int i = 0; i < n; i++)
					{
						for (int j = 0; j < n; j++)
						{
							if (i != j)
							{
								for (int k = 0; k < d; k++)
								{
									Matrix_D[i][j] += (features[i][k] - features[j][k]) * (features[i][k] - features[j][k]) *Matrix_B[k][k];
								}
								for (int p = 0; p < d - 1; p++)
								{
									for (int l = p + 1; l < d; l++)
									{
										Matrix_D[i][j] += 2 * (features[i][p] - features[j][p])* (features[i][l] - features[j][l]) * Matrix_B[p][l];
									}
								}
							}
						}
					}

					/// define O_alleged
					for (int i = 0; i < n; i++)
					{
						O_alleged[i] = 0;
						if (outliers[i] == 0)
						{
							temp = 999999;
							for (int j; j < n; j++)
							{
								if ((V0_0[i][j] == 1) && (i != j))//??????????
								{
									if (temp>Matrix_D[i][j])
									{
										temp = Matrix_D[i][j];
										ii = i;
										jj = j;
									}
								}
							}
							if (temp > 998)
								continue;
							else
							{
								if (t_sol[i]<temp - threshold)
									O_alleged[i] = 1;
							}
						}
					}


					///check violated constraints

					//V0
					for (int i = 0; i < n; i++)
					{
						if (outliers[i] == 0)
						{
							temp = -999999;
							for (int j = 0; j < n; j++)
							{
								if ((i != j) && (outliers[j] == 0) && (labels_raw[i] == labels_raw[j]))
								{
									if ((temp < t_sol[i] - Matrix_D[i][j]) && (V0_0[i][j] == 0))
									{
										temp = t_sol[i] - Matrix_D[i][j];
										ii = i; jj = j;
									}
								}
							}

							if (temp < threshold)
							{
								if (O_alleged[ii] == 1)
								{
									outliers[i] = 1;
								}
							}
							else
							{
								V0_0[ii][jj] = 1;
								model.add(t[ii] <= D[ii][jj]);
								flag = 0;
							}
						}
					}

					//V1
					for (int i = 0; i < n; i++)
					{
						if (outliers[i] == 0)
						{
							temp = -999999;
							for (int k = 0; k < n; k++)
							{
								if ((outliers[k] == 0) && (labels_raw[i] != labels_raw[k]))
								{
									if ((temp < t_sol[i] + epsilon - Matrix_D[i][k]) && (V1_0[i][k] == 0))
									{
										temp = t_sol[i] + epsilon - Matrix_D[i][k];
										ii = i; kk = k;
									}
								}
							}

							if (temp < threshold)
								continue;
							else
							{
								V1_0[ii][kk] = 1;
								model.add(t[ii] + epsilon <= D[ii][kk]);
								flag = 0;
							}
						}
					}

					//V2

					for (int i = 0; i < n; i++)
					{
						if (outliers[i] == 0)
						{
							temp = 999999;
							for (int j = 0; j < n; j++)
							{
								if ((i != j) && (outliers[j] == 0))
								{
									if ((temp > Matrix_D[i][j]) && (V2_0[i][j] == 0))
									{
										temp = Matrix_D[i][j];
										ii = i; jj = j;
									}
								}
							}

							if (temp > 0 - threshold)
							{
								continue;
							}
							else
							{
								V2_0[ii][jj] = 1;
								model.add(0 <= D[ii][jj]);
								flag = 0;
							}
						}
					}

					//V3

					for (int i = 0; i < n; i++)
					{
						if (outliers[i] == 0)
						{
							temp = -999999;
							for (int j = 0; j < n; j++)
							{
								if ((i != j) && (outliers[j] == 0))
								{
									if ((temp < Matrix_D[i][j]) && (V3_0[i][j] == 0))
									{
										temp = Matrix_D[i][j];
										ii = i; jj = j;
									}
								}
							}

							if (temp < 1 + threshold)
							{
								continue;
							}
							else
							{
								V3_0[ii][jj] = 1;
								model.add(1 >= D[ii][jj]);
								flag = 0;
							}
						}
					}


					if (flag != 0)
					{
						break;
					}

					///modify obj in each iteration
					model.remove(obj);
					IloExpr newexp(env);
					for (int i = 0; i < n; i++)
					{
						if (outliers[i] == 0)
							newexp += t[i];
					}

					obj = IloMaximize(env, newexp);
					model.add(obj);
					newexp.end();


					///re_solve the model
					cplex.extract(model);
					cplex.exportModel("LP_fast.lp");
					cplex.solve();
					///////////////////////////////////////////////////////////////////////////////// testing output

					//get Obj
					cplex.out() << "Objective value = " << cplex.getObjValue() << endl;

					//get Matrix_B
					for (int i = 0; i < d; i++)
					{
						for (int j = 0; j < d - i; j++)
						{
							Matrix_B[i][j + i] = cplex.getValue(B[i][j]);
						}
					}
					env.out() << " - Solution B: " << endl;

					for (int i = 0; i < d; i++)
					{
						for (int j = 0; j < d; j++)
						{
							env.out() << Matrix_B[i][j] << "\t";
						}
						env.out() << "\n";
					}
					env.out() << endl;

					//get outliers
					cout << "outliers:" << endl;
					for (int i = 0; i < n; i++)
					{
						if (outliers[i] == 1)
							cout << i << "\t";
					}
					cout << endl;


					cout << "t_sol:" << endl;
					for (int i = 0; i < n; i++)
					{
						cout << t_sol[i] << "\t";
					}
					cout << endl;


					///////////////////////////////////////////////////////////////////////////////// testing output end


					///reinsert outliers(here we use Ri method)
					for (;;)
					{
						//calculate D_ij with outliers
						for (int i = 0; i < n; i++)
						{
							if (outliers[i] == 1)
							{
								for (int j = 0; j < n; j++)
								{
									if (outliers[j] != 1)
									{
										Matrix_D[i][j] = 0;
										for (int k = 0; k < d; k++)
										{
											Matrix_D[i][j] += (features[i][k] - features[j][k]) * (features[i][k] - features[j][k]) * Matrix_B[k][k];
										}
										for (int p = 0; p < d - 1; p++)
										{
											for (int l = p + 1; l < d; l++)
											{
												Matrix_D[i][j] += 2 * (features[i][p] - features[j][p])* (features[i][l] - features[j][l]) * Matrix_B[p][l];
											}
										}
									}
								}
							}
						}
						/////calculate Ri
						for (int i = 0; i < n; i++)
							R[i] = 0;

						double temp, temp2;
						for (int i = 0; i < n; i++)
						{
							temp = 999, temp2 = 999;
							if (outliers[i] == 1)
							{
								for (int j = 0; j < n; j++)
								{
									if (outliers[j] == 0)
									{
										if ((i != j) && (labels_raw[i] != labels_raw[j]) && (temp>Matrix_D[i][j]))
										{
											temp = Matrix_D[i][j];
										}
										if ((i != j) && (labels_raw[i] == labels_raw[j]) && (temp2 > Matrix_D[i][j]))
										{
											temp2 = Matrix_D[i][j];
										}
									}
								}
								R[i] = temp / temp2;
							}
						}

						////reinsert by order, until Ri<1;
						temp = 0;
						ii = 0;
						for (int i = 0; i < n; i++)
						{
							if ((outliers[i] == 1) && (temp < R[i]))
							{
								temp = R[i];
								ii = i;
							}


						}
						if (R[ii]>1)
							outliers[ii] = 0;
						else
							break;

					}
					///////////////////////////////////////////////////////////////////////////////// testing output

					//get Obj
					cplex.out() << "Objective value = " << cplex.getObjValue() << endl;

					//get Matrix_B
					for (int i = 0; i < d; i++)
					{
						for (int j = 0; j < d - i; j++)
						{
							Matrix_B[i][j + i] = cplex.getValue(B[i][j]);
						}
					}
					env.out() << " - Solution B: " << endl;

					for (int i = 0; i < d; i++)
					{
						for (int j = 0; j < d; j++)
						{
							env.out() << Matrix_B[i][j] << "\t";
						}
						env.out() << "\n";
					}
					env.out() << endl;

					//get outliers
					cout << "outliers:" << endl;
					for (int i = 0; i < n; i++)
					{
						if (outliers[i] == 1)
							cout << i << "\t";
					}
					cout << endl;

					///////////////////////////////////////////////////////////////////////////////// testing output end


				}

				/////// final output

				//get Obj
				cplex.out() << "Objective value = " << cplex.getObjValue() << endl;

				//get Matrix_B
				for (int i = 0; i < d; i++)
				{
					for (int j = 0; j < d - i; j++)
					{
						Matrix_B[i][j + i] = cplex.getValue(B[i][j]);
					}
				}
				env.out() << " - Solution B: " << endl;

				for (int i = 0; i < d; i++)
				{
					for (int j = 0; j < d; j++)
					{
						env.out() << Matrix_B[i][j] << "\t";
					}
					env.out() << "\n";
				}
				env.out() << endl;

				//get outliers
				cout << "outliers:" << endl;
				for (int i = 0; i < n; i++)
				{
					if (outliers[i] == 1)
						cout << i << "\t";
				}
				cout << endl;





				////release dynamic memory
				/*delete[]O_alleged;
				delete[]t_sol;
				for (int i = 0; i < d; i++)
				delete[]B_start[i];
				delete[]B_start;
				for (int i = 0; i < n; i++)
				delete[]D_start[i];
				delete[]D_start;
				for (int i = 0; i < n; i++)
				delete[]V0_0[i];
				delete[]V0_0;
				for (int i = 0; i < n; i++)
				delete[]V1_0[i];
				delete[]V1_0;
				for (int i = 0; i < n; i++)
				delete[]V2_0[i];
				delete[]V2_0;
				for (int i = 0; i < n; i++)
				delete[]V3_0[i];
				delete[]V3_0;
				*/

			}
			catch (IloException& ex) {
				cerr << "Error: " << ex << endl;
			}

			env.end();

		}


		void Set_samples_test()
		{
			d = 2;
			n = 20; 

		}

		void learn_metric_loop_v1(double lower_bound, double upper_bound, int loop_num,int reinsert_method)
		{

			outliers_num = new int[loop_num];
			outliers_num_bool = 1;

			epsilon_loop = new double[loop_num];
			epsilon_loop_bool = 1;

			//start loop:
			for (int i = 0; i<loop_num;i++)
			{
				epsilon = lower_bound + i*(upper_bound - lower_bound) / (loop_num - 1);
				DistanceMetricLearner::Reset_Outliers();

				for (;;)
				{
					learn_metric_LP();
					//learn_metric_LP_fast_real();
					Detect_Outliers();
					if (outliers_change_flag == 0)
						break;
				}
				for (;;)
				{
					switch (reinsert_method)
					{
					case 0:
					{
							  reinsert_outliers();
							  break;
					}

					}
					learn_metric_LP();
					//learn_metric_LP_fast_real();
					Detect_Outliers();
					if (outliers_change_flag == 0)
						break;
				}

				epsilon_loop[i] = epsilon;
				outliers_num[i] = 0;
				for (int j = 0; j < n; j++)
				{
					if (outliers[j] != 0)
						outliers_num[i]++;
				}
			}

			/////////////////////////output
			cout << "number of outliers:" << endl;
			for (int i = 0; i < loop_num; i++)
			{
				cout << outliers_num[i] << "\t";
			}
			cout << endl;

			cout << "with paired epsilons:" << endl;
			for (int i = 0; i < loop_num; i++)
			{
				cout << epsilon_loop[i] << "\t";
			}
			cout << endl;


	
		
		
		}

		/*void learn_metric_loop_test()
		{
			Reset_Outliers();
			Set_LP_epsilon();
			for (;;)
			{
				learn_metric_LP_fast_real();
				//learn_metric_LP();
				Detect_Outliers();
				if (outliers_change_flag == 0)
					break;
			}
			for (;;)
			{
				reinsert_outliers();
				learn_metric_LP_fast_real();
				//learn_metric_LP();
				Detect_Outliers();
				if (outliers_change_flag == 0)
					break;
			}


		}*/

};

int main()
{
	DistanceMetricLearner _model;
	double dur;
	clock_t start, end;
	start = clock();
	_model.Read_data("temp.txt");
	
	//_model.Set_LP_dimension();
	//_model.Set_LP_obs();
	_model.Reset_Outliers();
	//_model.learn_metric_loop_v1(0.0001,0.0003,3,0);
	//_model.learn_metric_loop_test();
	//_model.Find_Max_epsilon();
	_model.Set_LP_epsilon();
	//_model.learn_metric_LP();

	//time calculate

	_model.learn_metric_LP_fast(1);//dosomething
	//_model.learn_metric_LP();

	_model.Detect_Outliers();
	//_model.learn_metric_LP();
	/*
	_model.Set_LP_dimension();
	_model.Set_LP_obs();
	_model.Reset_Outliers();
	
	_model.Set_LP_epsilon();
	//_model.reinsert_outliers_MILP();
	//_model.learn_metric_LP();
	//_model.learn_metric_LP_fast_real();
	*/
	//_model.Set_LP_epsilon();
	//_model.learn_metric_LP();
	//_model.learn_metric_LP_fast_real();

	_model.release_dynamic_memory();
	end = clock();
	dur = (double)(end - start);
	printf("Use Time:%f\n", (dur / CLOCKS_PER_SEC));
	//end
	return 0;
}