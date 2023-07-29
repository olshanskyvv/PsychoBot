select * from bot_users where telegram_id = $1;

select * from services where id = $1;

select * from available_sessions where id = $1;

select * from sessions where id = $1;

select exists(select *
from sessions ss
where ss.bot_user_id = 1);

select date from available_sessions
where date = current_date + 1 and time_begin > current_time or
      date > current_date + 1 and date <= current_date + 7
group by date order by date;

select id, time_begin from available_sessions
where date = $1
order by time_begin;

select id from services
where name = 'Первичная консультация';