#include <bits/stdc++.h>

using namespace std;

int main(){
    map<pair<int, int>, set<int>> rel;
    map<pair<int, int>, int> novo;
    int a, b, c, aux;

    while (cin >> a >> b >> c){

        pair<int, int> key = make_pair(a, b);

        if (rel.find(key) == rel.end()){

            set<int> values;
            values.insert(c);
            rel[key] = values;
        } else{

            rel[key].insert(c);
        }
    }

    ofstream arquivoErro("guilherme-erro.txt");
    if (arquivoErro.is_open()) {
        cout << "De prima?";
    } else {
        cout << "Falha ao abrir o arquivo." << endl;
        return 1;
    }

    for (const auto& entry : rel) {
        pair<int, int> key = entry.first;
        set<int> values = entry.second;

        if(values.size() == 1){
            //cout << key.first << " " << key.second << ": " << *values.begin() << endl;
            novo[key] = *values.begin();
        }
        else{
            arquivoErro << key.first << " " << key.second << ": ";
            for (int value : values) {
                arquivoErro << value << " ";
            }
            arquivoErro << endl;
        }
    }
    arquivoErro.close();

    ofstream arquivo("guilherme-conections-novo.txt"); //saida normal

    if (arquivo.is_open()) {

        for(const auto& entry : novo){
            pair<int, int> key = entry.first;
            int value = entry.second;
            arquivo << key.first << " " << key.second << " " << value << endl;
        }

        arquivo.close(); 
    } else {
        cout << "Falha ao abrir o arquivo." << endl;
    }


    return 0;
}
