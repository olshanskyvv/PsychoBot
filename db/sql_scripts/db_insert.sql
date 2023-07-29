insert into bot_users (telegram_id) values ($1);

insert into services (name, cost, duration, is_for_benefits)
values ($1, $2, $3, $4)
returning id;

insert into available_sessions (date, time_begin)
values ($1, $2)
returning id;

insert into sessions (bot_user_id, service_id, available_session_id)
values ($1, $2, $3)
returning id;

