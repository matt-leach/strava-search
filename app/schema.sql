drop table if exists users;
create table users (
  id integer primary key,
  name text,
  picture text
);

drop table if exists activities;
create table activities (
  id integer primary key,
  name text,
  distance integer,
  start_time datetime,
  users_id integer references users(users_id)
)
