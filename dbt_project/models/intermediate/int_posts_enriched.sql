-- models/intermediate/int_posts_enriched.sql
with posts as (
    select * from {{ ref('stg_posts') }}
)
select
  id,
  userId,
  title,
  length(body) as body_length
from posts
