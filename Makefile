.PHONY: up down logs db backend frontend

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

db:
	docker exec -it game-db psql -U gameuser -d gamedb

backend:
	cd backend && uvicorn app.main:app --reload

frontend:
	cd frontend && npm run dev
ingest:
	cd ingestion && python -m app.main
embed:
	cd ingestion && python -m app.embed_games
search:
	cd ingestion && python -m app.search_games
