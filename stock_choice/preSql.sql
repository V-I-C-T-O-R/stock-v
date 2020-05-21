-- drop table stock_info;
CREATE TABLE IF NOT EXISTS stock_info (
      code  TEXT,
      name  TEXT,
      nmc   TEXT
);
-- drop table stock_work_day_data;
-- 记得建索引
create table if not EXISTS stock_work_day_data(
`date_day` date,
`open` DOUBLE,
`close` DOUBLE ,
`high` DOUBLE,
`low` DOUBLE,
`volume` DOUBLE,
`code` TEXT,
`p_change` DOUBLE
);


