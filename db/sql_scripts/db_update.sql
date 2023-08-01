update bot_users
set agreement = true
where telegram_id = $1;


update bot_users
set full_name = $1, birth_date = $2
where telegram_id = $3;


update sessions
set available_session_id = $1
where id = $2