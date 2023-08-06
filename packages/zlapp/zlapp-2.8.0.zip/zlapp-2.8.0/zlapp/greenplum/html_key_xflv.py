import time 
from lmf.dbv2 import db_command,db_query
import traceback
from lmf.bigdata import pg2pg 
from sqlalchemy.dialects.postgresql import  TEXT,BIGINT,TIMESTAMP,NUMERIC
import time 
from datetime import datetime

def est_html_key_xflv(conp):
    sql="""
    create table if not exists html_key_xflv 
    (html_key bigint primary key  , 
    bd_key bigint,
    xflv float) distributed by (html_key)"""
    db_command(sql,dbtype="postgresql",conp= conp)



def update_html_key_xflv(conp):
    bg=time.time()
    est_html_key_xflv(conp)
    sql="truncate public.html_key_xflv;"
    db_command(sql,dbtype="postgresql",conp=conp)
    sql="""
    insert into "public".html_key_xflv 

    SELECT distinct on(html_key) a.html_key,a.bd_key,b.xflv 

     FROM "public"."gg"  as a , t_bd_xflv as b

    where  a.bd_key=b.bd_key;

        """
    print(sql)
    

    db_command(sql,dbtype="postgresql",conp=conp)

    ed=time.time()

    cost=int(ed-bg)

    print("html_key_xflv 全表耗时%d"%cost)