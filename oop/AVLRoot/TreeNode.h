#include <iostream>
using namespace std;

#ifndef _TREENODE_H_
#define _TREENODE_H_
class TreeNode{
friend class Tree;
friend class Path;
protected:
    int key;
    TreeNode *left;
    TreeNode *right;
public:
    TreeNode():TreeNode(0){};
    TreeNode(int key): key(key), left(nullptr), right(nullptr){}; 
    int larger(int num) { return key > num; }
    int smaller(int num) { return key < num; }
    void print_root() { cout << key;}
};
#endif