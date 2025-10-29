-- models/staging/stg_posts_incremental.sql
{{ config(materialized='incremental', unique_key='id') }}

with raw as (
    select
      (data->>'id')::int as id,
      (data->>'userId')::int as userId,
      data->>'title' as title,
      data->>'body' as body,
      meta->>'raw_key' as raw_key,
      meta->>'ingested_at' as ingested_at
    from (
      select jsonb_build_object('data', to_jsonb(t.*), 'meta', jsonb_build_object('raw_key', raw_key, 'ingested_at', now()::text)) as obj
      from {{ source('raw', 'raw_posts') }} as t
    ) s,
    lateral (select obj->'data' as data, obj->'meta' as meta) ped
)

select id, userId, title, body, raw_key, ingested_at::timestamp as ingested_at
from raw

{% if is_incremental() %}
  where id not in (select id from {{ this }})
{% endif %}
