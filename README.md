# Enemy Soldiers CRUD API (FastAPI + MongoDB)

A complete CRUD system for managing enemy soldiers using **FastAPI** and **MongoDB**.

## 1) Run Locally

### 1.1 Start MongoDB (Docker)

```bash
scripts/run_local_mongo_docker.bat
```

MongoDB will be available at:

```
mongodb://localhost:27017
```

### 1.2 Install Python dependencies

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 1.3 Run FastAPI server

```bash
set MONGODB_URI=mongodb://localhost:27017
set DB_NAME=enemy_soldiers
set COLLECTION_NAME=soldier_details
python -m services.data_loader.api
```

### 1.4 Test locally

```bash
python scripts/test_requests.py
```

Or open Swagger UI:

```
http://localhost:8000/docs
```

---

## 2) CRUD Endpoints

* **GET** `/soldiersdb/` — get all soldiers
* **GET** `/soldiersdb/{id}` — get soldier by ID
* **POST** `/soldiersdb/` — add new soldier (full JSON)
* **PUT** `/soldiersdb/{id}` — update soldier fields (partial JSON)
* **DELETE** `/soldiersdb/{id}` — delete soldier by ID

Example POST:

```bash
curl -X POST http://localhost:8000/soldiersdb/ \
  -H "Content-Type: application/json" \
  -d '{"id":1,"first_name":"Ali","last_name":"Reza","phone_number":"+98-555-1111","rank":"Private"}'
```

---

## 3) Docker Build & Run

### 3.1 Build image & push to Docker Hub

Edit `scripts/commands.bat` and set:

```
DOCKER_USER=shmuelgross
NAMESPACE=shmuelgross3-dev
```

Then run:

```bash
scripts/commands.bat
```

### 3.2 Run container locally

```bash
docker run -p 8000:8000 -e MONGODB_URI=mongodb://host.docker.internal:27017 <USER>/enemy-soldiers-api:latest
```

---

## 4) OpenShift Deployment

1. Create PVC:

```bash
oc apply -f infrastructure/k8s/mongo-pvc.yaml
```

2. Deploy MongoDB:

```bash
oc apply -f infrastructure/k8s/mongo-deployment.yaml
oc apply -f infrastructure/k8s/mongo-service.yaml
```

3. Deploy API:

```bash
oc apply -f infrastructure/k8s/api-deployment.yaml
oc apply -f infrastructure/k8s/api-service.yaml
oc apply -f infrastructure/k8s/api-route.yaml
```

4. Get the public route:

```bash
oc get route enemy-soldiers-api -o jsonpath="{.spec.host}\n"
```

Test with:

```bash
curl https://<route-host>/soldiersdb/
```

---

## 6) Notes

* For demo purposes MongoDB runs **without authentication**. For production, configure a **Secret** with username/password and set `MONGODB_URI` accordingly (e.g., `mongodb://user:pass@mongodb:27017/?authSource=admin`).
* Swagger documentation is available at `/docs`. You can also use Postman or CURL for testing.
