import time 
from lmf.dbv2 import db_command,db_query
import traceback
from lmf.bigdata import pg2pg 
from sqlalchemy.dialects.postgresql import  TEXT,BIGINT,TIMESTAMP,NUMERIC
import time 
from datetime import datetime
from lmf.tool import add_months

def est_entrank(conp):
    sql="""
    create table if not exists   "public".entrank(
    "companyKey"  bigint,
    "companyName"   text,
    "totalCount"  int,  
    "totalMoney"  float,    
    "totalCountRank" int,   
    "totalMoneyRank" int,   
    "time_range" text

    ) distributed by ("companyKey")"""


    

    db_command(sql,dbtype="postgresql",conp= conp)



def update_entrank(conp):
    bg=time.time()
    est_entrank(conp)
    sql="truncate public.entrank;"
    db_command(sql,dbtype="postgresql",conp=conp)
    nw=datetime.strftime(datetime.now(),'%Y-%m-01')
    bdate=add_months(nw,-12)
    edate=add_months(1)
   # bdate,edate='-'.join([str(datetime.now().year-1),str(datetime.now().month),'01']),'-'.join([str(datetime.now().year),str(datetime.now().month+1),'01'])
    sql="""
    insert into entrank("companyKey",   "companyName",  "totalCount"    ,"totalMoney"   ,"totalCountRank"   ,"totalMoneyRank"   ,"time_range")

    with a as (SELECT 
        ent_key ,
        zhongbiaoren,
        count(*) cn,
        sum(coalesce(zhongbiaojia,0)) as sm 
         FROM "public"."gg_zhongbiao" 
        
        
        where   ent_key is not null 
        and fabu_time>='%s' and fabu_time<'%s'
        group by ent_key ,zhongbiaoren)
        
        ,b as(
        select 
        ent_key "companyKey",
        zhongbiaoren as "companyName"
        , cn "totalCount"
        ,sm::float "totalMoney"
        ,rank() over( order by cn desc  ) "totalCountRank"
        
        ,rank() over( order by sm desc  ) "totalMoneyRank"
         from a  )


    ,a1 as (SELECT 
        ent_key ,
        zhongbiaoren,
        count(*) cn,
        sum(coalesce(zhongbiaojia,0)) as sm 
         FROM "public"."gg_zhongbiao" 
        
        
        where   ent_key is not null 
        
        group by ent_key ,zhongbiaoren)
        
        ,b1 as(
        select 
        ent_key "companyKey",
        zhongbiaoren as "companyName"
        , cn "totalCount"
        ,sm::float "totalMoney"
        ,rank() over( order by cn desc  ) "totalCountRank"
        
        ,rank() over( order by sm desc  ) "totalMoneyRank"
         from a1  )


    select * from (select *,'%s,%s' time_range from b ) t1

    union all 

    select * from (select *,'' time_range   from b1 ) t2
    """%(bdate,edate,bdate,edate)
    print(sql)
    

    db_command(sql,dbtype="postgresql",conp=conp)

    ed=time.time()

    cost=int(ed-bg)

    print("entrank 全表耗时%d"%cost)