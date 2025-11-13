
# 🎯 Jocul de Ghicit Numere — Automatizare DevOps pe Google Cloud Platform (GCP)

Acest proiect conține un simplu **joc în Python de ghicit numere**, implementat printr-o **arhitectură DevOps completă** care rulează pe **Google Cloud Platform (GCP)**.

Deși aplicația rulează interactiv în consolă, scopul proiectului este de a demonstra cum se pot integra:
- 🐳 **Docker** — pentru containerizarea aplicației  
- ☁️ **Kubernetes (GKE)** — pentru orchestrarea containerelor  
- 🏗️ **Terraform** — pentru crearea infrastructurii  
- ⚙️ **Ansible** — pentru configurarea mediilor  
- 🔁 **GitHub Actions** — pentru pipeline-ul CI/CD automat  
- 📊 **Prometheus + Grafana** — pentru monitorizare  
- 💰 **GCP Recommender API** — pentru optimizarea costurilor

---

## 🧩 Despre joc

**Jocul de ghicit numere** generează un număr aleator între **1 și 100**.  
Jucătorul trebuie să-l ghicească, iar programul oferă feedback la fiecare încercare (`Prea mic`, `Prea mare`, `Corect!`).

Este un exemplu simplu, dar util pentru a demonstra un flux DevOps complet — de la cod sursă până la rulare în Kubernetes.

### 🎮 Exemplu de rulare

```
--- Bine ai venit la Jocul de Ghicit Numere! ---
Ghiceste un număr între 1 și 100.
Introdu numărul tău: 50
Prea mic! Încearcă din nou.
Introdu numărul tău: 75
Prea mare! Încearcă din nou.
Introdu numărul tău: 68
Felicitări! Ai ghicit numărul 68 în 9 încercări.
```

---

## 📂 Structura proiectului

```
flask-kube-gcp/
├── app.py                     # Codul principal al jocului
├── Dockerfile                 # Instrucțiuni pentru imaginea Docker
├── requirements.txt           # Dependențe Python
├── kubernetes/
│   ├── deployment.yaml        # Manifestul Kubernetes pentru aplicație
│   └── service.yaml           # Manifestul Kubernetes pentru serviciu
├── terraform/
│   ├── main.tf                # Infrastructura GKE + Artifact Registry
│   ├── variables.tf
│   └── outputs.tf
├── ansible/
│   ├── inventory.ini
│   └── playbook.yml
└── .github/
    └── workflows/
        └── deploy.yaml        # Workflow GitHub Actions (CI/CD)
```

---

## 🏗️ Arhitectura DevOps

```
Aplicație Python (consolă)
     ↓
Docker Image
     ↓
Artifact Registry (GCP)
     ↓
GKE Cluster (Terraform)
     ↓
CI/CD (GitHub Actions)
     ↓
Configurare (Ansible)
     ↓
Monitorizare + Optimizare costuri
```

---

## ⚙️ Cerințe preliminare

Înainte de rulare, ai nevoie de:

- Un **proiect GCP** cu facturare activată  
- Un **Service Account** cu următoarele roluri:
  - `roles/container.admin`
  - `roles/artifactregistry.admin`
  - `roles/compute.viewer`
  - `roles/iam.serviceAccountUser`
- (Opțional) Unelte locale instalate:
  - [Docker](https://docs.docker.com/)
  - [Terraform](https://developer.hashicorp.com/terraform/downloads)
  - [gcloud CLI](https://cloud.google.com/sdk/docs/install)
  - [kubectl](https://kubernetes.io/docs/tasks/tools/)
  - [Ansible](https://www.ansible.com/)

---

## 🎯 Rulare locală

```bash
python app.py
```

Pentru a ieși din joc:
```
Introdu numărul tău: quit
```

---

## 🐳 Utilizare Docker

### Construirea imaginii Docker:
```bash
docker build -t number-guess-game .
```

### Rulare interactivă:
```bash
docker run -it number-guess-game
```

---

## ☁️ Automatizare CI/CD cu GitHub Actions

Pipeline-ul GitHub Actions (`.github/workflows/deploy.yaml`) execută automat:

1. Crearea infrastructurii cu **Terraform**  
2. Construirea și trimiterea imaginii Docker către **Artifact Registry**  
3. Deploy în **Google Kubernetes Engine (GKE)**  
4. Configurare și monitorizare prin **Ansible**

### Configurare:

1. Publică acest repository pe contul tău GitHub.  
2. Adaugă următoarele **GitHub Secrets**:
   - `GCP_PROJECT_ID`
   - `GCP_SA_KEY` (conținutul fișierului JSON al service account-ului)
3. Fă *push* pe branch-ul `main` — pipeline-ul va porni automat.

---

## 📊 Monitorizare cu Prometheus & Grafana

Pentru a instala sistemul de monitorizare:
```bash
ansible-playbook -i ansible/inventory.ini ansible/playbook.yml
```

Apoi accesează Grafana:
```bash
kubectl port-forward svc/grafana 3000:3000 -n monitoring
```
🔗 [http://localhost:3000](http://localhost:3000)  
Login implicit: `admin / admin`

---

## 💰 Optimizarea costurilor în GCP

Activează API-ul Recommender:
```bash
gcloud services enable recommender.googleapis.com
```

Afișează recomandări:
```bash
gcloud recommender recommendations list   --recommender=google.compute.instance.MachineTypeRecommender
```

---

## 🧹 Curățare resurse

Pentru a șterge întreaga infrastructură:
```bash
terraform -chdir=terraform destroy -auto-approve
```

---

## 🧾 Probleme frecvente

| Problemă | Cauză | Soluție |
|-----------|--------|----------|
| `EOFError: EOF when reading a line` | Aplicația e interactivă (`input()` în Docker) | Rulează cu `docker run -it` |
| `failed to read dockerfile` | Lipsă fișier `Dockerfile` în director | Verifică locația proiectului |
| `permission denied` | Lipsă roluri în Service Account | Adaugă rolurile GKE și Artifact Registry |
| Aplicația nu pornește în GKE | Imagine greșită în deployment.yaml | Actualizează cu numele imaginii corecte |


