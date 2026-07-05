# SmartDiag API

Production-grade disease prediction REST API built with FastAPI, containerized with Docker, orchestrated with Kubernetes, and deployed via CI/CD on AWS.

## Stack
- **Backend**: Python 3.11, FastAPI, Scikit-learn
- **Containerization**: Docker (non-root, health-checked)
- **Orchestration**: Kubernetes (Deployment, Service, HPA)
- **CI/CD**: GitHub Actions (test → build → deploy pipeline)
- **Cloud**: AWS EC2 / S3 (model artifact storage)

## Architecture

```
GitHub Push → CI (pytest) → Docker Build → GHCR Push → kubectl rollout
```

Zero-downtime deployments via RollingUpdate strategy. HPA scales pods 2→10 based on CPU utilization (70% threshold).

## Local Development

```bash
# Run with docker-compose
docker-compose up --build

# Test the API
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.2, 3.4, 5.6, 7.8]}'
```

## Run Tests

```bash
pip install -r requirements.txt
pytest app/test_main.py -v
```

## Kubernetes Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Check rollout
kubectl rollout status deployment/smartdiag-api

# Scale manually if needed
kubectl scale deployment/smartdiag-api --replicas=4
```

## CI/CD Pipeline

| Stage  | Trigger       | Action                          |
|--------|---------------|---------------------------------|
| Test   | Every push    | pytest                          |
| Build  | Merge to main | Docker build + push to GHCR     |
| Deploy | After build   | kubectl rolling update          |

## Observability

- `/health` — liveness probe (used by Kubernetes)
- `/metrics` — readiness + model status endpoint
- Prometheus-compatible metrics endpoint (extend via `prometheus-fastapi-instrumentator`)
