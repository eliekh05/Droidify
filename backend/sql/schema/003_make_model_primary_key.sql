-- +goose Up
alter table devices
    drop constraint if exists devices_pkey,
    add primary key (model);

-- +goose Down
alter table devices
    drop constraint if exists devices_pkey;
