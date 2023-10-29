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
where date = $1 and time_begin > $2 and
      id not in (select available_session_id from sessions)
order by time_begin;

select id from services
where name = 'Первичная консультация';

select id, name, cost, duration from services
where cost > 0 and is_for_benefits = $1 and is_deleted = false
order by name;

select id, name, cost, duration, is_for_benefits from services
where cost > 0 and is_deleted = false
order by name;

select ss.id as id,
       s.name as name,
       av_s.date as date,
       av_s.time_begin as time,
       ss.is_confirmed as is_confirmed
from sessions ss
join available_sessions av_s on av_s.id = ss.available_session_id
join services s on s.id = ss.service_id
where (av_s.date = current_date and av_s.time_begin > current_time
or av_s.date > current_date)
and ss.bot_user_id = $1;


select date from available_sessions
where
    id in (select available_session_id from sessions) and
    (date = current_date and time_begin > current_time or date > current_date)
group by date order by date;

select ss.id as id, s.name as name, av.time_begin as time
from sessions ss
join services s on s.id = ss.service_id
join available_sessions av on av.id = ss.available_session_id
where av.date = $1 and av.time_begin > $2
order by av.time_begin;


select
    ss.id as id,
    bu.username as username,
    bu.full_name as full_name,
    bu.birth_date as user_birth,
    s.name as service_name,
    av.date as date,
    av.time_begin as time,
    ss.is_confirmed as is_confirmed
from sessions ss
join bot_users bu on ss.bot_user_id = bu.telegram_id
join services s on s.id = ss.service_id
join available_sessions av on av.id = ss.available_session_id
where ss.id = $1;


select
    av.id,
    av.time_begin
from available_sessions as av
where av.date = $1
order by av.time_begin;


select exists(
select
    *
from sessions
where available_session_id = '65d0c392-16eb-4280-83b3-6c4da4948f0'
);