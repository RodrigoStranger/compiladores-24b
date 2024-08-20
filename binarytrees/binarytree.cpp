#include <iostream>
#include <string>

using namespace std;

class Nodo {
public:
    int key;
    string data;
    Nodo* left;
    Nodo* right;
    
    Nodo(int key, string data) {
        this->key=key;
        this->data=data;
        this->left=nullptr;
        this->right=nullptr;
    }

    string EncontrarDato(int key);
    bool InsertarDato(int key, string data);
    void EliminarDato(string dato);

 };


 int main () {
    cout<<"holi";
    return 0;
 }
