-- models/marts/mart_user_analytics.sql
{{ config(materialized='table') }}

with users as (
  select user_id, username from {{ ref('dim_users') }}
),
facts as (
  select user_id, count(*) as posts_count, avg(body_length) as avg_body_length
  from {{ ref('posts_fact') }}
  group by user_id
)
select u.user_id, u.username, coalesce(f.posts_count,0) as posts_count, coalesce(f.avg_body_length,0) as avg_body_length
from users u
left join facts f on u.user_id = f.user_id
