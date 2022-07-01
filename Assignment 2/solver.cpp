#include <iostream>
#include <vector>
#include <math.h>
#include <fstream>
#include <algorithm>
#include <limits.h>

using namespace std;

// Return
// 1 for Satisfied
// 0 for Unsatisfied
// -1 for Completed
// 2 for Normal

class Formula
{
public:
  vector<vector<int>> literal; // for storing literals, its frequency and the polarity difference

  vector<vector<int>> clauses; // vector to store clauses
  // If literal is positive store it in form of 10n or n+"0" else 10n+1 + n+"1" if literal is negative

  Formula() {}
  Formula(const Formula &f)
  {
    clauses = f.clauses;
    literal = f.literal;
  }
};

void result(Formula &f, int res)
{
  if (res == 1)
  { // If the formula is SATisfiable
    cout << "SAT" << endl;

    for (int i = 0; i < f.literal[0].size(); i++)
    {
      if (f.literal[0][i] != -1)
      {
        cout << pow(-1, f.literal[0][i]) * (i + 1) << " ";
      }
      else
      { // For literals unassigned and can take any value, assign true
        cout << (i + 1) << " ";
      }
    }
    cout << "0" << endl;
  }
  else
  {
    // If the formula comes out to be UnSATisfiable
    cout << "UnSAT" << endl;
  }
}

int transform(Formula &f, int target)
{
  int val_target = f.literal[0][target];
  // 0 is True, 1 if False

  for (int i = 0; i < f.clauses.size(); i++)
  {
    // iterate over the clauses in the formula
    for (int j = 0; j < f.clauses[i].size(); j++)
    {
      // Iterate over the variables in clause

      if ((10 * target + val_target) == f.clauses[i][j])
      {
        // If literal applies with same polarity as it is being tagetted
        // remove the clause from the list
        f.clauses.erase(f.clauses.begin() + i);
        i--;

        if (f.clauses.size() == 0)
        {
          // If no clauses remain, formula is satisfied
          return 1;
        }
        break; // move to the next clause
      }
      else if (f.clauses[i][j] / 10 == target)
      {

        // the literal appears with opposite polarity
        f.clauses[i].erase(f.clauses[i].begin() + j);
        // remove the literal from the clause, as it is false in it
        j--;

        if (f.clauses[i].size() == 0)
        {
          // If the clause is empty the clause is unsatisfiable for now
          return 0;
        }
        break; // move to the next clause
      }
    }
  }

  // Function ends normally
  return 2;
}

/* Applying the unit propagation on the clauses and applying the respective
transformations on the other clauses*/

int uni_prop(Formula &f)
{
  bool found = false; // bool to get if a unit clause is found or not

  if (f.clauses.size() == 0)
  { // No literal, already SATisfied
    return 1;
  }
  do
  {
    found = false;

    for (int i = 0; i < f.clauses.size(); i++)
    {
      if (f.clauses[i].size() == 1)
      { // If clause contains one literal, it is a unit clause
        found = true;
        f.literal[0][f.clauses[i][0] / 10] = f.clauses[i][0] % 10; // Assigning the truth value to the clause
        f.literal[1][f.clauses[i][0] / 10] = -1;                   // Marking the clause as closed

        int res = transform(f, f.clauses[i][0] / 10); // Applying the transformations over all clauses

        if (res == 0 || res == 1)
          return res;

        break; // Check for another open clause
      }
      else if (f.clauses[i].size() == 0)
      {
        return 0; // Empty clause signifies that it is currently unsatisfiable
      }
    }
  } while (found);

  return 2; // Ends normally
}

int Algorithm(Formula f)
{
  int res = uni_prop(f); // perform unit propagation on the formula
  if (res == 1)          // If formula gets satisfies  show the result
  {
    result(f, res);
    return -1;
  }
  else if (res == 0) // If formula isn't satisfied  then return normally
  {
    return 2;
  }
  // find the variable with maximum frequency in f, which will be the next to be
  // assigned a value 
  // Already assigned variables have this field reset to -1 in
  // order to ignore them

  vector <int > ::iterator ptr;
  int maxm=INT_MIN;
  for(vector <int>::iterator i=f.literal[1].begin();i<f.literal[1].end();i++){
      if(*i>=maxm){
          maxm=*i;
          ptr=i;
      }
  }

  vector <int > ::iterator pt=f.literal[1].begin();
  int i=0;
  while(pt!=ptr){
      i++;
      pt++;
  }


  // Aplly loop twice
  // once for true and once for false

  for (int j = 0; j < 2; j++)
  {
    Formula new_f = f; // Copying the formula into other formula

    if (new_f.literal[2][i] > 0)
    {
      // If the positive sign literals are more then assign true first
      new_f.literal[0][i] = j;
    }
    else
    {
      // Else assign negative first
      new_f.literal[0][i] = (j + 1) % 2;
    }
    new_f.literal[1][i] = -1; // Reset the frquency to close the branch

    int transform_result = transform(new_f, i); // Apply the transformations to all the groups

    if (transform_result == 1)
    { // If formula is satisfied then show result and return
      result(new_f, transform_result);
      return -1;
    }
    else if (transform_result == 0)
    { // If formula not satisfied, return normally
      continue;
    }

    int dpll_result = Algorithm(new_f); // Recursive call for the DPLL Algorithm
    if (dpll_result == -1)              // If done then forward the result
    {
      return dpll_result;
    }
  }

  // Ends normally
  return 2;
}

void solve(Formula formula)
{
  int res = Algorithm(formula); // result of DPLL algorithm on the formula
  if (res == 2)
  {
    result(formula, 0);
  }
}

int main()
{
  ios::sync_with_stdio(0);
  cin.tie(0);
  cout.tie(0);

  Formula formula;
  int literal_count;
  int clause_count;

  //----------------------------INPUT-------------------------------------------------------

  string str;

  // Read from the cnf file
  string path;
  cin >> path;
  ifstream cnf_file(path);

  int idx = 0;

  // Use a while loop together with the getline() function to read the file line by line
  while (getline(cnf_file, str))
  {

    if (str[0] == 'c')
      continue;
    else if (str[0] == 'p')
    {
      int i = 6;
      string s = "";
      while (str[i] != ' ')
      {
        s += str[i];
        i++;
      }
      literal_count = stoi(s); // Store the value of literal_count

      s = "";
      while (i != str.length())
      {
        s += str[i];
        i++;
      }
      clause_count = stoi(s); // Store the value of clause_count

      // Resize the vectors on basis of the literal count
      formula.literal.resize(3);
      formula.literal[0].resize(literal_count, -1); // to store the literals
                                                    // // -1 unassigned
                                                    // // 0 True
                                                    // // 1 False

      formula.literal[1].resize(literal_count, 0); // to store the frequency of a literal
      formula.literal[2].resize(literal_count, 0); // to store the polarity difference of a literal
      formula.clauses.resize(clause_count);
    }
    else
    {
      int i = 0;
      string s = "";
      while (i != str.length() - 1)
      {
        if (str[i] == ' ')
        {
          int val = stoi(s);
          s = "";
          if (val > 0)
          {
            string s1 = to_string(val - 1);
            s1 = s1 + "0";
            formula.clauses[idx].push_back(stoi(s1)); // store it in the form n+"0" or 10n

            // increase frequency and sign of the literal
            formula.literal[1][val - 1]++;
            formula.literal[2][val - 1]++;
          }
          else
          {
            string s1 = to_string(-val - 1);
            s1 = s1 + "1";
            formula.clauses[idx].push_back(stoi(s1)); // store it in the form n+"1" or 10n+1

            // increase frequency and sign of the literal
            formula.literal[1][-val - 1]++;
            formula.literal[2][-val - 1]--;
          }
        }
        else
        {
          s += str[i];
        }
        i++;
      }
      idx++;
    }
  }

  // Close the file
  cnf_file.close();

  //-------------------------------pROCESSING FUNCTSION----------------------------------

  cout << "Proccessing the formulas......." << endl;
  solve(formula);
  return 0;
}