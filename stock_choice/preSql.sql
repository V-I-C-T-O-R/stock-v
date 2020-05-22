-- drop table stock_info;
CREATE TABLE IF NOT EXISTS stock_info (
      code  TEXT,
      name  TEXT,
      nmc   TEXT
);
-- drop table stock_work_day_data;
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
-- 记得建索引
create index code_index on stock_work_day_data(code, date_day);


