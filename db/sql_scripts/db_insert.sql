insert into bot_users (telegram_id)
values ($1);

insert into services (name, cost, duration, is_for_benefits)
values ($1, $2, $3, $4)
returning id;

insert into available_sessions (date, time_begin)
values ($1, $2)
returning id;

insert into available_sessions (date, time_begin)
values ('2023-08-01', '17:00'),
       ('2023-08-01', '18:00'),
       ('2023-08-01', '19:00'),
       ('2023-08-01', '20:00'),
       ('2023-08-01', '21:00'),
       ('2023-08-01', '22:00'),
       ('2023-08-02', '17:00'),
       ('2023-08-02', '18:00'),
       ('2023-08-02', '19:00'),
       ('2023-08-02', '20:00'),
       ('2023-08-02', '21:00'),
       ('2023-08-02', '22:00'),
       ('2023-08-03', '17:00'),
       ('2023-08-03', '18:00'),
       ('2023-08-03', '19:00'),
       ('2023-08-03', '20:00'),
       ('2023-08-03', '21:00'),
       ('2023-08-03', '22:00');

insert into sessions (bot_user_id, service_id, available_session_id)
values ($1, $2, $3)
returning id;

