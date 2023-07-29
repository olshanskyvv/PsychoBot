init_query = """
create table if not exists bot_users (
  telegram_id bigint primary key,
  full_name varchar(255) null,
  birth_date date null,
  agreement bool default false,
  is_benefits bool default false
);

create table if not exists services (
  id uuid primary key default gen_random_uuid(),
  name varchar(255) not null,
  cost integer not null,
  duration integer not null,
  is_for_benefits bool default false
);

create table if not exists available_sessions (
    id uuid primary key default gen_random_uuid(),
    date date unique,
    time_begin time unique
);

create table if not exists sessions(
    id uuid primary key default gen_random_uuid(),
    bot_user_id bigint references bot_users(telegram_id) not null,
    service_id uuid references services(id) not null,
    available_session_id uuid references available_sessions(id) not null unique,
    is_confirmed bool default false
);

insert into services (name, cost, duration)
values ('Первичная консультация', 0, 30)
on conflict do nothing;
"""
