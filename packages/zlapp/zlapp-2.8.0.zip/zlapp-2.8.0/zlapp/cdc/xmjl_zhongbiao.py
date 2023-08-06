import time 
from lmf.dbv2 import db_command,db_query,db_write
import traceback
from lmf.bigdata import pg2pg 
from sqlalchemy.dialects.postgresql import  TEXT,BIGINT,TIMESTAMP,NUMERIC

def est_xmjl_zhongbiao_quyu(quyu,conp_gp):
    sql="""
    CREATE  unlogged TABLE if not exists "etl"."xmjl_zhongbiao_%s" (
    xmjl text,
    gg_name text,
    fabu_time timestamp,
    html_key  bigint,
    zhongbiaojia numeric,
    href text,
    xzqh text,
    person_key bigint  not null 
    )
    distributed by (person_key)"""%quyu
    db_command(sql,dbtype="postgresql",conp=conp_gp)

def pre_quyu_cdc(quyu,conp_gp):
    est_xmjl_zhongbiao_quyu(quyu,conp_gp)
    sql="truncate table etl.xmjl_zhongbiao_%s;"%quyu
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp_gp)

    sql1="""
    insert into etl.xmjl_zhongbiao_%s(xmjl  ,  gg_name ,fabu_time ,  html_key  ,  zhongbiaojia ,href,xzqh ,  person_key)
    SELECT  xmjl
    ,gg_name 

    ,fabu_time 

    ,html_key

    ,zhongbiaojia
    ,href
    ,xzqh 
    ,person_key

     FROM "app"."gg_meta_single"  as t1 where  exists (SELECT 1 FROM "etl"."gg_zhongbiao_%s" as t2 where t2.person_key =t1.person_key ) and person_key is not null

    """%(quyu,quyu)

    ##    select a.*,b.person_key  from a left join  "public".t_person  as b on a.xmjl_zsbh=b.xmjl_zsbh and a.xmjl=b.xmjl
    db_command(sql1,dbtype="postgresql",conp=conp_gp)
    cnt=db_query("select count(*) from etl.xmjl_zhongbiao_%s "%quyu,dbtype="postgresql",conp=conp_gp).iat[0,0]
    print("etl.xmjl_zhongbiao_%s :此次更新数据 %d 条"%(quyu,cnt))

def et_xmjl_zhongbiao_quyu(quyu,conp_gp,conp_app5):
    user,passwd,host,db,schema=conp_gp
    sql="""
    drop external table if exists cdc.et_xmjl_zhongbiao_anhui_anqing_ggzy;
    create  external table  cdc.et_xmjl_zhongbiao_anhui_anqing_ggzy(
    xmjl text,
    gg_name text,
    fabu_time timestamp,
    html_key  bigint,
    zhongbiaojia numeric,
    href text,
    xzqh  text,
    person_key bigint
    )
    LOCATION ('pxf://etl.xmjl_zhongbiao_anhui_anqing_ggzy?PROFILE=JDBC&JDBC_DRIVER=org.postgresql.Driver&DB_URL=jdbc:postgresql://%s/base_db&USER=%s&PASS=%s')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    """%(host,user,passwd)

    sql=sql.replace("anhui_anqing_ggzy",quyu)

    db_command(sql,dbtype="postgresql",conp=conp_app5)


def insert_into(quyu,conp_gp,conp_app5):
    et_xmjl_zhongbiao_quyu(quyu,conp_gp,conp_app5)
    sql="""
    delete from public.xmjl_zhongbiao where person_key in (select distinct person_key from cdc.et_xmjl_zhongbiao_%s )
    """%(quyu)
    db_command(sql,dbtype="postgresql",conp=conp_app5)


    sql="""insert into public.xmjl_zhongbiao(person_key ,gg_names,gg_fabutimes,html_keys,zhongbiaojias,zhongbiao_counts,xmjl)
    select person_key
   ,array_agg(gg_name order by fabu_time desc ) as gg_names 


    ,array_agg(fabu_time order by fabu_time desc) gg_fabutimes

    ,array_agg(html_key order by fabu_time desc) html_keys

    ,array_agg(coalesce(zhongbiaojia::numeric,0) order by fabu_time desc ) as zhongbiaojias 
    
    ,count(*) zhongbiao_counts
    ,(array_agg(xmjl  ))[1] as xmjl 
            from cdc.et_xmjl_zhongbiao_%s group by person_key
    """%quyu
    db_command(sql,dbtype="postgresql",conp=conp_app5)



def update(quyu,conp_gp,conp_app):
    print("----------------------%s 开始更新--------------------------------------- "%quyu)
    pre_qy_zhongbiao(quyu,conp_gp)
    insert_into(quyu,conp_app)


# quyu="anhui_anqing_ggzy"
# conp_gp=['gpadmin','since2015','192.168.4.183:5433','base_db','etl']
# conp_app=['gpadmin','since2015','192.168.4.206','biaost','public']