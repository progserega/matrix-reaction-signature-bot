create table tbl_users_info(
	user_id serial,
	mxid varchar(255) default null,
	room_id varchar(255) default null,
	signature varchar(255) default null,
	signature_author varchar(255) default null,
  signature_time_create timestamp DEFAULT null,
  signature_show boolean  DEFAULT TRUE,
	signature_description varchar(2048) default null,
  rule_interruption_active_count integer DEFAULT 0,
  rule_interruption_count_all integer DEFAULT 0,
	user_description varchar(2048) default null,
  user_description_time_create timestamp DEFAULT null,
	primary key( user_id )
);

comment on table tbl_users_info is 'Пользователи, их описание, подпись, количество замечаний от админа';
comment on column tbl_users_info.user_id is 'Числовой идентификатор пользователя в MATRIX';
comment on column tbl_users_info.mxid is 'Идентификатор пользователя в MATRIX';
comment on column tbl_users_info.room_id is 'Идентификатор комнаты, к которой относится информация';
comment on column tbl_users_info.signature is 'Подпись у пользователя';
comment on column tbl_users_info.signature_author is 'кто установил подпись (MXID)';
comment on column tbl_users_info.signature_time_create is 'Время создания подписи у пользователя';
comment on column tbl_users_info.signature_show is 'Флаг, определяющий показывать или нет подпись пользователя';
comment on column tbl_users_info.signature_description is 'Описание подписи';
comment on column tbl_users_info.rule_interruption_active_count is 'Текущее количество активных замечаний о нарушении правил пользователем';
comment on column tbl_users_info.rule_interruption_count_all is 'Общее количество нарушений правил пользователем за всю историю наблюдений';
comment on column tbl_users_info.user_description is 'Описание пользователя';
comment on column tbl_users_info.user_description_time_create is 'Время создания описания пользователя';


create table tbl_rule_interruptions (
	rule_interruption_id serial,
  user_id integer DEFAULT 0,
  rule_interruption_author varchar(255) NOT NULL,
  description varchar(2048) NOT NULL,
  time_create timestamp DEFAULT now(),
  active_rule_interruption boolean  DEFAULT TRUE,
  PRIMARY KEY (user_id)
);

comment on table tbl_rule_interruptions is 'Описание замечаний от админов';
comment on column tbl_rule_interruptions.rule_interruption_id is 'Числовой идентификатор замечания';
comment on column tbl_rule_interruptions.user_id is 'Числовой идентификатор пользователя в MATRIX';
comment on column tbl_rule_interruptions.rule_interruption_author is 'Кто вынес данное замечение (MXID)';
comment on column tbl_rule_interruptions.description is 'Описание замечания';
comment on column tbl_rule_interruptions.time_create is 'Время замечания';
comment on column tbl_rule_interruptions.active_rule_interruption is 'Является ли это замечание текущим (активным)';
