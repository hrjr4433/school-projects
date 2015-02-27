/***********************************************************************
* Program:
*    Project 2, Sudoku CSP level 2
*    Brother Wayne Boyer, CS490
* Author:
*    Jay Lee
* Summary: 
*         This program read a file and display as the Sudoku table.
*         Then it solves the sudoku with CSP and backtracking.
* variable = each cells in sudoku table
* domain = {1 ... 9}
* constraint = no same number on a horizontal line, 
*              no same number on a vertical line, 
*              no same number on a sub-square (3 X 3)
************************************************************************/
#include <string.h>
#include <iostream>
#include <cctype>
#include <cstdlib>
#include <fstream>
#include <vector>
using namespace std;

class CELL {
public:
  int value;
  int row;
  int column;
  bool readOnly;
  vector < int > possible_values;
  
  void remove_poss (int value)
  {
    for (int i = 0; i < possible_values.size(); i++)
      if (possible_values[i] == value)
        possible_values.erase(possible_values.begin() + i);
  }
  
  void add_poss (int value) 
  {
    bool found = false;
    for (int i = 0; i < possible_values.size(); i++)
      if (possible_values[i] == value)
        found = true;
    if (!found)
      possible_values.push_back(value);
  }
  
};

CELL solution[9][9];
int num_sol = 0;
vector < CELL* > sorted_list;

bool readFile(char* fileName, CELL sudoku[][9]);
bool checkRules(CELL sudoku[][9], int dummy, int i, int j);
void displayTable(CELL sudoku[][9]);
void solveAnySudoku(CELL sudoku[][9], int mrv_index);

/**********************************************************************
* main function. it reads file and solve the sudoku, then display it.
***********************************************************************/
int main(int argc, char** argv)
{
  char fileName[256];
  CELL sudoku[9][9];
  
  if (argc >= 2)
    strcpy(fileName, argv[1]);
  else
  {
     cout << "Usage: " << argv[0] << " FILE_NAME\n";
     exit(-1);
  }
  
  if (readFile(fileName, sudoku))
  {
    solveAnySudoku(sudoku, 0);
    if (num_sol > 0)
    {
      displayTable(solution);
      cout << "The total number of solution: " << num_sol << endl;
    }
    else
      cout << "No Solution\n";
  }
  else
  {
    cout << "File does not exist or corrupted\n";
    exit(-1);
  }
  
  return 0;
}

/**********************************************************************
* readFile reads a file and populate the sudoku board
***********************************************************************/
bool readFile(char* fileName, CELL sudoku[][9])
{
  char buffer;
  
  ifstream fin(fileName);
  if (fin.fail())
  {
    fin.close();
    return 0;
  }

  for (int i = 0;i < 9;i++)
    for (int j = 0;j < 9;j++)
    {
      fin >> buffer;
      
      if (isdigit(buffer) && buffer > '0' && buffer <= '9')
      {
        sudoku[i][j].value = (int)(buffer - '0');
        sudoku[i][j].row = i;
        sudoku[i][j].column = j; 
        sudoku[i][j].readOnly = true;
      }
      else
      {
        sudoku[i][j].value = 0;
        sudoku[i][j].row = i;
        sudoku[i][j].column = j;
        sudoku[i][j].readOnly = false;
      }
    }
  
  for (int i = 0;i < 9;i++)
    for (int j = 0;j < 9;j++)
    {
      if (!sudoku[i][j].readOnly)
      {
        for (int k = 1; k < 10; k++)
          if (checkRules(sudoku, k, i, j))
            sudoku[i][j].add_poss(k);
      
        int current_size = sorted_list.size();        
        for (int k = 0;k < current_size;k++)
          if (sudoku[i][j].possible_values.size() < sorted_list[k]->possible_values.size())
          {
            sorted_list.insert(sorted_list.begin() + k, &sudoku[i][j]);
            break;
          }
         
        if (current_size == sorted_list.size())
          sorted_list.push_back(&sudoku[i][j]);
      }
    }
  
  if (fin.fail())
  {
    fin.close();
    return 0;
  }

  fin.close();
  return 1;
}

/**********************************************************************
* displayTable displays the sudoku table
***********************************************************************/
void displayTable(CELL sudoku[][9])
{
  for (int i = 0;i < 9;i++)
  {
    for (int j = 0;j < 9;j++)
    {
      cout << sudoku[i][j].value;
  
      if (j == 8)
        cout << endl;
    }
  }
}


/**********************************************************************
* check constraints(vertical, horizontal, and sub square).
***********************************************************************/
bool checkRules(CELL sudoku[][9], int dummy, int i, int j)
{
  int a = i;
  int b = j;

  bool check = true;
  // line constraint
  for (int line = 0;line < 9;line++)
    if (sudoku[i][line].value == dummy && dummy != 0 && line != j)
      check = false;
      
  // column constraint
  for (int column = 0;column < 9;column++)
    if (sudoku[column][j].value == dummy && dummy != 0 && column != i)
      check = false;

  i /= 3;
  i *= 3;
  j /= 3;
  j *= 3;

  // subsqure constraint
  for (int k = 0;k < 3;k++)
    for (int h = 0;h < 3;h++)
    {
      if (sudoku[i + k][j + h].value == dummy && dummy != 0
         && ((i + k) != a && (j + h) != b))
        check = false;
    }
  return check;
}


/**********************************************************************
* solveAnySudoku solves sudoku using constraints and possible values.
* This program using 'backtracking with MRV'.
***********************************************************************/
void solveAnySudoku(CELL sudoku[][9], int mrv_index)
{
  if (mrv_index == sorted_list.size()) //after done, set the success true, break the function
  {
    for(int i = 0; i < 9; i++)
      for(int j = 0; j < 9; j++)
        solution[i][j] = sudoku[i][j];
    num_sol++;
    return;
  }

  CELL* p = sorted_list[mrv_index];
  
  for (int i = 0;i < p->possible_values.size();i++)//use the possibility
  {
    int value = p->possible_values[i];
    if (checkRules(sudoku, value, p->row, p->column))
      p->value = value;
    else
      continue; 

    solveAnySudoku(sudoku, mrv_index + 1);
  }
  
  p->value = 0;//set the previous value to 0
  return;
  
}