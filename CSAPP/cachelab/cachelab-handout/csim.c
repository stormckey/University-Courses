#include "cachelab.h"
#include <stdio.h>
#include <getopt.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

typedef struct Op{
    unsigned int address;
    unsigned int size;
    char op;
}Op;
typedef struct block{
    unsigned int validation;
    unsigned int label;
    unsigned int lasttime;
}block;
typedef block* Set;
typedef struct Cache{
    unsigned int s;
    unsigned int b;
    unsigned int e;
    unsigned int v;
    char* file;
    Set * set;
}Cache;

void get_arg(unsigned int argc,char* argv[],Cache* cache);
void print_help();
unsigned int str2int(char*);
Op get_ops(FILE* file);
void delete_cache(Cache* cache);
void init_cache(Cache*);
void op_(Op*,unsigned int*,unsigned int*,unsigned int*,Cache*,unsigned int *);
unsigned int gets_s(unsigned int add,unsigned int s,unsigned int b) { return (add>>b) % (1<<s); }
unsigned int gett(unsigned int add,unsigned int s,unsigned int b) { return add>>(s+b); }

int main(int argc,char* argv[])
{
    Cache cache;
    get_arg(argc,argv,&cache);
    init_cache(&cache);
    unsigned int hit = 0, miss = 0, evic = 0,time = 0;
    Op op;
    FILE* trace = fopen(cache.file,"r");
    if (!trace) return 1;
    while(1){
        op = get_ops(trace);
        if(op.op == 0 ) break;
        if(op.op == 'I') continue;
        op_(&op,&hit,&miss,&evic,&cache,&time);
    }
    fclose(trace);
    delete_cache(&cache);
    printSummary(hit, miss, evic);
    return 0;
}

void get_arg(unsigned int argc,char* argv[],Cache* cache){
    cache->v = 0;
    char arg;
    while((arg = getopt(argc,argv,"hvs:E:b:t:"))!=-1){
        switch(arg){
            case 'h':
                print_help();
                break;
            case 'v':
                cache->v = 1;
                break;
            case 's':
                cache->s = str2int(optarg);
                break;
            case 'E':
                cache->e = str2int(optarg);
                break;
            case 'b':
                cache->b = str2int(optarg);
                break;
            case 't':
                cache->file = malloc(strlen(optarg)+1);
                strcpy(cache->file,optarg);
                break;
        }
    }
}
void print_help(){
    printf("Usage: ./csim-ref [-hv] -s <num> -E <num> -b <num> -t <file> \n \
Options: \n \
  -h         print this help message. \n \
  -v         Optional verbose flag. \n \
  -s <num>   Number of set index bits. \n \
  -E <num>   Number of lines per set. \n \
  -b <num>   Number of block offset bits. \n \
  -t <file>  Trace file. \n \
 \n \
Examples: \n \
  linux>  ./csim-ref -s 4 -E 1 -b 4 -t traces/yi.trace \n \
  linux>  ./csim-ref -v -s 8 -E 2 -b 4 -t traces/yi.trace\n");
}
unsigned int str2int (char* s){
    if(!s[1])   return s[0]-'0';
    return 10*(s[0]-'0' +str2int(s+1)); 
}
Op get_ops(FILE* file){
    char buf[50];
    Op op= {0,0,0};
    if(fgets(buf,49,file)) sscanf(buf," %c %x,%d",&op.op,&op.address,&op.size);
    return op;
}
void init_cache(Cache* cache){
    cache->set = malloc(sizeof(Set)*(1<<(cache->s)));
    for(unsigned int i=0;i<(1<<cache->s);i++){
        (cache->set)[i] = malloc(sizeof(block)*(1<<cache->b));
        for(unsigned int j=0;j<(1<<cache->b);j++){
            (((cache->set)[i])[j]).validation = 0; 
        }
    }
}
void delete_cache(Cache* cache){
    for(unsigned int i=0;i<cache->s;i++){
        free(cache->set[i]);
    }
    free(cache->set);
}
void op_(Op* op,unsigned int * hit,unsigned int* miss,unsigned int* evic,Cache* cache,unsigned int *time){
    if (cache->v)printf("%c %x,%d ",op->op,op->address,op->size);
    unsigned int s_index = gets_s(op->address,cache->s,cache->b);
    unsigned int t = gett(op->address,cache->s,cache->b);
    unsigned int tt = 99999,min = 0,empty = 9999999,flag = 0;
    for(unsigned int i=0;i<cache->e;i++){
        block * b = &((cache->set)[s_index])[i];
        if(!b->validation) empty = i;
        if(b->lasttime < tt){
            tt = b->lasttime;
            min = i;
        }
        if(flag) continue;
        if(b->validation && b->label == t){
            (*hit)++;
            if (cache->v) printf("hit ");
            b->lasttime = (*time)++;
            flag = 1;
        }
    }
    if(!flag&&empty!=9999999){
        block * b = &((cache->set)[s_index])[empty];
        (*miss)++;
        if(cache->v) printf("miss ");
        b->validation = 1;
        b->label = t;
        b->lasttime = (*time)++;
    }
    if(!flag&&empty==9999999){
        block * b = &((cache->set)[s_index])[min];
        b->label = t;
        (*miss)++;
        b->lasttime = (*time)++;
        (*evic)++;
        if(cache->v)printf("miss evication ");
    }
    if(op->op == 'M'){
        (*hit)++;
        if(cache->v)printf("hit ");
    }
    if(cache->v) printf("\n");
}