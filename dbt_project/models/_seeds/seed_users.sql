-- models/_seeds/seed_users.sql
-- wrapper model for users seed (dbt seed will create table 'seed_users')
select * from {{ ref('seed_users') }}
