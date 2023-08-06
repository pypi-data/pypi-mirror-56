sql="""
create user app_reader with password 'since2015';

grant connect on database biaost to app_reader ;

revoke all on schema public from public ;


grant usage on schema public to app_reader;


grant select on all tables in schema public to app_reader ;

grant execute on all functions in schema public to app_reader ;

grant select on table public.app_qy_zz  to app_reader;
grant select on table public.app_qy_zcry  to app_reader;
grant select on table public.qy_zz  to app_reader;
grant select on table public.t_gg_ent_bridge  to app_reader;
grant select on table public.qy_base  to app_reader;
grant select on table public.bd_dt  to app_reader;
grant select on table public.app_gg_zhongbiao  to app_reader;
grant select on table public.t_bd_xflv  to app_reader;
grant select on table public.qy_zcry  to app_reader;
grant select on table public.qy_zhongbiao  to app_reader;
grant select on table public.et_gg_html  to app_reader;
grant select on table public.gg_zhongbiao  to app_reader;
grant select on table public.xmjl_zhongbiao  to app_reader;
grant select on table public.bd  to app_reader;
grant select on table public.et_qy_zz  to app_reader;
grant select on table public.et_qy_zcry  to app_reader;
grant select on table public.et_qy_base  to app_reader;
grant select on table public.et_t_person  to app_reader;
grant select on table public.app_qy_query  to app_reader;
grant select on table public.gg_meta  to app_reader;
grant select on table public.gg_1_prt_gg_prt_other  to app_reader;
grant select on table public.gg_1_prt_gg_prt_normal  to app_reader;
grant select on table public.gg  to app_reader;
grant select on table public.t_person  to app_reader;
grant select on table public.et_gg_meta  to app_reader;


"""