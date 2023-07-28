select * from bot_users where telegram_id = $1;

select * from services where id = $1;

select * from available_sessions where id = $1;

select * from sessions where id = $1;