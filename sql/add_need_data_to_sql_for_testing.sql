CREATE view view_rule_interruption AS 
select 
  b.rule_interruption_id,
  a.mxid,
  b.description,
  b.time_create,
  b.active_rule_interruption as active
  from tbl_users_info as a 
  LEFT JOIN tbl_rule_interruptions as b ON a.user_id = b.user_id 
  order by b.time_create;
