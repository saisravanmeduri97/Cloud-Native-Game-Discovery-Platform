# Cloud Native Game Discovery Platform

An AI-powered game discovery platform that uses semantic search to recommend games based on natural language queries.

---

## Tech Stack

- Frontend: Next.js  
- Backend: FastAPI  
- AI: Vertex AI embeddings  
- Database: PostgreSQL + pgvector  
- Ingestion: Python  
- DevOps: Docker, GitHub Actions, Kubernetes (GKE), Terraform  

---

## Architecture

RAWG API → Ingestion → PostgreSQL (pgvector)  
User → Frontend → Backend → Vertex AI → Vector Search → Results  

---

## API

POST /search  
→ semantic game recommendations  

GET /games/{id}  
→ game details  

GET /health  
GET /ready  

---

## Features

- Semantic search using embeddings  
- Real game data ingestion  
- Vector similarity search (pgvector)  
- FastAPI backend  
- Next.js frontend  
- Structured logging and caching  

---

## Local Development

Start backend  
make backend  

Start frontend  
make frontend  

Run ingestion  
make ingest  

Run embeddings  
make embed  

---

## Docker

Build  
make build  

Run  
make up

---

## Roadmap

- Docker → Docker Hub  
- GitHub Actions CI/CD  
- Deploy to GKE  
- Add ingestion as job  
- Add monitoring  

---
