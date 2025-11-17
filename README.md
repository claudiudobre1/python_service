# 🎮 Guessing Game -- Microservices on Kubernetes (GKE)

Acest proiect implementează un sistem de microservicii pentru un joc de
„Guess the Number", folosind:

-   **Python Flask** -- Gateway + Game Service + Score Service\
-   **React** -- Frontend\
-   **PostgreSQL** -- Bază de date pentru scoruri\
-   **Docker** -- Containerizare\
-   **Kubernetes (GKE)** -- Orchestrare\
-   **Artifact Registry** -- Stocarea imaginilor Docker\
-   **Ingress (NGINX)** -- expunere externă\
-   **CI/CD cu GitHub Actions** -- build + push + deploy automat

## 🧩 Arhitectura aplicației

``` mermaid
flowchart TB

User -->|HTTP| Ingress

Ingress -->|/api| Gateway
Ingress -->|/| Frontend

Gateway --> GameService
Gateway --> ScoreService

ScoreService --> PostgreSQL
```

## 🌐 IP-uri & URL-uri utile

  Serviciu                             Adresă / URL
  ------------------------------------ ---------------------------------
  **Ingress Public IP**                `http://34.116.141.233`
  **Frontend direct (LoadBalancer)**   `http://34.116.172.10`
  **API extern via Ingress**           `http://34.116.141.233/api/...`
  **Gateway intern**                   `gateway:8000`
  **Game Service intern**              `game-service:8000`
  **Score Service intern**             `score-service:8001`
  **Postgres service**                 `postgres:5432`

## 📁 Structura proiectului

    guessing-micro-full/
    │
    ├── frontend/               
    ├── gateway/               
    ├── services/
    │   ├── game-service/
    │   └── score-service/
    │
    ├── k8s/
    │   ├── frontend-deployment.yaml
    │   ├── gateway-deployment.yaml
    │   ├── game-service-deployment.yaml
    │   ├── score-service-deployment.yaml
    │   ├── postgres-deployment.yaml
    │   ├── ingress.yaml
    │   └── postgres-secret.yaml
    │
    └── .github/workflows/
        ├── build-and-deploy-frontend.yml
        ├── build-and-deploy-gateway.yml
        ├── build-and-deploy-game-service.yml
        └── build-and-deploy-score-service.yml

## 🐳 Docker -- Build & Run (Local)

### Gateway

``` bash
docker build -t gateway:local ./gateway
docker run -p 8000:8000 gateway:local
```

### Game Service

``` bash
docker build -t game-service:local ./services/game-service
docker run -p 8000:8000 game-service:local
```

### Score Service

``` bash
docker build -t score-service:local ./services/score-service
docker run -p 8001:8001 score-service:local
```

### Frontend

``` bash
docker build -t frontend:local ./frontend
docker run -p 80:80 frontend:local
```

## ☸️ Kubernetes -- Comenzi importante

### Deploy complet:

``` bash
kubectl apply -f k8s/
```

### Verificare resurse:

``` bash
kubectl get pods -o wide
kubectl get svc
kubectl get ingress
```

### Logs:

``` bash
kubectl logs -l app=gateway --tail=200
```

### Debug DNS intern:

``` bash
kubectl exec -it <gateway-pod> -- getent hosts score-service
```

### Test API:

``` bash
kubectl exec -it <gateway-pod> -- python3 - <<EOF
import requests
print(requests.get("http://score-service:8001/highscore").text)
EOF
```

## 🚀 Deploy pe Google Cloud (GKE + Artifact Registry)

### Autentificare Docker:

``` bash
gcloud auth configure-docker europe-central2-docker.pkg.dev
```

### Build:

``` bash
docker build -t europe-central2-docker.pkg.dev/PROJECT/my-repo/gateway:v1 .
```

### Push:

``` bash
docker push europe-central2-docker.pkg.dev/PROJECT/my-repo/gateway:v1
```

### Update deployment:

``` bash
kubectl set image deployment/gateway gateway=europe-central2-docker.pkg.dev/PROJECT/my-repo/gateway:v1
```

## 🔄 CI/CD -- GitHub Actions

Fiecare microserviciu are propriul pipeline.

### Exemple secretes necesare:

-   `GCP_PROJECT_ID`
-   `GCP_SA_KEY`
-   `GKE_CLUSTER`
-   `GKE_ZONE`

## 🛠 Troubleshooting

### ❌ Score Service -- "password authentication failed"

``` bash
kubectl delete secret postgres-secret
kubectl apply -f k8s/postgres-secret.yaml
kubectl rollout restart deployment score-service
```

### ❌ Ingress returnează 404

Verifică:

``` bash
kubectl describe ingress guessing-app-ingress
```

## 🌍 URL-uri finale

  Endpoint          URL
  ----------------- -------------------------------------
  Frontend          http://34.116.172.10
  API → Highscore   http://34.116.141.233/api/highscore
  API → Guess       http://34.116.141.233/api/guess
  API → Reset       http://34.116.141.233/api/reset
