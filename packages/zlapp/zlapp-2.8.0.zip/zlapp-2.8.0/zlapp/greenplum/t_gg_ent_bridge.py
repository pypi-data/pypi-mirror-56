import time 
from lmf.dbv2 import db_command,db_query
import traceback
from lmf.bigdata import pg2pg 
from sqlalchemy.dialects.postgresql import  TEXT,BIGINT,TIMESTAMP,NUMERIC
import time 
def est_t_gg_ent_bridge(conp):
    sql="""
    CREATE  TABLE if not exists "public"."t_gg_ent_bridge" (
    "html_key" int8 ,
    "href" text COLLATE "default",
    "ggtype" text COLLATE "default",
    "quyu" text COLLATE "default",
    "entname" text COLLATE "default",
    "entrole" text COLLATE "default",
    "price" numeric,
    "diqu" text COLLATE "default",
    "xzqh" text COLLATE "default",
    "fabu_time" timestamp(6),
    "gg_name" text COLLATE "default",
    "ent_key" int8
    )
    distributed by (html_key)"""

    db_command(sql,dbtype="postgresql",conp=conp)

    sql="grant select on table t_gg_ent_bridge to app_reader"
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp)
    sql=" select * from pg_indexes where tablename='t_gg_ent_bridge' and indexname='idx_t_gg_ent_bridge_ent_key' "
    df=db_query(sql,dbtype="postgresql",conp=conp)
    if df.empty:
        sql="create index idx_t_gg_ent_bridge_ent_key on public.t_gg_ent_bridge(ent_key)"
        print(sql)
        db_command(sql,dbtype="postgresql",conp=conp)


def update_t_gg_ent_bridge(conp):
    bg=time.time()
    est_t_gg_ent_bridge(conp)
    sql=" truncate public.t_gg_ent_bridge;"
    db_command(sql,dbtype="postgresql",conp=conp)
    sql="""

    insert into t_gg_ent_bridge(html_key,   href    ,ggtype ,quyu,  entname ,entrole,   price   ,diqu,  xzqh,   fabu_time,  gg_name,    ent_key)
        with a as (SELECT html_key,href,ggtype,quyu
        ,zhongbiaoren as entname ,'中标人'::text entrole
        ,zhongbiaojia::float as price  ,diqu,xzqh,fabu_time,gg_name,ent_key
         FROM "public".gg_meta  where zhongbiaoren is not null and ent_key is not null
         )
        ,b as (SELECT html_key,href,ggtype,quyu
        ,zhaobiaoren as entname ,'招标人'::text entrole
        ,kzj::float as price  ,diqu,t1.xzqh,fabu_time,gg_name,t2.ent_key
         FROM "public".gg_meta as t1
         left join public.qy_base as t2 on  t1.zhaobiaoren=t2.jgmc
          where zhaobiaoren is not null  
         )
        ,c as (SELECT html_key,href,ggtype,quyu
        ,zbdl as entname ,'招标代理'::text entrole
        ,kzj::float as price  ,diqu,q1.xzqh,fabu_time,gg_name,q2.ent_key
         FROM "public".gg_meta q1 
         left join public.qy_base as q2 on  q1.zbdl=q2.jgmc
         where zbdl is not null
         )
        , d as (
         select * from a union  select * from b union select * from c)
        select html_key,   href    ,ggtype ,quyu,  entname ,entrole,   price   ,diqu,  xzqh,   fabu_time,  gg_name,    ent_key from d 
    """
    print(sql)

    db_command(sql,dbtype="postgresql",conp=conp)

    ed=time.time()

    cost=int(ed-bg)
    print("t_gg_ent_bridge 全表更新耗时%d"%cost)