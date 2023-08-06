import time 
from lmf.dbv2 import db_command,db_query
import traceback
from lmf.bigdata import pg2pg 
from sqlalchemy.dialects.postgresql import  TEXT,BIGINT,TIMESTAMP,NUMERIC
import time
from zlapp import forbiden_list
from lmf.tool import mythread
#conp=['developer','developer','192.168.169.111','biaost','public']


#app_gg_meta_single

def est_app_gg_meta_single(conp_gp):
    sql="""
    CREATE TABLE if not exists app.gg_meta_single (
    html_key bigint,
    guid text,
    gg_name text,
    href text,
    fabu_time timestamp,
    ggtype text,
    jytype text,
    diqu text,
    quyu text,
    info text,
    create_time timestamp,
    xzqh text,
    ts_title text,
    bd_key bigint,
    person text,
    price float,

    zhaobiaoren text ,

    zhongbiaoren  text ,

    zbdl   text ,

    zhongbiaojia float ,

    kzj  float ,

    xmmc  text ,

    xmjl text ,

    xmjl_zsbh text ,

    xmdz  text , 

    zbfs text ,

    xmbh  text ,

    mine_info text primary key  ,
    person_key bigint,
    ent_key bigint 

    )
    distributed by(mine_info)

    """
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp_gp)

    cols=['html_key','quyu','zhaobiaoren','ent_key','zbdl']
    for col in cols:
        sql=" select * from pg_indexes where tablename='gg_meta_single' and indexname='idx_gg_meta_single_%s' "%col
        df=db_query(sql,dbtype="postgresql",conp=conp_gp)
        if df.empty:
            sql="create index idx_gg_meta_single_%s on app.gg_meta_single(%s)"%(col,col)
            print(sql)
            db_command(sql,dbtype="postgresql",conp=conp_gp)

 





def app_gg_meta_single_insert_into(conp_gp):
    bg=time.time()
    est_app_gg_meta_single(conp_gp)
    sql="truncate table app.gg_meta_single;"
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp_gp)

    quyus=forbiden_list
    quyus=','.join([ "'%s'"%w for w in quyus])
    sql="""
    insert into app.gg_meta_single(html_key,  guid,   gg_name,    href,   fabu_time,  ggtype, jytype, diqu    ,quyu   ,info   ,create_time,   xzqh,   ts_title    ,bd_key ,person ,price
    ,zhaobiaoren    ,zhongbiaoren   ,zbdl   ,zhongbiaojia   ,kzj    ,xmmc   ,xmjl   ,xmjl_zsbh, xmdz,   zbfs    ,xmbh,  mine_info,person_key,ent_key)

    select distinct on(mine_info)  html_key,  guid,    app.title_clear(gg_name) as gg_name,    
    href,   
    fabu_time, case when ggtype='异常公告' then '流标公告' else ggtype end as  ggtype,
     jytype, diqu    ,quyu   ,info   ,create_time,   xzqh,   ts_title 
       ,bd_key ,person ,case when price::float <10000 then 0 else price::float end price
    ,zhaobiaoren    ,zhongbiaoren   ,zbdl   ,case when zhongbiaojia::float <10000 then 0 else zhongbiaojia::float end zhongbiaojia   
    ,case when kzj<10000 then 0 else kzj end kzj    ,xmmc   ,xmjl   ,xmjl_zsbh, xmdz,   zbfs    ,xmbh,  mine_info,person_key,ent_key
     from dst.gg_meta where quyu not in (%s) and trim(gg_name)!=''
     order by mine_info,quyu desc,fabu_time asc
    """%quyus
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp_gp)


    #zlsys 地区 只展示招标 和中标 流 变
    sql="delete from app.gg_meta_single where quyu~'^zlsys' and ggtype !~'中|招|变|流' "
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp_gp)


    ed=time.time()
    cost=int(ed-bg)
    print("耗时%d 秒"%cost)

























###更新代码

def est_gg_meta(conp):
    sql="""
    CREATE  TABLE if not exists "public"."gg_meta" (
    "html_key" bigint primary key,
    "guid" text COLLATE "default",
    "gg_name" text COLLATE "default",
    "href" text COLLATE "default",
    "fabu_time" timestamp(6),
    "ggtype" text COLLATE "default",
    "jytype" text COLLATE "default",
    "diqu" text COLLATE "default",
    "quyu" text COLLATE "default",
    "info" text COLLATE "default",
    "create_time" timestamp(6),
    "xzqh" text COLLATE "default",
    "ts_title" tsvector,
    "bd_key" int8,
    "person" text COLLATE "default",
    "price" numeric NOT NULL default 0,
    zhaobiaoren text ,
    zhongbiaoren    text,
    zbdl text , 
    zhongbiaojia text   ,
    kzj float ,
    xmmc text , 
    xmjl text , 
    xmjl_zsbh text  ,
    xmdz text ,
    zbfs text ,
    xmbh text , 
    mine_info text ,
    person_key bigint ,
    ent_key bigint
    ) distributed by(html_key)"""

    db_command(sql,dbtype="postgresql",conp=conp)
    sql="grant select on table gg to app_reader"
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp)

def update_gg_meta(conp,conp_gp):
    
    app_gg_meta_single_insert_into(conp_gp)
    bg=time.time()
    est_gg_meta(conp)
    sql="""truncate public.gg_meta;"""
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp)
    def f(i):
        sql="""
        insert into "public".gg_meta(html_key,  guid,   gg_name,    href,   fabu_time,  ggtype, jytype, diqu    ,quyu   ,info   ,create_time,   xzqh,   ts_title    ,bd_key ,person ,price
        ,zhaobiaoren    ,zhongbiaoren   ,zbdl   ,zhongbiaojia   ,kzj    ,xmmc   ,xmjl   ,xmjl_zsbh, xmdz,   zbfs    ,xmbh,  mine_info,person_key,ent_key) 

        select   html_key,    guid,   gg_name,    href,   fabu_time,  ggtype, jytype, diqu    ,quyu   ,info   
        ,create_time,   xzqh,   ts_title::tsvector as ts_title  ,bd_key ,person ,coalesce(price::numeric,0) as price
        ,zhaobiaoren    ,zhongbiaoren   ,zbdl   , coalesce(zhongbiaojia::numeric,0) zhongbiaojia   ,coalesce(kzj::numeric,0) kzj    ,xmmc   ,xmjl   ,xmjl_zsbh, xmdz,   zbfs    ,xmbh,  mine_info
        ,case when person_key =0 then null else  person_key end  as person_key
        ,case when ent_key =0 then null else  ent_key end  as ent_key
         from et_gg_meta_%d 
        """%i
        print(sql)
        db_command(sql,dbtype="postgresql",conp=conp)
        ed=time.time()
        cost=int(ed-bg)
        print("gg_meta 全表重导累积耗时%s 秒"%cost)
    for i in range(1,30):
        f(i)
    #mythread(list(range(1,30)),f).run(3)

    ed=time.time()
    cost=int(ed-bg)
    print("gg_meta 全表重导入耗时%s 秒"%cost)