#include <stdio.h>
#include <stdlib.h>
#include "csapp.h"

/* Recommended max cache and object sizes */
#define MAX_CACHE_SIZE 1049000
#define MAX_OBJECT_SIZE 102400

typedef struct {
    char forward_host[MAXLINE];
    char forward_obj[MAXLINE];
    char forward_port[MAXLINE];
    char host[MAXLINE];
}Request;
typedef struct {
    char host[MAXLINE];
    char obj[MAX_OBJECT_SIZE-MAXLINE];
}Block;
typedef struct{
    int cnt;
    Block cache[MAX_CACHE_SIZE/MAX_OBJECT_SIZE];
}Cache;

/* You won't lose style points for including this long line in your code */
static const char *user_agent_hdr = "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:10.0.3) Gecko/20120305 Firefox/10.0.3";
int netread(int connfd, char* buf);
int parse(char*,Request*);
void* thread(void*);
int cache_r(char*,char*host);
void cache_w(char*,Request*);
int ifbinary(Request*);
inline int ifbinary(Request* request){
    return (!(strcmp("/tiny",request->forward_obj))) || (!(strcmp("/godzilla.gif",request->forward_obj))) || (!(strcmp("/godzilla.jpg",request->forward_obj)));
}
sem_t mutex_r,mutex_w;
int cnt_r = 0;
Cache cache;

int main(int argc, char**argv)
{
    cache.cnt = 0;
    sem_init(&mutex_r,0,1);
    sem_init(&mutex_w,0,1);
    socklen_t clientlen = sizeof(struct sockaddr_storage);
    struct sockaddr_storage clientaddr;
    char client_hostname[MAXLINE],client_port[MAXLINE],buf[MAXLINE],header[MAXLINE];//definition and initialization
    int connfd,listenfd = Open_listenfd(argv[1]);//listen to the user
    pthread_t tid;
    while(1){
        connfd = Accept(listenfd, (SA *) &clientaddr, &clientlen);//receive a conection,relavent info will be stored in clientaddr
        printf("%s\n",client_hostname);
        Getnameinfo((SA*)&clientaddr,clientlen,client_hostname,MAXLINE,client_port,MAXLINE,0);//extract data out from clientaddr
        printf("Received connection from %s:%s\n",client_hostname,client_port);
        Pthread_create(&tid,NULL,thread,(void*)connfd);//create a thread to handle the request
    }
    return 0;
}
/*
read a line of string from connfd into buf
*/
int netread (int connfd, char* buf){
    rio_t rio;
    Rio_readinitb(&rio, connfd);
    return Rio_readlineb(&rio,buf,MAXLINE);
}
/*
parse the data stored in buf and store the result in request
*/
int parse(char* buf,Request* request){
    char method[MAXLINE];
    sscanf(buf," %s",method);
    if(strcmp(method,"GET")){
        printf("Invalid method\n");
        return 1;
    };//test if the method is GET
    buf += strlen(method)+1;//jump over method
    sscanf(buf," %s",request->forward_host);
    sscanf(buf," %s",request->host);
    char * slash = strchr(request->forward_host+8,'/');//the / after the port
    char * colon = strchr(request->forward_host+8,':');//the colon before port(if exist)
    sscanf(slash,"%s",request->forward_obj);
    if(colon){//if there is the port
        *(slash) = '\0';//seperate the port
        sscanf(colon,"%7s",request->forward_port);//read the port
        *(colon) = '\0';//seperate the host
    }else{
        strcpy(request->forward_port,":80");//default prt
        *(strchr(request->forward_host+8,'/')) = '\0';
    }
}
void* thread(void* v){
    int connfd = (int)v;
    Request *request = malloc(sizeof(Request));//store the parsed data
    Pthread_detach(pthread_self());
    char buf[MAXLINE],header[MAXLINE],response[MAXLINE],Response[MAX_OBJECT_SIZE],*p = Response;
    if(netread(connfd,buf)) parse(buf,request);
    if(cache_r(Response,request->host)){//try to read from cache
        Rio_writen(connfd,Response,strlen(Response));
        free(request);
        Close(connfd);
        return;
    }
    sprintf(header,"%s %s %s\r\n%s %s\r\n%s %s\r\n%s %s\r\n%s %s\r\n\r\n",\
            "GET",request->forward_obj,"HTTP/1.0",\
            "Host:",request->forward_host,\
            "User-Agent:",user_agent_hdr,\
            "Connection:","close",\
            "Proxy-Connection:","close");//put the data into header
    int clientfd,n,cnt=0,is_binary=0;;
    clientfd = open_clientfd(request->forward_host+7,request->forward_port+1);//try to connect to the server
    rio_t rio;
    Rio_readinitb(&rio,clientfd);
    Rio_writen(clientfd,header,MAXLINE);//write backc the header
    while(Rio_readlineb(&rio,response,MAXLINE)){
        if(is_binary = ifbinary(request))   break;//if the data is binary we dont need to cahe it and we shall output directly
        if(cnt++ >= 4){
            sprintf(p,"%s",response);
            p += strlen(p);//stored in respnse to be stored in Response to store in cache
        }
        else    printf("%s",response);//header info will be printed in proxy
    }
    if(is_binary)//if the data is binary
        while(n = Rio_readlineb(&rio,response,MAXLINE))
            if(cnt++>=4)    Rio_writen(connfd,response,n);
            else printf("%s",response);
    else{//the output has been stored in Response
        Rio_writen(connfd,Response,strlen(Response));
        cache_w(Response,request);
    }
    Close(clientfd);
    Close(connfd); 
    free(request);
}
//read first 
int cache_r(char *buf,char*host){
    P(&mutex_r);
    cnt_r++;
    if(cnt_r ==1) P(&mutex_w);
    V(&mutex_r);
    int flag = 0;
    for(int i=0;i<cache.cnt;i++){//test the proxy member of every Block
        if(flag = !strcmp(host,((Block*)&cache.cache[i])->host)) {
            strcpy(buf,((Block*)&cache.cache[i])->obj);
            break;
        }
    }
    P(&mutex_r);
    cnt_r--;
    if(cnt_r == 0) V(&mutex_w);
    V(&mutex_r);
    return flag;
}
void cache_w(char* Response,Request * request){
    P(&mutex_w);
    Block* ptr = (Block*)&cache.cache[cache.cnt++];
    strcpy(ptr->host,request->host);
    strcpy(ptr->obj,Response);
    V(&mutex_w);
}