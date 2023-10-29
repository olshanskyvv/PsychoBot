delete from sessions
where id = $1;


delete from available_sessions
where id = $1;