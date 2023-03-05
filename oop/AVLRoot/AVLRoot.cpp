#include <iostream>
#define MAXPATH 30
#define LEFT 0
#define RIGHT 1
#define Height(tn) (((Tree*)(tn))->height)
#define update_path_node(n) ((Tree*)path[n])->update_h()
using namespace std;

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

class Tree:public TreeNode{
friend void delete_tree(Tree*);
private:
    int height;
public:
    Tree(): Tree(0)  {};
    Tree(int key): TreeNode(key), height(0) {};
    Tree * insert (int num);
    void output();
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

class Path{
private:
    TreeNode * path[30];
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
}
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
void Tree::output(){
    if(left) ((Tree*)left)->output();
    cout << key << endl;
    if(right) ((Tree*)right)->output();
}
void delete_tree(Tree * tree){
    if(tree->left) delete_tree((Tree*)(tree->left));
    if(tree->right) delete_tree((Tree*)(tree->right));
    delete tree;
}