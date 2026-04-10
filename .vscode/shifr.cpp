#include <iostream>
#include <windows.h>
#include <random>
#include <string>
#include <locale>

using namespace std;

int k1[]{1,3,6,2,4,5,7,8};
int k2[]{3,1,2,4};
string s{"А ты лох"};
char *s1{new char[10]};
char *s2{new char[10]};
char *s3{new char[10]};
char *s4{new char[10]};
string alph{"ёйцуекенгшщзхъфывапролджэячсмитьбю"};
int l{alph.length()};

void fe(char *mas){
    for (int i=0;mas[i];i++){
    }
}

int main(){
    setlocale(LC_ALL, "Russian");
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    cout << l << endl;
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> distrib(1, 32);
    fe(s1);
    for (int i=0;s1[i];i++){
        cout << s1[i] << " ";
    }
 }