## Cloud-Native Game Discovery Platform

An end-to-end AI-powered semantic search platform that enables users to discover games using natural language queries.

This project demonstrates how to build and deploy a production-ready system combining data pipelines, vector embeddings, backend APIs, frontend applications, and Kubernetes-based infrastructure with fully automated CI/CD.

## Architecture
User → Frontend (Next.js)
↓
Backend (FastAPI)
↓
PostgreSQL (pgvector)
↓
Vertex AI (Embeddings)



## Tech Stack

- Frontend: Next.js (App Router)
- Backend: FastAPI (Python)
- Database: PostgreSQL + pgvector
- AI/ML: Vertex AI Embeddings
- Cloud: Google Cloud Platform (GKE)
- CI/CD: GitHub Actions
- Containerization: Docker
- Orchestration: Kubernetes

## Key Features

- Semantic search using natural language queries
- Vector similarity ranking via embeddings
- Automated data ingestion from RAWG API
- FastAPI backend with structured logging and caching
- Kubernetes-based deployment (GKE)
- Secure GCP access using Workload Identity
- Fully automated CI/CD pipeline

## Deployment Workflow

1. Build Docker images (frontend, backend, ingestion)
2. Push images to Docker Hub
3. GitHub Actions deploys to GKE
4. Kubernetes provisions:
   - PostgreSQL (StatefulSet)
   - Backend & Frontend (Deployments)
   - Ingestion & Embedding Jobs

## Future Improvements

- Add Redis caching layer
- Implement Horizontal Pod Autoscaling
- Integrate observability (Prometheus + Grafana)
- Enable multi-region deployment
- Add personalization and recommendation tuning
