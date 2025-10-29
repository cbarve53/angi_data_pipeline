-- models/marts/mart_user_posts.sql
select
  userId,
  count(*) as posts_count,
  avg(body_length) as avg_body_length
from {{ ref('int_posts_enriched') }}
group by userId
