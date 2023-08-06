import time 
from lmf.dbv2 import db_command,db_query
import traceback
from lmf.bigdata import pg2pg 
from sqlalchemy.dialects.postgresql import  TEXT,BIGINT,TIMESTAMP,NUMERIC
import time 


def est_app_ry_query(conp):
    sql="""
     create table if not exists "public".app_ry_query (

    person_key bigint primary key ,
    name text not null ,

    gender text,
    zjhm text,  
    zj_type text ,



    entname text ,

    ent_key bigint ,
    xzqh text,
    zczj text,  
    fddbr text,
    clrq timestamp, 
    qy_alias text,
    logo text ,
    qy_total int ,

    ry_total int,

    ry_latest_zhongbiao_time timestamp ,

    ry_zhongbiao_info json[], 
    ryzz_info json[]

    ) distributed by (person_key)
    """

    db_command(sql,dbtype="postgresql",conp= conp)
    sql="grant select on table app_ry_query to app_reader"
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp)


def update_app_ry_query(conp):
    bg=time.time()
    est_app_ry_query(conp)
    sql="truncate public.app_ry_query;"
    db_command(sql,dbtype="postgresql",conp=conp)
    sql="""
    insert into "public".app_ry_query (person_key,name,zj_type,zjhm,gender,ryzz_info,ent_key,entname,xzqh
    ,clrq   ,zczj,  fddbr,  qy_alias,   logo    ,ry_total   ,ry_latest_zhongbiao_time,  qy_total    ,ry_zhongbiao_info)
    with a as (
    select 
    person_key, 

    (array_agg(name))[1] as name ,
    (array_agg(zj_type))[1] as zj_type ,
    (array_agg(zjhm))[1] as zjhm ,
    (array_agg(gender))[1] as gender 
    ,array_agg(json_build_object('zclb',zclb,'zsbh',zsbh,'yzh',yzh,'zhuanye',zhuanye,'youxiao_date',youxiao_date,'ryzz_code',ryzz_code)) as ryzz_info 
    ,(array_agg(ent_key))[1] as ent_key 
    ,(array_agg(entname))[1] as entname 
    ,(array_agg(xzqh))[1] as xzqh 
    from public.qy_zcry  where person_key!=0 and person_key is not null

    group by person_key 
    )

    select a.person_key,a.name,a.zj_type,a.zjhm,a.gender,a.ryzz_info
    ,a.ent_key,a.entname ,a.xzqh
    ,b.clrq,b.zczj,b.fddbr,b.alias as qy_alias,b.logo
    ,coalesce(c.zhongbiao_counts,0) as ry_total 
    ,c.gg_fabutimes[1] as ry_latest_zhongbiao_time 

    ,coalesce(e.zhongbiao_counts,0) as qy_total
    ,f.ry_zhongbiao_info 
     from a 
    left join "public".qy_base as b on a.ent_key=b.ent_key
    left join public.xmjl_zhongbiao as c on a.person_key=c.person_key
    left join  public.qy_zhongbiao as e on a.ent_key=e.ent_key


    left join 
    (select person_key
    ,array_agg(json_build_object('html_key',html_key,'href',href,'gg_name',gg_name,'quyu',xzqh,'zhongbiaojia',zhongbiaojia,'fabu_time',fabu_time)  ORDER BY fabu_time desc) as ry_zhongbiao_info
     from "public".gg_zhongbiao where person_key is not null group by person_key ) as f 
    on a.person_key=f.person_key
    ;
 
    """
    print(sql)
    

    db_command(sql,dbtype="postgresql",conp=conp)

    ed=time.time()

    cost=int(ed-bg)

    print("app_ry_query 全表耗时%d"%cost)