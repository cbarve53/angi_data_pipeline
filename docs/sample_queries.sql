-- sample_queries.sql
-- 1) top users by post count
select userId, posts_count from marts.mart_user_posts order by posts_count desc limit 10;

-- 2) average body length
select avg(avg_body_length) from marts.mart_user_posts;
