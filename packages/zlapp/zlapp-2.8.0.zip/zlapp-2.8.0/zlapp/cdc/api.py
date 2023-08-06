from zlapp import app_settings
from zlapp.cdc import gg_meta,t_gg_ent_bridge
from zlapp.cdc import gg ,gg_zhongbiao,qy_zhongbiao,app_qy_zz
from zlapp.cdc import app_ry_query,app_qy_zcry,app_qy_query,bd_dt,xmjl_zhongbiao
from zlapp.cdc import  gg_html ,gg_html_algo,t_bd_xflv
import time 

from lmf.dbv2 import db_query,db_command ,db_write 
from lmf.bigdata import pg2pg 
from sqlalchemy.dialects.postgresql import  TEXT,BIGINT,TIMESTAMP,NUMERIC
from traceback import print_exc


def pre_meta(loc='aliyun'):
    conp_app=list(app_settings[loc]['conp_app5'])
    conp_gp=list(app_settings[loc]['conp_gp'])
    sql="""
    with a as (select  
    quyu,max(html_key) as max_gg_meta
    from "public".gg_meta group by quyu )
    ,b as (
    select  
    quyu,max(html_key) as max_gg
    from "public".gg group by quyu
    )
    ,c as (
    select  
    quyu,max(html_key) as max_gg_zhongbiao
    from "public".gg_zhongbiao group by quyu
    )
    select a.*, coalesce(max_gg,0) max_gg, coalesce(max_gg_zhongbiao,0)  max_gg_zhongbiao from a left join b on a.quyu=b.quyu left join c on a.quyu=c.quyu 
    """
    df=db_query(sql,dbtype="postgresql",conp=conp_app)
    conp_gp[4]='etlmeta'
    db_write(df,'t_html_key',dbtype="postgresql",conp=conp_gp)


def pre_quyu(quyu,tb,loc):
    conp_gp=list(app_settings[loc]['conp_gp'])
    f=eval("%s.pre_quyu_cdc"%tb)
    key=f(quyu,conp_gp)
    if key is not None:return key

def del_quyu(quyu,tb,loc):
    conp_gp=list(app_settings[loc]['conp_gp'])
    conp_app5=app_settings[loc]['conp_app5']
    f=eval("%s.del_quyu"%tb)
    f(quyu,conp_gp,conp_app5)

def insert_into(quyu,tb,loc):
    conp_gp=list(app_settings[loc]['conp_gp'])
    conp_app5=list(app_settings[loc]['conp_app5'])
    conp_app1=list(app_settings[loc]['conp_app1'])
    f=eval("%s.insert_into"%tb)
    if tb in ['gg_html','gg_html_algo']:
        f(quyu,conp_gp,conp_app1)
    else:
        f(quyu,conp_gp,conp_app5)


def quyu_not_exists(quyu,conp_gp):
    df=db_query("select quyu from etlmeta.t_html_key ",dbtype="postgresql",conp=conp_gp)
    if quyu not in df['quyu'].tolist():
        db_command("insert into etlmeta.t_html_key(quyu, max_gg_meta,max_gg  ,max_gg_zhongbiao) values('%s',0,0,0)"%quyu,dbtype="postgresql",conp=conp_gp)


def add_quyu_app(quyu,loc="aliyun"):
    bg=time.time()
    conp_app5=app_settings[loc]['conp_app5']
    conp_gp=app_settings[loc]['conp_gp']
    conp_app1=app_settings[loc]['conp_app1']
    quyu_not_exists(quyu,conp_gp)
    print("---------------------------add--dst(%s)-->app---------------------------------"%quyu)
    max_html_key1=pre_quyu(quyu,'gg_meta',loc)
    if max_html_key1 is  None:
        ed=time.time()
        cost=int(ed-bg)
        print("%d 秒"%cost)
        return None
    max_html_key2=pre_quyu(quyu,'gg',loc)

    max_html_key3=pre_quyu(quyu,'gg_zhongbiao',loc)


    tbs=['gg_html','t_gg_ent_bridge','bd_dt','t_bd_xflv','xmjl_zhongbiao','qy_zhongbiao','app_qy_zcry','app_qy_query','app_ry_query']
    for tb in tbs:
        pre_quyu(quyu,tb,loc)


    if max_html_key1 is None:
        print("更新后最大html_key :",max_html_key1)
        ed=time.time()
        cost=int(ed-bg)
        print("%d 秒"%cost)
        return None
    print("待插入数据准备完成,即将往app里insert ")
    try:
        insert_into(quyu,'gg_meta',loc)
    except:
        print_exc()
    sql="update etlmeta.t_html_key set max_gg_meta=%d where quyu='%s' "%(max_html_key1,quyu)
    db_command(sql,dbtype='postgresql',conp=conp_gp)
    print("更新后最大html_key :",max_html_key1)

    try:
        insert_into(quyu,'gg',loc)
    except:
        print_exc()
    if max_html_key2 is not None:
        sql="update etlmeta.t_html_key set max_gg=%d where quyu='%s' "%(max_html_key2,quyu)
        db_command(sql,dbtype='postgresql',conp=conp_gp)
        print("更新后最大html_key :",max_html_key2)


 
    try:
        insert_into(quyu,'gg_zhongbiao',loc)
    except:
        print_exc()
    if max_html_key3 is not None: 
        sql="update etlmeta.t_html_key set max_gg_zhongbiao=%d where quyu='%s' "%(max_html_key3,quyu)
        db_command(sql,dbtype='postgresql',conp=conp_gp)
        print("更新后最大html_key :",max_html_key3)

    tbs=['t_gg_ent_bridge','bd_dt','t_bd_xflv','xmjl_zhongbiao','qy_zhongbiao','app_qy_zcry','app_qy_query','app_ry_query','gg_html']
    for tb in tbs:
        try:
            print(tb)
            insert_into(quyu,tb,loc)
        except:
            print_exc()


    ed=time.time()
    cost=int(ed-bg)
    print("%s--add_quyu_app:耗时%d 秒"%(quyu,cost))



def restart_quyu_app(quyu,loc="aliyun"):
    bg=time.time()
    for tb in ['gg_meta','gg','gg_zhongbiao']:
        print("restart-del--%s"%quyu)
        del_quyu(quyu,tb,loc)

    print("add_quyu_app")
    add_quyu_app(quyu,loc)

    ed=time.time()
    cost=int(ed-bg)
    print("%s--restart_quyu_app:耗时%d秒"%(quyu,cost))
