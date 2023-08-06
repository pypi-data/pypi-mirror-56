import time 
from lmf.dbv2 import db_command,db_query,db_write
import traceback
from lmf.bigdata import pg2pg 
from sqlalchemy.dialects.postgresql import  TEXT,BIGINT,TIMESTAMP,NUMERIC

def est_qy_zhongbiao_quyu(quyu,conp_gp):
    sql="""
    CREATE  unlogged TABLE if not exists "etl"."qy_zhongbiao_%s" (
    zhongbiaoren text,
    gg_name text,
    fabu_time timestamp,
    html_key  bigint,
    zhongbiaojia numeric,
    ent_key bigint not null
    )
    distributed by (ent_key)"""%quyu
    db_command(sql,dbtype="postgresql",conp=conp_gp)

def est_qy_base_quyu(quyu,conp_gp):
    sql="""
    CREATE  unlogged TABLE if not exists "etl"."qy_base_%s" (
    ent_key bigint,
    entname text,
    fddbr text,
    clrq text,
    zczj text,
    xzqh text,
    qy_alias text,
    logo text
   
    )
    distributed by (ent_key)"""%quyu
    db_command(sql,dbtype="postgresql",conp=conp_gp)


def est_qy_zz_quyu(quyu,conp_gp):
    sql="""
    CREATE  unlogged TABLE if not exists "etl"."qy_zz_%s" (
    ent_key bigint,
    zzmc text,
    zzbh text,
    zzcode text,
    zzlb text
    )
    distributed by (ent_key)"""%quyu
    db_command(sql,dbtype="postgresql",conp=conp_gp)

def est_qy_zcry_quyu(quyu,conp_gp):
    sql="""
    CREATE  unlogged TABLE if not exists "etl"."qy_zcry_%s" (
    ent_key bigint,
    person_key bigint,
    name text,
    zj_type text,
    gender text,
    zjhm text,
    zclb text,
    zhuanye text,
    zsbh   text,
    yzh   text,
    youxiao_date text,
    ryzz_code  text,
    entname text,
    xzqh text
    )
    distributed by (ent_key)"""%quyu
    db_command(sql,dbtype="postgresql",conp=conp_gp)





def pre_quyu_cdc(quyu,conp_gp):
    est_qy_zhongbiao_quyu(quyu,conp_gp)
    est_qy_base_quyu(quyu,conp_gp)
    est_qy_zz_quyu(quyu,conp_gp)
    est_qy_zcry_quyu(quyu,conp_gp)
    sql="truncate table etl.qy_zhongbiao_%s;"%quyu
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp_gp)

    sql="truncate table etl.qy_base_%s;"%quyu
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp_gp)

    sql="truncate table etl.qy_zz_%s;"%quyu
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp_gp)

    sql="truncate table etl.qy_zcry_%s;"%quyu
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp_gp)

    sql1="""
    insert into etl.qy_zhongbiao_%s(zhongbiaoren  ,  gg_name ,fabu_time ,  html_key  ,  zhongbiaojia  ,  ent_key)
   SELECT  zhongbiaoren
    ,gg_name 

    ,fabu_time 

    ,html_key

    ,zhongbiaojia 
    ,ent_key
     FROM "app"."gg_meta_single"  where ent_key is not null and ent_key in (SELECT distinct ent_key FROM "etl"."gg_zhongbiao_%s" )    

    """%(quyu,quyu)
    ##select a.*,b.ent_key  from a left join  "public".qy_base  as b on a.zhongbiaoren=b.jgmc
    db_command(sql1,dbtype="postgresql",conp=conp_gp)
    cnt=db_query("select count(*) from etl.qy_zhongbiao_%s "%quyu,dbtype="postgresql",conp=conp_gp).iat[0,0]
    print("etl.qy_zhongbiao_%s :此次更新数据 %d 条"%(quyu,cnt))


    sql2="""
    insert into etl.qy_base_%s(ent_key, entname,fddbr,clrq,zczj,xzqh,qy_alias,logo)
    SELECT  ent_key,jgmc as entname,fddbr,clrq,zczj,xzqh,alias as qy_alias,logo
     FROM "public"."qy_base"  where ent_key is not null and ent_key in (SELECT distinct ent_key FROM "etl"."gg_zhongbiao_%s" )    

    """%(quyu,quyu)
    ##select a.*,b.ent_key  from a left join  "public".qy_base  as b on a.zhongbiaoren=b.jgmc
    db_command(sql2,dbtype="postgresql",conp=conp_gp)
    cnt=db_query("select count(*) from etl.qy_base_%s "%quyu,dbtype="postgresql",conp=conp_gp).iat[0,0]
    print("etl.qy_base_%s :此次更新数据 %d 条"%(quyu,cnt))

    sql3="""
    insert into etl.qy_zz_%s(    ent_key ,zzmc ,zzbh ,zzcode ,zzlb  )
    SELECT  ent_key ,zzmc ,zzbh ,zzcode ,zzlb 
     FROM "public"."qy_zz"  where ent_key is not null and ent_key in (SELECT distinct ent_key FROM "etl"."gg_zhongbiao_%s" )    

    """%(quyu,quyu)
    ##select a.*,b.ent_key  from a left join  "public".qy_base  as b on a.zhongbiaoren=b.jgmc
    db_command(sql3,dbtype="postgresql",conp=conp_gp)
    cnt=db_query("select count(*) from etl.qy_zz_%s "%quyu,dbtype="postgresql",conp=conp_gp).iat[0,0]
    print("etl.qy_zz_%s :此次更新数据 %d 条"%(quyu,cnt))

    sql4="""
    insert into etl.qy_zcry_%s(ent_key ,person_key,name ,zj_type ,gender,zjhm,zclb ,zhuanye,zsbh , yzh ,youxiao_date,ryzz_code,entname,xzqh   )
    SELECT  ent_key ,person_key,name,    zj_type ,gender , ,zjhm,zclb ,zhuanye,zsbh , yzh ,youxiao_date,ryzz_code ,entname,xzqh 
     FROM "public"."qy_zcry"  where ent_key is not null and ent_key in (SELECT distinct ent_key FROM "etl"."gg_zhongbiao_%s" )    
    """%(quyu,quyu)
    ##select a.*,b.ent_key  from a left join  "public".qy_base  as b on a.zhongbiaoren=b.jgmc
    db_command(sql3,dbtype="postgresql",conp=conp_gp)
    cnt=db_query("select count(*) from etl.qy_zcry_%s "%quyu,dbtype="postgresql",conp=conp_gp).iat[0,0]
    print("etl.qy_zcry_%s :此次更新数据 %d 条"%(quyu,cnt))



#insert into
def et_qy_zhongbiao_quyu(quyu,conp_gp,conp_app5):
    user,passwd,host,db,schema=conp_gp
    sql="""
    drop external table if exists cdc.et_qy_zhongbiao_anhui_anqing_ggzy;
    create  external table  cdc.et_qy_zhongbiao_anhui_anqing_ggzy(
    zhongbiaoren text,
    gg_name text,
    fabu_time timestamp,
    html_key  bigint,
    zhongbiaojia numeric,
    ent_key bigint
    )
    LOCATION ('pxf://etl.qy_zhongbiao_anhui_anqing_ggzy?PROFILE=JDBC&JDBC_DRIVER=org.postgresql.Driver&DB_URL=jdbc:postgresql://%s/base_db&USER=%s&PASS=%s')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    """%(host,user,passwd)

    sql=sql.replace("anhui_anqing_ggzy",quyu)

    db_command(sql,dbtype="postgresql",conp=conp_app5)

def et_qy_base_quyu(quyu,conp_gp,conp_app5):
    user,passwd,host,db,schema=conp_gp
    sql="""
    drop external table if exists cdc.et_qy_base_anhui_anqing_ggzy;
    create  external table  cdc.et_qy_base_anhui_anqing_ggzy(
    ent_key bigint,
    entname text,
    fddbr text,
    clrq text,
    zczj text,
    xzqh text,
    qy_alias text,
    logo text
    )
    LOCATION ('pxf://etl.qy_base_anhui_anqing_ggzy?PROFILE=JDBC&JDBC_DRIVER=org.postgresql.Driver&DB_URL=jdbc:postgresql://%s/base_db&USER=%s&PASS=%s')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    """%(host,user,passwd)

    sql=sql.replace("anhui_anqing_ggzy",quyu)

    db_command(sql,dbtype="postgresql",conp=conp_app5)

def et_qy_zz_quyu(quyu,conp_gp,conp_app5):
    user,passwd,host,db,schema=conp_gp
    sql="""
    drop external table if exists cdc.et_qy_zz_anhui_anqing_ggzy;
    create  external table  cdc.et_qy_zz_anhui_anqing_ggzy(
    ent_key bigint,
    zzmc text,
    zzbh text,
    zzcode text,
    zzlb text
    )
    LOCATION ('pxf://etl.qy_zz_anhui_anqing_ggzy?PROFILE=JDBC&JDBC_DRIVER=org.postgresql.Driver&DB_URL=jdbc:postgresql://%s/base_db&USER=%s&PASS=%s')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    """%(host,user,passwd)

    sql=sql.replace("anhui_anqing_ggzy",quyu)

    db_command(sql,dbtype="postgresql",conp=conp_app5)

def et_qy_zcry_quyu(quyu,conp_gp,conp_app5):
    user,passwd,host,db,schema=conp_gp
    sql="""
    drop external table if exists cdc.et_qy_zcry_anhui_anqing_ggzy;
    create  external table  cdc.et_qy_zcry_anhui_anqing_ggzy(
    ent_key bigint,
    person_key bigint,
    name text,
    zj_type  text,
    gender text,
    zjhm text,
    zclb text,
    zhuanye text,
    zsbh   text,
    yzh   text,
    youxiao_date text,
    ryzz_code  text,
    entname text,
    xzqh text
    )
    LOCATION ('pxf://etl.qy_zcry_anhui_anqing_ggzy?PROFILE=JDBC&JDBC_DRIVER=org.postgresql.Driver&DB_URL=jdbc:postgresql://%s/base_db&USER=%s&PASS=%s')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    """%(host,user,passwd)

    sql=sql.replace("anhui_anqing_ggzy",quyu)

    db_command(sql,dbtype="postgresql",conp=conp_app5)



def insert_into(quyu,conp_gp,conp_app5):
    et_qy_zhongbiao_quyu(quyu,conp_gp,conp_app5)
    et_qy_zz_quyu(quyu,conp_gp,conp_app5)
    et_qy_base_quyu(quyu,conp_gp,conp_app5)
    et_qy_zcry_quyu(quyu,conp_gp,conp_app5)
    sql="""
    delete from public.qy_zhongbiao where ent_key in (select distinct ent_key from cdc.et_qy_zhongbiao_%s )
    """%(quyu)
    db_command(sql,dbtype="postgresql",conp=conp_app5)


    sql="""insert into public.qy_zhongbiao(ent_key ,gg_names,gg_fabutimes,html_keys,zhongbiaojias,zhongbiao_counts,zhongbiaoren)
    select ent_key
   ,array_agg(gg_name order by fabu_time desc ) as gg_names 


    ,array_agg(fabu_time order by fabu_time desc) gg_fabutimes

    ,array_agg(html_key order by fabu_time desc) html_keys

    ,array_agg(coalesce(zhongbiaojia::numeric,0) order by fabu_time desc ) as zhongbiaojias 
    
    ,count(*) zhongbiao_counts
    ,(array_agg(zhongbiaoren  ))[1] as zhongbiaoren 
            from cdc.et_qy_zhongbiao_%s group by ent_key
    """%quyu
    db_command(sql,dbtype="postgresql",conp=conp_app5)



# quyu="anhui_anqing_ggzy"
# conp_gp=['gpadmin','since2015','192.168.4.183:5433','base_db','etl']
# conp_app=['gpadmin','since2015','192.168.4.206','biaost','public']