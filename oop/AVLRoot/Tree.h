#include <iostream>
#include "TreeNode.h"
#define Height(tn) (((Tree*)(tn))->height)
using namespace std;

#ifndef _TREE_H_
#define _TREE_H_
class Tree:public TreeNode{
friend void delete_tree(Tree*);
private:
    int height;
public:
    Tree(): Tree(0)  {};
    Tree(int key): TreeNode(key), height(0) {};
    Tree * insert (int num);
    void output(){
        if(left) ((Tree*)left)->output();
        cout << key << endl;
        if(right) ((Tree*)right)->output();
    };
    void update_h(){
        if(!left)
            if(!right)  height = 0;
            else height = Height(right) + 1;
        else 
            if(!right) height = Height(left) + 1; 
            else height = max(Height(left),Height(right))+1;
    };
    int not_balance() { 
        if(!left) return Height(this) > 1;
        else if(!right) return Height(this) >1;
        else {
            int && n = Height(left) - Height(right);
            return n < -1 || n > 1;
        }
    }
};
#endif