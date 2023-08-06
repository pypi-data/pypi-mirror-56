import time 
from lmf.dbv2 import db_command,db_query
import traceback
from lmf.bigdata import pg2pg 
from sqlalchemy.dialects.postgresql import  TEXT,BIGINT,TIMESTAMP,NUMERIC

import time 

def est_gg_zhongbiao(conp):
    sql="""
    CREATE  TABLE if not exists "public"."gg_zhongbiao" (
    "html_key"  int8 primary key,
    "href" text COLLATE "default",
    "ggtype" text COLLATE "default",
    "quyu" text COLLATE "default",
    "zhongbiaoren" text COLLATE "default",
    "zhaobiaoren" text COLLATE "default",
    "zbdl" text COLLATE "default",
    "zhongbiaojia" numeric,
    "kzj" numeric,
    "xmmc" text COLLATE "default",
    "xmjl" text COLLATE "default",
     "xmjl_zsbh" text COLLATE "default",
    "xmdz" text COLLATE "default",
    "zbfs" text COLLATE "default",
    "xmbh" text COLLATE "default",
    "gg_name" text COLLATE "default",
    "fabu_time" timestamp(6),
    "xzqh" text COLLATE "default",
    "ts_title" tsvector,
    "ent_key" int8 not null,
    "person_key" int8 
    )
    distributed by (html_key)"""

    db_command(sql,dbtype="postgresql",conp=conp)

    sql="grant select on table gg_zhongbiao to app_reader"
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp)
    sql=" select * from pg_indexes where tablename='gg_zhongbiao' and indexname='idx_gg_zhongbiao_ent_key' "
    df=db_query(sql,dbtype="postgresql",conp=conp)
    if df.empty:
        sql="create index idx_gg_zhongbiao_ent_key on public.gg_zhongbiao(ent_key)"
        print(sql)
        db_command(sql,dbtype="postgresql",conp=conp)


def est_gg_zhaobiao(conp):
    sql="""
    CREATE  TABLE if not exists "public"."gg_zhaobiao" (
    "html_key"  int8 primary key,
    "href" text COLLATE "default",
    "ggtype" text COLLATE "default",
    "quyu" text COLLATE "default",
    "zhongbiaoren" text COLLATE "default",
    "zhaobiaoren" text COLLATE "default",
    "zbdl" text COLLATE "default",
    "zhongbiaojia" numeric,
    "kzj" numeric,
    "xmmc" text COLLATE "default",
    "xmjl" text COLLATE "default",
     "xmjl_zsbh" text COLLATE "default",
    "xmdz" text COLLATE "default",
    "zbfs" text COLLATE "default",
    "xmbh" text COLLATE "default",
    "gg_name" text COLLATE "default",
    "fabu_time" timestamp(6),
    "xzqh" text COLLATE "default",
    "ts_title" tsvector,
    "ent_key" int8 ,
    "person_key" int8 
    )
    distributed by (html_key)"""

    db_command(sql,dbtype="postgresql",conp=conp)

    sql="grant select on table gg_zhaobiao to app_reader"
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp)
    sql=" select * from pg_indexes where tablename='gg_zhaobiao' and indexname='idx_gg_zhaobiao_zhaobiaoren' "
    df=db_query(sql,dbtype="postgresql",conp=conp)
    if df.empty:
        sql="create index idx_gg_zhaobiao_zhaobiaoren on public.gg_zhaobiao(zhaobiaoren)"
        print(sql)
        db_command(sql,dbtype="postgresql",conp=conp)

    #create index idx_gg_zhongbiao_ent_key on gg_zhongbiao(ent_key)

def update_gg_zhongbiao(conp):
    bg=time.time()

    est_gg_zhongbiao(conp)
    sql="truncate table public.gg_zhongbiao;"
    db_command(sql,dbtype="postgresql",conp=conp)
    sql="""
    
    insert into public.gg_zhongbiao( html_key,  href ,   ggtype , quyu ,   zhongbiaoren,    zhaobiaoren ,zbdl  ,  zhongbiaojia  ,  kzj, xmmc,    xmjl ,xmjl_zsbh,   xmdz ,
           zbfs  ,  xmbh ,   gg_name, fabu_time ,  xzqh ,   ts_title,person_key,ent_key)

    select  html_key,  href ,   ggtype ,quyu ,   zhongbiaoren, zhaobiaoren ,zbdl  ,zhongbiaojia::numeric zhongbiaojia  
    ,  kzj, xmmc,  xmjl ,xmjl_zsbh,   xmdz ,zbfs  ,  xmbh , gg_name,fabu_time ,  xzqh , ts_title::tsvector ts_title 
      ,person_key,ent_key  from public.gg_meta 
    where   ent_key is not null  and ent_key!=0
    """
    print(sql)

    db_command(sql,dbtype="postgresql",conp=conp)

    ed=time.time()

    cost=int(ed-bg)

    print("gg_zhongbiao 全表重导入耗时%s 秒"%cost)

#def update_gg_zhaobiao(conp):
    bg=time.time()

    est_gg_zhaobiao(conp)
    sql="truncate table public.gg_zhaobiao;"
    db_command(sql,dbtype="postgresql",conp=conp)
    sql="""
    
    insert into public.gg_zhaobiao( html_key,  href ,   ggtype , quyu ,   zhongbiaoren,    zhaobiaoren ,zbdl  ,  zhongbiaojia  ,  kzj, xmmc,    xmjl ,xmjl_zsbh,   xmdz ,
           zbfs  ,  xmbh ,   gg_name, fabu_time ,  xzqh ,   ts_title,person_key,ent_key)

    select  html_key,  href ,   ggtype ,quyu ,   zhongbiaoren, zhaobiaoren ,zbdl  ,zhongbiaojia::numeric zhongbiaojia  
    ,  kzj, xmmc,  xmjl ,xmjl_zsbh,   xmdz ,zbfs  ,  xmbh , gg_name,fabu_time ,  xzqh , ts_title::tsvector ts_title 
      ,person_key,ent_key  from public.gg_meta 
    where   zhaobiaoren is not null 
    """
    print(sql)

    db_command(sql,dbtype="postgresql",conp=conp)

    ed=time.time()

    cost=int(ed-bg)

    print("gg_zhaobiao 全表重导入耗时%s 秒"%cost)