insert into bot_users (telegram_id, username)
values ($1, $2)
on conflict do nothing;

insert into services (name, cost, duration, is_for_benefits)
values ($1, $2, $3, $4)
returning id;

insert into available_sessions (date, time_begin)
values ($1, $2)
returning id;

insert into available_sessions (date, time_begin)
values ('2023-08-07', '17:00'),
       ('2023-08-07', '18:00'),
       ('2023-08-07', '19:00'),
       ('2023-08-07', '20:00'),
       ('2023-08-07', '21:00'),
       ('2023-08-07', '22:00'),
       ('2023-08-08', '17:00'),
       ('2023-08-08', '18:00'),
       ('2023-08-08', '19:00'),
       ('2023-08-08', '20:00'),
       ('2023-08-08', '21:00'),
       ('2023-08-08', '22:00'),
       ('2023-08-09', '17:00'),
       ('2023-08-09', '18:00'),
       ('2023-08-09', '19:00'),
       ('2023-08-09', '20:00'),
       ('2023-08-09', '21:00'),
       ('2023-08-09', '22:00');

insert into sessions (bot_user_id, service_id, available_session_id)
values ($1, $2, $3)
returning id;


insert into available_sessions (date, time_begin)
values ('2023-10-29', '17:00'),
       ('2023-10-29', '18:00'),
       ('2023-10-29', '18:00')
on conflict do nothing;

