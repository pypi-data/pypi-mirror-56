from lmf.dbv2 import db_query ,db_command 

import os 

f_names=['public.get_search_gg','public.get_gg','public.get_qy_name_list_pc','public.get_qy_by_zz','public.get_qy_by_ry'
,'public.get_xmjl_list_pc'
]

f_dirname=os.path.dirname(__file__)
def est_func(f_name,conp=None):
    conp=['postgres','since2015','192.168.4.207','biaost','public']
    #f_name='public.get_search_gg'
    f_name=f_name.replace('.','_')
    path=os.path.join(f_dirname,'%s.sql'%f_name)

    with open(path,'r',encoding='utf8') as f :

        sql=f.read()

    db_command(sql,dbtype="postgresql",conp=conp)

