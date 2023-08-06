from zlapp import app_settings
import time 
from lmf.dbv2 import db_command,db_query,db_write
import traceback
from lmf.bigdata import pg2pg 
from sqlalchemy.dialects.postgresql import  TEXT,BIGINT,TIMESTAMP,NUMERIC

def est_app_qy_query_quyu(quyu,conp_gp):
    sql="""
    CREATE unlogged TABLE if not exists "etl"."app_qy_query_%s" (
    "html_key" int8,
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
    distributed by (ent_key)"""%quyu
    db_command(sql,dbtype="postgresql",conp=conp_gp)

def pre_quyu_cdc(quyu,conp_gp):
    est_app_qy_query_quyu(quyu,conp_gp)
    sql="truncate table etl.app_qy_query_%s;"%quyu
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp_gp)
    sql1="""
    insert into etl.app_qy_query_anhui_anqing_ggzy(html_key,   href    ,ggtype ,quyu,  entname ,entrole,   price   ,diqu,  xzqh,   fabu_time,  gg_name,    ent_key)
         with a as (SELECT html_key,href,ggtype,quyu
        ,zhongbiaoren as entname ,'中标人'::text entrole
        ,zhongbiaojia::float as price  ,diqu,xzqh,fabu_time,gg_name,ent_key
         FROM app.gg_meta_single t  where exists(select 1 from etl.gg_meta_anhui_anqing_ggzy t1 where t.ent_key=t1.ent_key) and ent_key is not null
         )
        ,b as (SELECT html_key,href,ggtype,quyu
        ,zhaobiaoren as entname ,'招标人'::text entrole
        ,kzj::float as price  ,diqu,xzqh,fabu_time,gg_name,public.add(encode(digest(zhaobiaoren,'md5'),'hex'))::bigint as ent_key
         FROM app.gg_meta_single t where zhaobiaoren  is not null  and exists(select 1 from etl.gg_meta_anhui_anqing_ggzy t1 where t.zhaobiaoren=t1.zhaobiaoren) 
         )
        ,c as (SELECT html_key,href,ggtype,quyu
        ,zbdl as entname ,'招标代理'::text entrole
        ,kzj::float as price  ,diqu,xzqh,fabu_time,gg_name,public.add(encode(digest(zbdl,'md5'),'hex'))::bigint as ent_key
         FROM app.gg_meta_single t where zbdl  is not null  and exists(select 1 from etl.gg_meta_anhui_anqing_ggzy t1 where t.zbdl=t1.zbdl) 
         )
        , d as (
         select * from a union  select * from b union select * from c)
    select html_key,   href    ,ggtype ,quyu,  entname ,entrole,   price   ,diqu,  xzqh,   fabu_time,  gg_name,    ent_key from d 
    """
    sql1=sql1.replace("anhui_anqing_ggzy",quyu)

    db_command(sql1,dbtype="postgresql",conp=conp_gp)

    cnt=db_query("select count(*) from etl.app_qy_query_%s "%quyu,dbtype="postgresql",conp=conp_gp).iat[0,0]
    print("etl.app_qy_query_%s :此次更新数据 %d 条"%(quyu,cnt))

def pre_quyu_cdc_1(quyu,loc='aliyun'):
    conp_gp=app_settings[loc]['conp_gp']
    pre_quyu_cdc(quyu,conp_gp)

def et_app_qy_query_quyu(quyu,conp_gp,conp_app5):
    user,passwd,host,db,schema=conp_gp
    sql="""
    drop external table if exists cdc.et_app_qy_query_anhui_anqing_ggzy;
    create  external table  cdc.et_app_qy_query_anhui_anqing_ggzy(
    "html_key" int8,
    "href" text,
    "ggtype" text,
    "quyu" text ,
    "entname" text,
    "entrole" text ,
    "price" numeric,
    "diqu" text ,
    "xzqh" text ,
    "fabu_time" timestamp(6),
    "gg_name" text ,
    "ent_key" int8
    )
    LOCATION ('pxf://etl.app_qy_query_anhui_anqing_ggzy?PROFILE=JDBC&JDBC_DRIVER=org.postgresql.Driver&DB_URL=jdbc:postgresql://%s/base_db&USER=%s&PASS=%s')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
    """%(host,user,passwd)

    sql=sql.replace("anhui_anqing_ggzy",quyu)

    db_command(sql,dbtype="postgresql",conp=conp_app5)




def insert_into(quyu,conp_gp,conp_app5):
    et_app_qy_query_quyu(quyu,conp_gp,conp_app5)
    sql="""
    delete from public.app_qy_query where ent_key in (select distinct ent_key from cdc.et_gg_zhongbiao_%s )
    """%(quyu)
    db_command(sql,dbtype="postgresql",conp=conp_app5)


    sql="""insert into public.app_qy_query(ent_key , entname, fddbr ,  clrq  ,  zczj   , xzqh  ,  qy_alias,    logo  ,  zhongbiaodate_latest  ,  zhongbiao_counts    
    ,qy_zz_codes ,qy_zz_info , ry_zz_codes, ry_zz_info , gg_info ,latest_gg_fabu_time ,gg_info_length , gg_zhongbiao_info ,  gg_zhongbiao_xzqhs)


     with a as (SELECT ent_key,entname,fddbr,clrq,zczj,xzqh, qy_alias,logo FROM "cdc"."et_qy_base_jiangsu_nantong_ggzy" )

    ,b as (select ent_key,max(fabu_time) zhongbiaodate_latest,count(*) zhongbiao_counts from cdc.et_qy_zhongbiao_jiangsu_nantong_ggzy where ent_key is not null group by ent_key )

    ,c as (SELECT ent_key, array_agg(json_build_object('zzmc',zzmc,'zzbh',zzbh,'zzcode',zzcode,'zzlb',zzlb)) as qy_zz_info,string_agg('code-'||zzcode,',') as qy_zz_codes

     FROM "cdc"."et_qy_zz_jiangsu_nantong_ggzy" where ent_key is not null and ent_key!=0 group by ent_key)
    
    ,d1 as (select person_key,max(fabu_time  ) fabu_time,count(*) ry_total
    from cdc.et_xmjl_zhongbiao_jiangsu_nantong_ggzy group by person_key)

    ,d as (
        select ent_key
    , array_agg(json_build_object( 'name',name,'zjhm',zjhm,'person_key',dd.person_key,'zclb',zclb,'zhuanye',zhuanye,'zsbh',zsbh
    ,'yzh',yzh,'youxiao_date',youxiao_date,'currentTotal',ry_total,'currentDate',fabu_time,'ryzz_code',ryzz_code ) order by dd.person_key  ) as ry_zz_info
    ,string_agg(concat('code-',ryzz_code),',') ry_zz_codes
     from cdc.et_qy_zcry_jiangsu_nantong_ggzy as dd left join  d1 on  dd.person_key=d1.person_key
      where ent_key is not null  and ent_key!=0

    group by ent_key 
    )

    ,e as (
    SELECT 
    ent_key 
    
    ,max(fabu_time) as latest_gg_fabu_time

    ,count(html_key) as gg_info_length
    ,array_agg(json_build_object('html_key',html_key,'gg_name',gg_name,'gg_type',ggtype,'fabu_time',fabu_time,'price',coalesce(price,0),'xzqh',xzqh) 
    order by fabu_time desc ,gg_name)filter(where entrole='中标人'  ) gg_zhongbiao_info
    ,string_agg(distinct concat('code-',xzqh),',') filter(where entrole='中标人'  )  gg_zhongbiao_xzqhs
    ,array_agg(json_build_object('html_key',html_key,'gg_name',gg_name,'gg_type',ggtype,'fabu_time',fabu_time,'price',coalesce(price,0),'xzqh',xzqh) order by fabu_time desc ,gg_name) gg_info
     FROM "cdc"."et_app_qy_query_jiangsu_nantong_ggzy"  
    where ent_key is not null and ent_key !=0

    group by ent_key)



    select a.ent_key,a.entname,fddbr,a.clrq::timestamp as clrq,zczj,a.xzqh,qy_alias,logo
    ,b.zhongbiaodate_latest,b.zhongbiao_counts 
    ,c.qy_zz_codes
    ,c.qy_zz_info
    ,d.ry_zz_codes

    ,d.ry_zz_info
    ,e.gg_info

    ,e.latest_gg_fabu_time
    ,e.gg_info_length
    ,e.gg_zhongbiao_info
    ,e.gg_zhongbiao_xzqhs
    
    from a left join b on a.ent_key=b.ent_key 
    left join c on a.ent_key=c.ent_key 
    left join d on a.ent_key=d.ent_key 
    left join e on a.ent_key=e.ent_key
    """
    sql=sql.replace("jiangsu_nantong_ggzy",quyu)
    db_command(sql,dbtype="postgresql",conp=conp_app5)

def insert_into_1(quyu,loc='aliyun'):
    conp_gp=app_settings[loc]['conp_gp']
    conp_app5=app_settings[loc]['conp_app5']
    insert_into(quyu,conp_gp,conp_app5)

# quyu="anhui_anqing_ggzy"
# conp_gp=['gpadmin','since2015','192.168.4.183:5433','base_db','etl']
# conp_app=['gpadmin','since2015','192.168.4.206','biaost','public']