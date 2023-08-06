import time 
from lmf.dbv2 import db_command,db_query
import traceback
from lmf.bigdata import pg2pg 
from sqlalchemy.dialects.postgresql import  TEXT,BIGINT,TIMESTAMP,NUMERIC
import time 


def est_app_qy_query(conp):
    sql="""
    CREATE  TABLE if not exists "public"."app_qy_query" (
    "ent_key" int4 primary key,
    "entname" varchar(500) COLLATE "default",
    "fddbr" text COLLATE "default",
    "clrq" timestamp(6),
    "zczj" text COLLATE "default",
    "xzqh" text COLLATE "default",
    "qy_alias" text COLLATE "default",
    "logo" text COLLATE "default",
    "zhongbiaodate_latest" timestamp(6),
    "zhongbiao_counts" int8,
    "qy_zz_codes" text COLLATE "default",
    "qy_zz_info" json[] ,
    "ry_zz_codes" text COLLATE "default",
    "ry_zz_info" json[],
    "gg_info" json[],
    "latest_gg_fabu_time" timestamp,
    "gg_info_length" int,
    "gg_zhongbiao_info" json[],
    "gg_zhongbiao_xzqhs" text
    )
    distributed by(ent_key)"""

    

    db_command(sql,dbtype="postgresql",conp= conp)
    sql="grant select on table app_qy_query to app_reader"
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp)


def update_app_qy_query(conp):
    bg=time.time()
    est_app_qy_query(conp)
    sql="truncate public.app_qy_query;"
    db_command(sql,dbtype="postgresql",conp=conp)
    sql="""
    insert into "public".app_qy_query(ent_key , entname, fddbr ,  clrq  ,  zczj   , xzqh  ,  qy_alias,    logo  ,  zhongbiaodate_latest  ,  zhongbiao_counts    
    ,qy_zz_codes ,qy_zz_info , ry_zz_codes, ry_zz_info , gg_info ,latest_gg_fabu_time ,gg_info_length , gg_zhongbiao_info ,  gg_zhongbiao_xzqhs) 

    with a as (SELECT ent_key,jgmc as entname,fddbr,clrq,zczj,xzqh,alias as qy_alias,logo FROM "public"."qy_base" )

    ,b as (select ent_key,gg_fabutimes[1] as zhongbiaodate_latest,zhongbiao_counts from public.qy_zhongbiao where ent_key is not null  )

    ,c as (SELECT ent_key, array_agg(json_build_object('zzmc',zzmc,'zzbh',zzbh,'zzcode',zzcode,'zzlb',zzlb)) as qy_zz_info,string_agg('code-'||zzcode,',') as qy_zz_codes

     FROM "public"."qy_zz" where ent_key is not null and ent_key!=0 group by ent_key)

    ,d as (
        select ent_key
    , array_agg(json_build_object( 'name',name,'zjhm',zjhm,'person_key',person_key,'zclb',zclb,'zhuanye',zhuanye,'zsbh',zsbh
    ,'yzh',yzh,'youxiao_date',youxiao_date,'currentTotal',ry_total,'currentDate',fabu_time,'ryzz_code',ryzz_code ) order by person_key  ) as ry_zz_info
    ,string_agg(concat('code-',ryzz_code),',') ry_zz_codes
     from public.app_qy_zcry where ent_key is not null  and ent_key!=0

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
     FROM "public"."t_gg_ent_bridge" 
    where ent_key is not null

    group by ent_key)


    select a.* ,b.zhongbiaodate_latest,b.zhongbiao_counts 
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
    print(sql)
    

    db_command(sql,dbtype="postgresql",conp=conp)

    ed=time.time()

    cost=int(ed-bg)

    print("app_qy_query 全表耗时%d"%cost)