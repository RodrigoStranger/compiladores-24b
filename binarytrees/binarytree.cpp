#include <iostream>
#include <string>

using namespace std;

class Nodo {
private:
    Nodo* Eliminar(Nodo* nodo, int key);
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
    
    Nodo* EliminarDato(int key);
    Nodo* EncontrarMinimo(Nodo* nodo);

 };

string Nodo::EncontrarDato(int key) {
    if(this->key == key) {
        return this->data;
    } else if (key < this->key && this-> left != nullptr) {
        return this->left->EncontrarDato(key);
    } else if (key > this->key && this->right != nullptr) {
        return this->right->EncontrarDato(key);
    } else {
        return "-1";
    }
}

bool Nodo::InsertarDato(int key, string data) {
    if(this->key == key) {
        cout<<"No se pudo insertar el dato";
        return false; 
    } else if (key < this->key) {
         if (this->left == nullptr) {
            this->left = new Nodo(key, data);
            return true; 
        }else {
            return this->left->InsertarDato(key, data);
        }
    } else {
        if (this->right == nullptr) {
            this->right = new Nodo(key, data);
            return true; 
        } else {
            return this->right->InsertarDato(key, data);
        }
    }
}

Nodo* Nodo::EncontrarMinimo(Nodo* nodo) {
    while (nodo && nodo->left != nullptr) {
        nodo = nodo->left;
    }
    return nodo;
}

Nodo* Nodo::Eliminar(Nodo* nodo, int key) {
    if (nodo == nullptr) return nodo;
    if (key < nodo->key) {
        nodo->left = Eliminar(nodo->left, key);
    } else if (key > nodo->key) {
        nodo->right = Eliminar(nodo->right, key);
    } else {
        if (nodo->left == nullptr) {
            Nodo* temp = nodo->right;
            delete nodo;
            return temp;
        } else if (nodo->right == nullptr) {
            Nodo* temp = nodo->left;
            delete nodo;
            return temp;
        }

        Nodo* temp = EncontrarMinimo(nodo->right);
        nodo->key = temp->key;
        nodo->data = temp->data;
        nodo->right = Eliminar(nodo->right, temp->key);
    }
    return nodo;
}

Nodo* Nodo::EliminarDato(int key) {
    return Eliminar(this, key);
}

 int main () {
    Nodo* root = new Nodo(10, "Raiz");
    root->InsertarDato(12, "asdasd");
    root->InsertarDato(11, "asdasssssss");
    //cout<<root->EncontrarDato(12);
    root = root->EliminarDato(10);
    cout<<root->EncontrarDato(10);
    return 0;
 }
