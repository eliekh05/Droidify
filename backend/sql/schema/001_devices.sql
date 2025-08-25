-- +goose Up
create table devices (
    id varchar(36) primary key,
    model text unique not null,
    twrp text unique,
    stock_firmware text unique,
    odin text unique,
    orange_fox_recovery text,
    custom_firmeware text,
    shrp_recovery text unique
);

-- +goose Down
drop table devices;
