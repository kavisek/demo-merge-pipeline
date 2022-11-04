status:
	docker compose ls
	docker container ls
	docker volume ls
	docker network ls

watch:
	watch -n 5 make status 

shutdown:
	docker-compose down

shutdown_volumes:
	docker-compose down -v

startup: shutdown
	docker compose --profile db up


	