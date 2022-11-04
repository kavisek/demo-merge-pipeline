create table if not exists demo.grade
(
	id bigint,
	last_modified timestamp,
	batch_uuid text,
	grade bigint
);

alter table demo.grade owner to postgres;

create unique index if not exists grade_id_uindex
	on demo.grade (id);