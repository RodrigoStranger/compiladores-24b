#include <iostream>
#include <string>

using namespace std;

class Nodo {
public:
    int key;
    int data;
    Nodo* left;
    Nodo* right;
    
    Nodo(int key, int data) {
        this->key=key;
        this->data=data;
        this->left=nullptr;
        this->right=nullptr;
    }

    int EncontrarDato(int key);
    bool InsertarDato(int key, int data);
    void EliminarDato(int data);

 };

int Nodo::EncontrarDato(int key) {
    if(this->key==key) {
        return this->data;
    } else if (key<this->key && this->left!=nullptr) {
        return this->left->EncontrarDato(key);
    } else if (key>this->key && this->right!=nullptr) {
        return this->right->EncontrarDato(key);
    } else {
        return -1;
    }
}

bool Nodo::InsertarDato(int key, int data) {
    
}

void Nodo::EliminarDato(int data) {

}

 int main () {
    cout<<"holi";
    return 0;
 }
