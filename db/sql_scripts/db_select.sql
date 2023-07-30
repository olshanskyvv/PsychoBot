select * from bot_users where telegram_id = $1;

select * from services where id = $1;

select * from available_sessions where id = $1;

select * from sessions where id = $1;

select exists(select *
from sessions ss
where ss.bot_user_id = 1);

select date from available_sessions
where (date = current_date + 1 and time_begin > current_time or
      date > current_date + 1 and date <= current_date + 7) and
    id not in (select available_session_id from sessions)
group by date order by date;

select id, time_begin from available_sessions
where date = $1 and
      id not in (select available_session_id from sessions)
order by time_begin;

select id from services
where name = 'Первичная консультация';

select id, name, cost, duration from services
where cost > 0 and is_for_benefits = $1
order by name