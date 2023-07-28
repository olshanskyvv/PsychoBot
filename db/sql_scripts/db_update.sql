update bot_users
set agreement = true
where telegram_id = $1;