import time 
from lmf.dbv2 import db_command,db_query,db_write
import traceback
from lmf.bigdata import pg2pg 
from sqlalchemy.dialects.postgresql import  TEXT,BIGINT,TIMESTAMP,NUMERIC

def pre_quyu_cdc(quyu,conp_gp):
    print("共用 qy_base qy_zcry xmjl_zhongbiao qy_zhonbiao 数据")




def insert_into(quyu,conp_gp,conp_app5):
    sql="""
    delete from public.app_ry_query where person_key in (select distinct person_key from cdc.et_gg_zhongbiao_%s ) and person_key is not null
    """%(quyu)
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp_app5)

    sql="""
    insert into "public".app_ry_query (person_key,name,zj_type,zjhm,gender,ryzz_info,ent_key,entname,xzqh
    ,clrq   ,zczj,  fddbr,  qy_alias,   logo    ,ry_total   ,ry_latest_zhongbiao_time,  qy_total    ,ry_zhongbiao_info)

    with a as (
    select 
    person_key, 

    (array_agg(name))[1] as name ,
    (array_agg(zj_type))[1] as zj_type ,
    (array_agg(zjhm))[1] as zjhm ,
    (array_agg(gender))[1] as gender 
    ,array_agg(json_build_object('zclb',zclb,'zsbh',zsbh,'yzh',yzh,'zhuanye',zhuanye,'youxiao_date',youxiao_date,'ryzz_code',ryzz_code)) as ryzz_info 
    ,(array_agg(ent_key))[1] as ent_key 
    ,(array_agg(entname))[1] as entname 
    ,(array_agg(xzqh))[1] as xzqh 
    from cdc.et_qy_zcry_jiangsu_nantong_ggzy  where person_key!=0 and person_key is not null

    group by person_key 
    )

    ,c as (select person_key,count(*) as ry_total , max(fabu_time) ry_latest_zhongbiao_time  
     ,array_agg(json_build_object('html_key',html_key,'href',href,'gg_name',gg_name,'quyu',xzqh,'zhongbiaojia',zhongbiaojia,'fabu_time',fabu_time)  ORDER BY fabu_time desc) as ry_zhongbiao_info
    from cdc.et_xmjl_zhongbiao_jiangsu_nantong_ggzy group by person_key)
    
    , e as (select ent_key,count(*) as qy_total from cdc.et_qy_zhongbiao_jiangsu_nantong_ggzy  group by ent_key)

    select a.person_key,a.name,a.zj_type,a.zjhm,a.gender,a.ryzz_info
    ,a.ent_key,a.entname ,a.xzqh
    ,b.clrq::timestamp clrq,b.zczj,b.fddbr,b.qy_alias,b.logo
    ,coalesce(c.ry_total,0) as ry_total 
    ,c.ry_latest_zhongbiao_time

    ,coalesce(e.qy_total,0) as qy_total

    ,c.ry_zhongbiao_info 
     from a 
    left join "cdc".et_qy_base_jiangsu_nantong_ggzy as b on a.ent_key=b.ent_key

    left join c on a.person_key=c.person_key

    left join   e on a.ent_key=e.ent_key
    """
    sql=sql.replace("jiangsu_nantong_ggzy",quyu)
    db_command(sql,dbtype="postgresql",conp=conp_app5)