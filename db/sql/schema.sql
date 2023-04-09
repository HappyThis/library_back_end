DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS desk;
DROP TABLE IF EXISTS part;
DROP TABLE IF EXISTS layer;
-- 外键约束
PRAGMA foreign_keys = ON;
-- 用户表
CREATE TABLE user
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    create_time   NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- 楼层表
CREATE TABLE layer
(
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
-- 分区表
CREATE TABLE part
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    layer_id INTEGER NOT NULL,
    name     TEXT    NOT NULL,
    FOREIGN KEY (layer_id) REFERENCES layer (id)
);
-- 桌子表
CREATE TABLE desk
(
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    part_id INTEGER NOT NULL,
    name    TEXT    NOT NULL,
    FOREIGN KEY (part_id) REFERENCES part (id)
);

-- 插入用户数据

insert into user(username, password)
values ("萝卜0", "123456");
insert into user(username, password)
values ("萝卜1", "123456");
insert into user(username, password)
values ("萝卜2", "123456");

-- 插入楼层

insert into layer(name)
values ("一楼");
insert into layer(name)
values ("二楼");
insert into layer(name)
values ("三楼");

-- 插入分区

insert into part(layer_id, name)
values (1, "A区");
insert into part(layer_id, name)
values (1, "B区");
insert into part(layer_id, name)
values (1, "C区");
insert into part(layer_id, name)
values (2, "A区");
insert into part(layer_id, name)
values (2, "B区");
insert into part(layer_id, name)
values (2, "C区");
insert into part(layer_id, name)
values (3, "A区");
insert into part(layer_id, name)
values (3, "B区");
insert into part(layer_id, name)
values (3, "C区");

--插入桌子

insert into desk(part_id, name)
values (1, "1号");
insert into desk(part_id, name)
values (1, "2号");
insert into desk(part_id, name)
values (1, "3号");
insert into desk(part_id, name)
values (2, "1号");
insert into desk(part_id, name)
values (2, "2号");
insert into desk(part_id, name)
values (2, "3号");
insert into desk(part_id, name)
values (3, "1号");
insert into desk(part_id, name)
values (3, "2号");
insert into desk(part_id, name)
values (3, "3号");
insert into desk(part_id, name)
values (4, "1号");
insert into desk(part_id, name)
values (4, "2号");
insert into desk(part_id, name)
values (4, "3号");
insert into desk(part_id, name)
values (5, "1号");
insert into desk(part_id, name)
values (5, "2号");
insert into desk(part_id, name)
values (5, "3号");
insert into desk(part_id, name)
values (6, "1号");
insert into desk(part_id, name)
values (6, "2号");
insert into desk(part_id, name)
values (6, "3号");
insert into desk(part_id, name)
values (7, "1号");
insert into desk(part_id, name)
values (7, "2号");
insert into desk(part_id, name)
values (7, "3号");
values (8, "1号");
insert into desk(part_id, name)
values (8, "2号");
insert into desk(part_id, name)
values (8, "3号");
values (9, "1号");
insert into desk(part_id, name)
values (9, "2号");
insert into desk(part_id, name)
values (9, "3号");