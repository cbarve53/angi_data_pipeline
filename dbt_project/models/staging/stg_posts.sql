-- models/staging/stg_posts.sql
with raw as (
    select
      id,
      userid::int as userId,
      title,
      body,
      raw_key
    from {{ source('raw', 'raw_posts') }}
)
select * from raw
