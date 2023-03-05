#include "TreeNode.h"
#include "Tree.h"
#include "Path.h"

Tree* Tree::insert(int num){
    TreeNode *probe=this,**next;
    Path path;
    while(1){
        path.push(probe);
        if(probe->larger(num)) 
            next = &(probe->left);
        else
            next = &(probe->right);//need the input number to be distinct
        if(!*next){
            *next = new Tree(num);
            path.push(*next);
            break;
        }
        probe = *next;
    }
    path.pop();
    while(path.test_rota((Tree*)path.pop()));
    return path.getRoot();
}