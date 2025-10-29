-- models/facts/posts_fact.sql
{{ config(materialized='table') }}

select
  p.id as post_id,
  p.userId as user_id,
  p.title,
  p.body,
  length(p.body) as body_length,
  date_trunc('day', p.ingested_at) as ingested_date
from {{ ref('stg_posts_incremental') }} p
