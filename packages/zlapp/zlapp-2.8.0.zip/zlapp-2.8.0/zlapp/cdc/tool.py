from lmf.dbv2 import db_query,db_command 

#删除某类外部表
def del_etl(table):
    conp=['developer','zhulong!123','192.168.4.183:5433','base_db','public']
    sql="select tablename from pg_tables  where schemaname='etl' and tablename~'^%s_' order by tablename "%table

    df=db_query(sql,dbtype="postgresql",conp=conp)

    tables=df['tablename'].tolist()

    for tb in tables:

        sql="drop  table etl.%s"%tb 
        print(sql)
        db_command(sql,dbtype="postgresql",conp=conp)
