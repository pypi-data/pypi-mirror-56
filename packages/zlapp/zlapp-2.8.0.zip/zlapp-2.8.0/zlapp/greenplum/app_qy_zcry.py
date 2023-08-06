import time 
from lmf.dbv2 import db_command,db_query
import traceback
from lmf.bigdata import pg2pg 
from sqlalchemy.dialects.postgresql import  TEXT,BIGINT,TIMESTAMP,NUMERIC
import time 

def est_app_qy_zcry(conp):
    sql="""
    CREATE TABLE if not exists "public"."app_qy_zcry" (
    "ent_key" int8 not null,
    "tydm" text COLLATE "default",
    "xzqh" text COLLATE "default",
    "ryzz_code" text COLLATE "default",
    "href" text COLLATE "default",
    "name" text COLLATE "default",
    "gender" text COLLATE "default",
    "zjhm" text COLLATE "default",
    "zj_type" text COLLATE "default",
    "zclb" text COLLATE "default",
    "zhuanye" text COLLATE "default",
    "zsbh" text COLLATE "default",
    "yzh" text COLLATE "default",
    "youxiao_date" text COLLATE "default",
    "entname" text COLLATE "default",
    "person_key" int8 not null,
    "qy_total" int8 not null,
    "ry_total" int8 not null,
    "fabu_time" timestamp(6),
    "zczj" text COLLATE "default",
    "fddbr" text COLLATE "default",
    "clrq" timestamp(6),
    "qy_alias" text COLLATE "default",
    "logo" text COLLATE "default"
    )
    distributed by (person_key)"""



    db_command(sql,dbtype="postgresql",conp=conp)


    sql="grant select on table app_qy_zcry to app_reader"
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp)


def update_app_qy_zcry(conp):
    bg=time.time()
    est_app_qy_zcry(conp)
    sql="truncate public.app_qy_zcry;"
    db_command(sql,dbtype="postgresql",conp=conp)
    
    sql="""
    
    insert into "public".app_qy_zcry(ent_key,   tydm,   xzqh    ,ryzz_code  ,href,  name,   gender  ,zjhm   ,zj_type,   zclb    ,zhuanye,   zsbh    ,yzh,   youxiao_date,   entname
        ,person_key  ,ry_total ,fabu_time  ,zczj   
    ,fddbr  ,clrq   ,qy_alias   ,logo,qy_total)
    SELECT 
    a.*

    ,coalesce(b.zhongbiao_counts,0) as ry_total 
    ,b.gg_fabutimes[1] as fabu_time 

    ,c.zczj
    ,c.fddbr
    ,c.clrq
    ,c.alias as qy_alias
    ,c.logo
    ,coalesce(d.zhongbiao_counts,0) as qy_total

    FROM "public"."qy_zcry" as a 
 
    left join public.xmjl_zhongbiao as b on a.person_key=b.person_key
    left join public.qy_base as c on a.ent_key=c.ent_key
    left join  public.qy_zhongbiao as d on a.ent_key=d.ent_key
       where a.ent_key is not null and length(a.name)>1
        """
    print(sql)

    db_command(sql,dbtype="postgresql",conp=conp)

    ed=time.time()

    cost=int(ed-bg)

    print("app_qy_zcry 全表更新 耗时%s"%cost)