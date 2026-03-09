# Deployment Guide - InsureSmart AI

## Quick Deployment to Azure Static Web Apps

### Step 1: Prerequisites

- Azure account (free tier available)
- GitHub repository with this code
- Azure CLI installed

### Step 2: Create Azure Static Web App

```bash
# Login to Azure
az login

# Create resource group
az group create --name insuresmart-rg --location eastus

# Create storage account for backend
az storage account create \
  --name insuresmartstorage \
  --resource-group insuresmart-rg \
  --location eastus

# Create Static Web App
az staticwebapp create \
  --name insuresmart-ai \
  --resource-group insuresmart-rg \
  --source https://github.com/yourusername/InsureSmart-AI \
  --branch main \
  --app-location "frontend/build" \
  --api-location "backend"
```

### Step 3: Configure Environment Variables

In Azure Portal:
1. Go to your Static Web App
2. Settings → Configuration
3. Add application settings:

```
DATABASE_URL=mysql+pymysql://user:pass@host/db
OPENAI_API_KEY=sk-...
JWT_SECRET_KEY=your-secret-key
```

### Step 4: Update GitHub Actions Workflow

The deployment yaml creates automatically. Verify it has:

```yaml
- name: Install backend dependencies
  run: |
    cd backend
    pip install -r requirements.txt

- name: Build frontend
  run: |
    cd frontend
    npm install
    npm run build
```

### Step 5: Deploy

Simply push to main branch:
```bash
git add .
git commit -m "deploy: Ready for Azure deployment"
git push origin main
```

### Step 6: Verify Deployment

Check Azure Portal for:
- ✅ Build status
- ✅ Live URLs
- ✅ API accessibility
- ✅ Database connectivity

## Alternative: Deploy to Render

### Create `.render.yaml`:

```yaml
services:
  - name: insuresmart-api
    env: python
    startCommand: python backend/run.py
    envVars:
      - key: DATABASE_URL
        value: <your-db-url>
      - key: OPENAI_API_KEY
        value: <your-key>
  
  - name: insuresmart-frontend
    env: static
    staticPublishPath: frontend/build
    buildCommand: cd frontend && npm install && npm run build
```

## Enable CORS for Local Development

Update `backend/app/__init__.py`:

```python
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    # ... rest of code
```

## Next Steps

- Set up CI/CD pipeline
- Configure custom domain
- Enable auto-scaling
- Set up monitoring and alerts
- Configure CDN for faster delivery
