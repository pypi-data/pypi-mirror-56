import time 
from lmf.dbv2 import db_command,db_query,db_write
import traceback
from lmf.bigdata import pg2pg 
from sqlalchemy.dialects.postgresql import  TEXT,BIGINT,TIMESTAMP,NUMERIC

def est_app_qy_zcry_quyu(quyu,conp_gp):
    sql="""
    CREATE unlogged TABLE if not exists "etl"."app_qy_zcry_%s" (
   "ent_key" int8 ,
    "person_key" int8 ,
    "qy_total" int8 ,
    "ry_total" int8 ,
    "fabu_time" timestamp(6)
    )
    distributed by (ent_key)"""%quyu
    db_command(sql,dbtype="postgresql",conp=conp_gp)

def pre_quyu_cdc(quyu,conp_gp):
    est_app_qy_zcry_quyu(quyu,conp_gp)
    sql="truncate table etl.app_qy_zcry_%s;"%quyu
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp_gp)

    sql1="""
    insert into etl."app_qy_zcry_jiangsu_nantong_ggzy"(ent_key ,person_key , qy_total  ,  ry_total    ,fabu_time)
    with a as (select ent_key,count(*) zhongbiao_counts from etl.qy_zhongbiao_jiangsu_nantong_ggzy group by ent_key)

    ,b as ( select person_key
    ,array_agg(fabu_time order by fabu_time desc) gg_fabutimes
    ,count(*) zhongbiao_counts
    from etl.xmjl_zhongbiao_jiangsu_nantong_ggzy group by person_key)


    SELECT 
    c.ent_key,c.person_key
    ,coalesce(a.zhongbiao_counts,0) as qy_total
    ,coalesce(b.zhongbiao_counts,0) as ry_total 
    ,b.gg_fabutimes[1] as fabu_time 

    FROM "public"."qy_zcry" as c inner join a on a.ent_key=c.ent_key left join b on b.person_key=c.person_key
 
       where c.ent_key is not null and length(name)>1
    """
    sql1=sql1.replace('jiangsu_nantong_ggzy',quyu)
    db_command(sql1,dbtype="postgresql",conp=conp_gp)
    cnt=db_query("select count(*) from etl.app_qy_zcry_%s "%quyu,dbtype="postgresql",conp=conp_gp).iat[0,0]
    print("etl.app_qy_zcry_%s :此次更新数据 %d 条"%(quyu,cnt))






def et_app_qy_zcry_quyu(quyu,conp_gp,conp_app5):
    user,passwd,host,db,schema=conp_gp

    sql="""
    drop external table if exists cdc.et_app_qy_zcry_anhui_anqing_ggzy;
    create  external table  cdc.et_app_qy_zcry_anhui_anqing_ggzy(
   "ent_key" int8 ,
    "person_key" int8 ,
    "qy_total" int8 ,
    "ry_total" int8 ,
    "fabu_time" timestamp(6)
    )
    LOCATION ('pxf://etl.app_qy_zcry_anhui_anqing_ggzy?PROFILE=JDBC&JDBC_DRIVER=org.postgresql.Driver&DB_URL=jdbc:postgresql://%s/base_db&USER=%s&PASS=%s')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    """%(host,user,passwd)

 
    sql=sql.replace("anhui_anqing_ggzy",quyu)

    db_command(sql,dbtype="postgresql",conp=conp_app5)


def insert_into(quyu,conp_gp,conp_app5):
    et_app_qy_zcry_quyu(quyu,conp_gp,conp_app5)
 

    sql="""update app_qy_zcry as a
    set qy_total=b.qy_total
    from  

    (select distinct  ent_key ,qy_total from cdc.et_app_qy_zcry_%s ) as b  where a.ent_key=b.ent_key 
    """%quyu
    db_command(sql,dbtype="postgresql",conp=conp_app5)

    sql="""
    update app_qy_zcry as a
    set ry_total=b.ry_total,fabu_time=b.fabu_time
    from 
    (select distinct  person_key ,ry_total,fabu_time from cdc.et_app_qy_zcry_%s ) as b  where a.person_key=b.person_key  and a.person_key is not null 
    """%quyu
    db_command(sql,dbtype="postgresql",conp=conp_app5)


#def insert_into(quyu,conp_gp,conp_app5):




# quyu="anhui_anqing_ggzy"
# conp_gp=['gpadmin','since2015','192.168.4.183:5433','base_db','etl']
# conp_app=['gpadmin','since2015','192.168.4.206','biaost','public']