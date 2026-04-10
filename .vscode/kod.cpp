#include <iostream>
#include <windows.h>
#include <random>

using namespace std;

int k1[]{1,3,6,2,4,5};
int k2[]{3,1,2,4};
char s[]{"А ты лох"};
char *s1[]{new char[10]};
char *s2[]{new char[10]};
char *s3[]{new char[10]};
char *s4[]{new char[10]};
char alph[]{"йцукенгшщзхъфывапролджэячсмитьбюё"};

int main(){
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    unsigned seed = time(0);
    mt19937 gen (seed);
    cout << "в" << endl;
    return 0;
}