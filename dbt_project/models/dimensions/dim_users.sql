-- models/dimensions/dim_users.sql
{{ config(materialized='table') }}

select
  id as user_id,
  username
from {{ ref('seed_users') }}
