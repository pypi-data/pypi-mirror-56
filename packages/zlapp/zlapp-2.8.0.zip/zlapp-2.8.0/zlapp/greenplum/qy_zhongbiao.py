import time 
from lmf.dbv2 import db_command,db_query
import traceback
from lmf.bigdata import pg2pg 
from sqlalchemy.dialects.postgresql import  TEXT,BIGINT,TIMESTAMP,NUMERIC
import time 
def est_qy_zhongbiao( conp):
    sql="""
    CREATE  TABLE if not exists "public"."qy_zhongbiao" (
     "ent_key" int8 primary key,
    "zhongbiaoren" text COLLATE "default",
    "gg_names" _text,
    "gg_fabutimes" _timestamp,
    "html_keys" _int8,
    "zhongbiaojias" _numeric,
    "zhongbiao_counts" int8
   
    ) distributed by (ent_key)"""


    db_command(sql,dbtype="postgresql",conp=conp)



def update_qy_zhongbiao(conp):
    bg=time.time()
    est_qy_zhongbiao(conp)
    sql="""    truncate  public.qy_zhongbiao;"""
    db_command(sql,dbtype="postgresql",conp=conp)
    sql="""
    insert into public.qy_zhongbiao(ent_key,   gg_names,   gg_fabutimes,   html_keys,  zhongbiaojias,  zhongbiao_counts,  zhongbiaoren)


    with a as (SELECT ent_key
    ,array_agg(gg_name order by fabu_time desc ) as gg_names 


    ,array_agg(fabu_time order by fabu_time desc) gg_fabutimes

    ,array_agg(html_key order by fabu_time desc) html_keys

    ,array_agg(zhongbiaojia order by fabu_time desc ) as zhongbiaojias 
    
    ,count(*) zhongbiao_counts
    
    ,(array_agg(zhongbiaoren order by fabu_time desc ))[1] as zhongbiaoren 


     FROM "public"."gg_zhongbiao" where ent_key is not null and ent_key!=0 group by ent_key )


    select * from a 

 
    """
    #select a.*,b.ent_key from a left join  "public".qy_base  as b on a.zhongbiaoren=b.jgmc 
    print(sql)

    db_command(sql,dbtype="postgresql",conp=conp)

    ed=time.time()
    cost=int(ed-bg)
    print("qy_zhongbiao表更新需要 %s "%cost)