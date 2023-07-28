insert into bot_users (telegram_id) values ($1);

insert into services (id, name, cost, duration, is_for_benefits)
values (gen_random_uuid(), $1, $2, $3, $4)
returning id;

insert into available_sessions (id, date, time_begin)
values (gen_random_uuid(), $1, $2)
returning id;

insert into sessions (id, bot_user_id, service_id, available_session_id)
values (gen_random_uuid(), $1, $2, $3)
returning id;

