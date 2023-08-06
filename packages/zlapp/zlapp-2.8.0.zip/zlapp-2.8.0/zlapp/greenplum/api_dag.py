from queue import Queue 
from collections import defaultdict


class tbdag1: 

    def __init__(self,arr): 
        self.graph = defaultdict(list) 
        data=set()
        for w in arr:data=data|set(w)

        self.V = list(data)
        for w in arr:
            self.addEdge(*w)
  
    def addEdge(self,u,v): 
        self.graph[u].append(v) 
  
    def topologicalSortUtil(self,v,visited,stack): 

        visited[v] = True
    
        for i in self.graph[v]: 
            if visited[i] == False: 
                self.topologicalSortUtil(i,visited,stack) 
  
        stack.insert(0,v) 
  
    def topologicalSort(self): 
        visited = defaultdict(lambda :False)
        stack =[] 
  
        for i in self.V: 
            if visited[i] == False: 
                self.topologicalSortUtil(i,visited,stack) 
  

        return stack
#app后台有向无图 

class tbdag:
    arr=set()
    data=[
    ('gg_meta','gg'),('gg_meta','bd'),('gg_meta','t_gg_ent_bridge'),
    ('gg','gg_zhongbiao'),('gg','t_bd_xflv'),('gg','bd_dt'),
    ('gg_zhongbiao','qy_zhongbiao'),('gg_zhongbiao','xmjl_zhongbiao'),

   # ('qy_zhongbiao','app_qy_zz'),('qy_zz','app_qy_zz'),('qy_base','app_qy_zz'),
    ('qy_zhongbiao','app_qy_query'),

    ('xmjl_zhongbiao','app_qy_zcry'),('t_person','app_qy_zcry'),('qy_base','app_qy_zcry'),('qy_zhongbiao','app_qy_zcry'),

    ('qy_zz','app_qy_query'),('app_qy_zcry','app_qy_query'),('t_gg_ent_bridge','app_qy_query'),

    ('qy_base','app_qy_query'),('qy_base','t_gg_ent_bridge'),

    ('qy_zcry','app_qy_zcry'),('qy_zcry','app_qy_query'),
    #('gg_html','gg_html_algo'),
    ('qy_zcry','app_ry_query'),('qy_base','app_ry_query'),('qy_zhongbiao','app_ry_query'),('xmjl_zhongbiao','app_ry_query'),('gg_zhongbiao','app_ry_query'),
    ('gg_zhongbiao','entrank'),('gg','html_key_xflv')

    #,('gg_zhongbiao','app_gg_zhongbiao'),('qy_zhongbiao','app_gg_zhongbiao'),('qy_base','app_gg_zhongbiao')
    ]
    arr=set(data)
    tp=tbdag1(arr).topologicalSort()
    @staticmethod
    def get_next(item):
        data=[]
        for w in tbdag.arr:
            if w[0]==item:data.append(w[1])

        return data

    @staticmethod
    def get_pre(item):
        data=[]
        for w in tbdag.arr:
            if w[1]==item:data.append(w[0])
        return data

    @staticmethod
    def tplist1(item):
        result=[item]
        q=Queue()
        q.put(item)
        while not q.empty():
            x=q.get()
            y=tbdag.get_next(x)
            if y !=[]:
                for w in y:
                    result.append(w)
                    q.put(w)

        return result

    @staticmethod 
    def isinfluence(item1,item2):
        result=tbdag.tplist1(item1)
        return item2 in result

    @staticmethod 
    def tplist(item):
        arr=tbdag.tp[tbdag.tp.index(item):]
        for w in arr[1:]:
            if not tbdag.isinfluence(item,w):arr.remove(w)
        return arr










