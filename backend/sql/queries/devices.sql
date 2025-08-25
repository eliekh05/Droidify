-- name: GetDevice :one
select * from devices where model = $1;

-- name: AddDevice :one
insert into devices (model,twrp, stock_firmware, odin, orange_fox_recovery, custom_firmware, shrp_recovery) values (
    $1,
    $2,
    $3,
    $4,
    $5,
    $6
) returning *;
