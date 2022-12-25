create table if not exists public.grade
(
	id bigint,
	last_modified timestamp,
	batch_uuid text,
	grade bigint
);

alter table public.grade owner to postgres;

create unique index if not exists grade_id_uindex
	on public.grade (id);