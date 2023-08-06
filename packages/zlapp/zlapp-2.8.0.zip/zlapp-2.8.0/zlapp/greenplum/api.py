
import time
from zlapp import app_settings
from zlapp.greenplum.api_dag import  tbdag  

#重新生成单个表
def update_tb(name,loc='aliyun',**krg):
    para={"max_html_key":None}
    para.update(krg)
    exec("from zlapp.greenplum import %s"%name)

    f=eval('%s.update_%s'%(name,name))
    conp_app5=list(app_settings[loc]['conp_app5'])
    conp_gp=list(app_settings[loc]['conp_gp'])
    conp_app1=list(app_settings[loc]['conp_app1'])


    if name in ['gg_html','gg_html_algo']:
        max_html_key=para['max_html_key']
        f(conp_gp,conp_app1,max_html_key)
    elif name in ['qy_zz','qy_base','qy_zcry','t_person'] :
        print("app5中%s 更新"%name)
        f(conp_app5)
    elif name in ['gg_meta']:
        f(conp_app5,conp_gp)
    else:
        f(conp_app5)


#重新生成表的所有拓扑序列
def plan_tb(name,loc='aliyun'):
    print(time.asctime(time.localtime()))
    if name=='all':
        plan_tb('gg_meta')
        update_tb('gg_html')
        return 
    tbs=tbdag.tplist(name)
    print("准备更新tbs--",tbs)
    for tb in tbs:
        print("本次更新计划--",tb)
        update_tb(tb,loc)
    print(time.asctime(time.localtime()))











