-- +goose Up
alter table devices drop column id;
