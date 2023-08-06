import time 
from lmf.dbv2 import db_command,db_query,db_write
import traceback
from lmf.bigdata import pg2pg 
from sqlalchemy.dialects.postgresql import  TEXT,BIGINT,TIMESTAMP,NUMERIC
import time 

def est_gg_meta_quyu(quyu,conp_gp):
    sql="""
    CREATE unlogged TABLE if not exists etl.gg_meta_%s (
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
    price text,
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

    mine_info text,
    person_key bigint,
    ent_key bigint   
    )
    distributed by(html_key)
    """%(quyu)
    db_command(sql,dbtype='postgresql',conp=conp_gp)



def get_max_html_key(quyu,conp_gp):
    max_html_key=db_query("select max_gg_meta from etlmeta.t_html_key where quyu='%s'"%quyu,dbtype="postgresql",conp=conp_gp).iat[0,0]

    return max_html_key

def pre_quyu_cdc(quyu,conp_gp):
    max_html_key=get_max_html_key(quyu,conp_gp)
    print("gg_meta 更新前最大html_key :",max_html_key)
    est_gg_meta_quyu(quyu,conp_gp)
    sql="truncate table etl.gg_meta_%s;"%quyu
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp_gp)
    if not quyu.startswith('zlsys'):
        sql0="""insert into app.gg_meta_single(html_key,  guid,   gg_name,    href,   fabu_time,  ggtype, jytype, diqu    ,quyu   ,info   ,create_time,   xzqh,  
         ts_title    ,bd_key ,person ,price
        ,zhaobiaoren    ,zhongbiaoren   ,zbdl   ,zhongbiaojia   ,kzj    ,xmmc   ,xmjl   ,xmjl_zsbh, xmdz,   zbfs    ,xmbh,  mine_info,person_key,ent_key)

         select  distinct on (mine_info)   
        html_key,  guid,   app.title_clear(gg_name) as gg_name,    href,   fabu_time,
         case when ggtype='异常公告' then '流标公告' else ggtype end as  ggtype,
           jytype, diqu    ,quyu   ,info   ,create_time,   xzqh,  
         ts_title    ,bd_key ,person ,case when price::float <10000 then 0 else price::float end price 
        ,zhaobiaoren    ,zhongbiaoren   ,zbdl   ,case when zhongbiaojia::float <10000 then 0 else zhongbiaojia::float end zhongbiaojia    ,case when kzj<10000 then 0 else kzj end kzj    
         ,xmmc   ,xmjl   ,xmjl_zsbh, xmdz,   zbfs    ,xmbh,  mine_info,person_key,ent_key

         from dst.gg_meta_1_prt_%s as b  where html_key>%d 
        and not exists(select 1 from app.gg_meta_single as a where a.mine_info=b.mine_info ) 
        """%(quyu,max_html_key)
    else:
        sql0="""insert into app.gg_meta_single(html_key,  guid,   gg_name,    href,   fabu_time,  ggtype, jytype, diqu    ,quyu   ,info   ,create_time,   xzqh,  
         ts_title    ,bd_key ,person ,price
        ,zhaobiaoren    ,zhongbiaoren   ,zbdl   ,zhongbiaojia   ,kzj    ,xmmc   ,xmjl   ,xmjl_zsbh, xmdz,   zbfs    ,xmbh,  mine_info,person_key,ent_key)

         select  distinct on (mine_info)   
        html_key,  guid,   app.title_clear(gg_name) as gg_name,    href,   fabu_time,
         case when ggtype='异常公告' then '流标公告' else ggtype end as  ggtype,
           jytype, diqu    ,quyu   ,info   ,create_time,   xzqh,  
         ts_title    ,bd_key ,person ,case when price::float <10000 then 0 else price::float end price 
        ,zhaobiaoren    ,zhongbiaoren   ,zbdl   ,case when zhongbiaojia::float <10000 then 0 else zhongbiaojia::float end zhongbiaojia    ,case when kzj<10000 then 0 else kzj end kzj    
         ,xmmc   ,xmjl   ,xmjl_zsbh, xmdz,   zbfs    ,xmbh,  mine_info,person_key,ent_key

         from dst.gg_meta_1_prt_%s as b  where html_key>%d 
        and not exists(select 1 from app.gg_meta_single as a where a.mine_info=b.mine_info ) and  ggtype ~'中|招|变|流'
        """%(quyu,max_html_key)

    print("app_gg_single ----- %s区域更新"%quyu)
    db_command(sql0,dbtype="postgresql",conp=conp_gp) 


    sql1="insert into etl.gg_meta_%s select  * from app.gg_meta_single where quyu='%s' and html_key>%d "%(quyu,quyu,max_html_key)
    db_command(sql1,dbtype="postgresql",conp=conp_gp)
    df=db_query("select max(html_key),count(*) from etl.gg_meta_%s "%quyu,dbtype="postgresql",conp=conp_gp)

    cnt=df.iat[0,1]
    print("etl.gg_meta_%s :此次更新数据 %d 条,不需要更新"%(quyu,cnt))
    if cnt==0:return None
    max_html_key1=df.iat[0,0]

    return max_html_key1





####insert into 
def et_gg_meta_quyu(quyu,conp_gp,conp_app5):
    user,passwd,host,db,schema=conp_gp
    sql="""
    drop external table if exists cdc.et_gg_meta_anhui_anqing_ggzy;
    create  external table  cdc.et_gg_meta_anhui_anqing_ggzy(html_key bigint,
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
    price text,
    zhaobiaoren text,
    zhongbiaoren text,
    zbdl text,
    zhongbiaojia float,
    kzj float8,
    xmmc text,
    xmjl text,
    xmjl_zsbh text,
    xmdz text,
    zbfs text,
    xmbh text,
    mine_info text,
    person_key bigint,
    ent_key bigint
    )
    LOCATION ('pxf://etl.gg_meta_anhui_anqing_ggzy?PROFILE=JDBC&JDBC_DRIVER=org.postgresql.Driver&DB_URL=jdbc:postgresql://%s/base_db&USER=%s&PASS=%s')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    """%(host,user,passwd)

    sql=sql.replace("anhui_anqing_ggzy",quyu)

    db_command(sql,dbtype="postgresql",conp=conp_app5)


def insert_into(quyu,conp_gp,conp_app5):
    et_gg_meta_quyu(quyu,conp_gp,conp_app5)
    sql="""
    insert into "public".gg_meta(html_key,  guid,   gg_name,    href,   fabu_time,  ggtype, jytype, diqu    ,quyu   ,info   ,create_time,   xzqh,   ts_title    ,bd_key ,person ,price
    ,zhaobiaoren    ,zhongbiaoren   ,zbdl   ,zhongbiaojia   ,kzj    ,xmmc   ,xmjl   ,xmjl_zsbh, xmdz,   zbfs    ,xmbh,  mine_info,person_key,ent_key) 

    select html_key,    guid,   gg_name,    href,   fabu_time,  ggtype, jytype, diqu    ,quyu   ,info   
    ,create_time,   xzqh,   ts_title::tsvector as ts_title  ,bd_key ,person ,coalesce(price::numeric,0) as price
    ,zhaobiaoren    ,zhongbiaoren   ,zbdl   , coalesce(zhongbiaojia::numeric,0) zhongbiaojia   ,coalesce(kzj::numeric,0) kzj    ,xmmc   ,xmjl   ,xmjl_zsbh, xmdz,   zbfs    ,xmbh,  mine_info
    ,case when person_key =0 then null else  person_key end  as person_key
    ,case when ent_key =0 then null else  ent_key end  as ent_key
     from cdc.et_gg_meta_%s 
    """%(quyu)
    db_command(sql,dbtype="postgresql",conp=conp_app5)

def del_quyu(quyu,conp_gp,conp_app5):
    sql="update etlmeta.t_html_key set max_gg_meta=0 where quyu='%s';"%quyu
    db_command(sql,dbtype="postgresql",conp=conp_gp)
    print(sql)

    sql="delete from public.gg_meta where quyu='%s' "%quyu 
    db_command(sql,dbtype="postgresql",conp=conp_app5)
    print(sql)

