#include "Tree.h"
#include "TreeNode.h"
#define MAXPATH 30

#ifndef _PATH_H_
#define _PATH_H_
class Path{
private:
    TreeNode * path[MAXPATH];
    Tree * Root;
    int n;
public:
    Path(): n(0), Root(nullptr) {};
    void push(TreeNode* t) { path[n++] = t; }
    TreeNode * next() { return path[n+1]; }
    void single_rota(int direction);
    void double_rota(int direction);
    int test_rota(Tree * tn);
    Tree* getRoot() { return (Tree*)Root;}
    TreeNode* pop() { 
        if(--n>=0) return path[n];
        else return nullptr;
    }
    int get_rot_type(){//left is 0 and right is 1 so ,we have 00/01/10/11 four types
        int type = 0;
        if(path[n]->right)
            if((path[n]->right)->key == path[n+1]->key) type += 2;
        if(path[n+1]->right)
            if((path[n+1]->right)->key == path[n+2]->key) type += 1;
        return type;
    }
};
#endif