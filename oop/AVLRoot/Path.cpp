#include "TreeNode.h"
#include "Tree.h"
#include "Path.h"
#define LEFT 0
#define RIGHT 1
#define update_path_node(n) ((Tree*)path[n])->update_h()

void Path::single_rota(int direction){
    if(n)
        if(path[n-1]->left&&path[n-1]->left->key == path[n]->key)   path[n-1]->left = path[n+1];
        else path[n-1]->right = path[n+1];
    else Root = (Tree*) path[n+1];
    if(direction == RIGHT){
        TreeNode * tmp = path[n+1]->right;
        path[n+1]->right = path[n];
        path[n]->left = tmp;
    }else{
        TreeNode *tmp = path[n+1]->left;
        path[n+1]->left = path[n];
        path[n]->right = tmp;
    }
    update_path_node(n);
    update_path_node(n+1);
}
void Path::double_rota(int direction){
    if(n)
        if(path[n-1]->left&&path[n-1]->left->key == path[n]->key)   path[n-1]->left = path[n+2];
        else path[n-1]->right = path[n+2];
    else Root = (Tree*) path[n+2];
    if(direction == RIGHT){
        TreeNode * tmp1 = path[n+2]->left;
        TreeNode * tmp2 = path[n+2]->right;
        path[n+2]->left = path[n];
        path[n+2]->right = path[n+1];
        path[n]->right = tmp1;
        path[n+1]->left = tmp2;
    }else{
        TreeNode * tmp1 = path[n+2]->left;
        TreeNode * tmp2 = path[n+2]->right;
        path[n+2]->left = path[n+1];
        path[n+2]->right = path[n];
        path[n+1]->right = tmp1;
        path[n]->left  = tmp2; 
    }
    update_path_node(n);
    update_path_node(n+1);
    update_path_node(n+2);
}
int Path::test_rota(Tree* tn){
    if(!tn) return 0;
    ((Tree*)tn)->update_h();
    if(((Tree*)tn)->not_balance()){
        int && type = get_rot_type();
        if(type >>1)
            if(type&1) single_rota(LEFT);//11
            else double_rota(RIGHT);//10
        else
            if(type&1) double_rota(LEFT);//01
            else single_rota(RIGHT);//00
    }
    return 1;
}