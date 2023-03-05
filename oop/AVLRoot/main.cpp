#include <iostream>
#include "TreeNode.h"
#include "Tree.h"
#include "Path.h"
using namespace std;

void delete_tree(Tree * tree);
inline int max(int a,int b) {return a>b?a:b;}

int main(){
    int n,num;
    cin >> n >>num;
    Tree *tree = new Tree(num);
    for(int i=0;i<n-1;i++){
        cin >>num;
        Tree * && newroot = tree->insert(num);
        if(newroot) tree = newroot;

    }
    tree->print_root();
    delete_tree(tree);
}

void delete_tree(Tree * tree){
    if(tree->left) delete_tree((Tree*)(tree->left));
    if(tree->right) delete_tree((Tree*)(tree->right));
    delete tree;
}