# Deployment Guide - Voice Deepfake Detection API

This guide covers deployment options for making your API publicly accessible.

## 🌐 Deployment Options

### 1. Render.com (Easiest - Free Tier Available)

#### Steps:

1. **Create account** at [render.com](https://render.com)

2. **Create new Web Service**
   - Click "New +" → "Web Service"
   - Connect your Git repository (or use manual deploy)

3. **Configuration**:
   ```
   Name: voice-deepfake-api
   Environment: Docker
   Region: Choose closest to your users
   Branch: main
   ```

4. **Environment Variables**:
   ```
   API_KEY=your-secure-random-api-key-here
   ```

5. **Deploy**
   - Render will auto-detect Dockerfile
   - First build takes 5-10 minutes
   - You'll get a URL like: `https://voice-deepfake-api.onrender.com`

#### Cost: 
- Free tier available (sleeps after 15 min inactivity)
- Paid: $7/month for always-on

---

### 2. Railway.app (Simple - Free Trial)

#### Steps:

1. **Sign up** at [railway.app](https://railway.app)

2. **New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo" or "Empty Project"

3. **Add Variables**:
   ```
   API_KEY=your-secure-api-key
   PORT=8000
   ```

4. **Deploy**
   - Railway auto-detects Dockerfile
   - Generates public URL: `https://your-app.railway.app`

#### Cost:
- $5 free trial credit
- Pay-as-you-go after trial

---

### 3. Google Cloud Run (Scalable - Pay-per-use)

#### Prerequisites:
```bash
# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash
gcloud init
```

#### Steps:

1. **Build and push image**:
```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Build with Cloud Build
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/voice-deepfake-api

# Or build locally and push
docker build -t gcr.io/YOUR_PROJECT_ID/voice-deepfake-api .
docker push gcr.io/YOUR_PROJECT_ID/voice-deepfake-api
```

2. **Deploy to Cloud Run**:
```bash
gcloud run deploy voice-deepfake-api \
  --image gcr.io/YOUR_PROJECT_ID/voice-deepfake-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars API_KEY=your-secure-api-key \
  --memory 2Gi \
  --timeout 300 \
  --max-instances 10
```

3. **Get URL**:
```bash
gcloud run services describe voice-deepfake-api \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

#### Cost:
- Free tier: 2 million requests/month
- $0.00002400 per request after free tier
- Billed only when running

---

### 4. AWS EC2 (Full Control)

#### Setup:

1. **Launch EC2 Instance**:
   - AMI: Ubuntu 22.04 LTS
   - Instance type: t3.medium (2 vCPU, 4GB RAM)
   - Security group: Allow ports 22 (SSH), 80 (HTTP), 443 (HTTPS)

2. **Connect and Install Docker**:
```bash
ssh -i your-key.pem ubuntu@your-instance-ip

# Install Docker
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
```

3. **Deploy Application**:
```bash
# Clone repository
git clone https://github.com/yourusername/voice-deepfake-api.git
cd voice-deepfake-api

# Set API key
echo "API_KEY=your-secure-api-key" > .env

# Run with Docker Compose
docker-compose up -d
```

4. **Setup Nginx Reverse Proxy** (Optional but recommended):
```bash
sudo apt install -y nginx

# Create nginx config
sudo nano /etc/nginx/sites-available/voice-api
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/voice-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

5. **Setup SSL with Let's Encrypt**:
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

#### Cost:
- t3.medium: ~$30-40/month
- More control and customization

---

### 5. DigitalOcean App Platform (Balanced)

#### Steps:

1. **Create account** at [digitalocean.com](https://digitalocean.com)

2. **Create App**:
   - Apps → Create App
   - Connect GitHub repository

3. **Configure**:
   ```
   Type: Web Service
   Dockerfile: Detected automatically
   HTTP Port: 8000
   ```

4. **Environment Variables**:
   ```
   API_KEY=your-secure-api-key
   ```

5. **Choose Plan**:
   - Basic: $5/month (512MB RAM)
   - Professional: $12/month (1GB RAM) - Recommended

6. **Deploy**: App URL will be provided

---

### 6. Heroku (Classic Option)

#### Steps:

1. **Install Heroku CLI**:
```bash
curl https://cli-assets.heroku.com/install.sh | sh
heroku login
```

2. **Create App**:
```bash
heroku create voice-deepfake-api
```

3. **Set Config**:
```bash
heroku config:set API_KEY=your-secure-api-key
```

4. **Deploy**:
```bash
# Using Container Registry
heroku container:login
heroku container:push web
heroku container:release web

# Open app
heroku open
```

#### Cost:
- Eco Dynos: $5/month (sleeps after 30 min)
- Basic: $7/month (no sleeping)

---

## 🔒 Security Checklist

Before deploying publicly:

- [ ] Change default API key to strong random string
- [ ] Enable HTTPS (SSL/TLS)
- [ ] Set up rate limiting
- [ ] Configure CORS appropriately
- [ ] Enable request logging
- [ ] Set up monitoring/alerting
- [ ] Review error messages (don't expose internals)
- [ ] Implement request size limits
- [ ] Add API documentation endpoint
- [ ] Set up backup/recovery

---

## 🔑 Generate Secure API Key

```python
import secrets

# Generate a secure random API key
api_key = secrets.token_urlsafe(32)
print(f"Your secure API key: {api_key}")
```

Or use command line:
```bash
openssl rand -base64 32
```

---

## 📊 Monitoring Setup

### Health Checks

All platforms support health checks. Configure:

- **Endpoint**: `/api/v1/health`
- **Method**: GET
- **Expected Response**: 200 OK
- **Interval**: 30 seconds
- **Timeout**: 10 seconds

### Logging

Add structured logging:

```python
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Log each request
logger.info(json.dumps({
    'event': 'api_request',
    'language': language,
    'classification': result,
    'confidence': confidence,
    'processing_time_ms': processing_time
}))
```

---

## 🚀 Performance Optimization

### 1. Docker Optimization

```dockerfile
# Multi-stage build for smaller image
FROM python:3.10-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Caching

Add Redis for caching results:

```python
import redis
import hashlib

redis_client = redis.Redis(host='localhost', port=6379)

def get_cache_key(audio_base64: str) -> str:
    return hashlib.sha256(audio_base64.encode()).hexdigest()

# Check cache before processing
cache_key = get_cache_key(request.audio_base64)
cached = redis_client.get(cache_key)
if cached:
    return json.loads(cached)
```

### 3. Workers

For higher throughput:

```bash
# Run with multiple workers
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🌍 Making API Publicly Accessible

After deployment, your API will be available at:

**Format**: `https://your-app-name.platform-domain.com/api/v1/analyze`

**Examples**:
- Render: `https://voice-deepfake-api.onrender.com/api/v1/analyze`
- Railway: `https://voice-deepfake-api.railway.app/api/v1/analyze`
- Cloud Run: `https://voice-deepfake-api-xxxxx.run.app/api/v1/analyze`

### Test Public API

```bash
# Replace with your actual URL
API_URL="https://your-app.platform.com"

# Health check
curl $API_URL/api/v1/health

# API info
curl $API_URL/api/v1/info
```

---

## 📝 Submission Template

For hackathon submission:

```
API Endpoint: https://voice-deepfake-api.onrender.com/api/v1/analyze
API Key: [Your-Secure-API-Key]

Supported Languages: Tamil, English, Hindi, Malayalam, Telugu
Input Format: Base64-encoded MP3 audio
Output Format: JSON with classification and confidence score

Sample Request:
POST https://voice-deepfake-api.onrender.com/api/v1/analyze
Headers:
  X-API-Key: [Your-Secure-API-Key]
  Content-Type: application/json
Body:
{
  "audio_base64": "...",
  "language": "english"
}

Documentation: https://github.com/yourusername/voice-deepfake-api
```

---

## 🆘 Troubleshooting

### Issue: Deployment fails

**Solution**:
- Check Dockerfile syntax
- Verify all files are committed
- Review build logs
- Ensure requirements.txt is complete

### Issue: API times out

**Solution**:
- Increase timeout settings (300s recommended)
- Optimize audio processing
- Use smaller audio samples for testing
- Increase memory allocation

### Issue: Cold starts are slow

**Solution**:
- Use paid tier to prevent sleeping
- Implement warm-up requests
- Consider serverless alternatives
- Add startup optimization

---

## 📞 Support

If you encounter issues:

1. Check platform-specific documentation
2. Review application logs
3. Test locally first with Docker
4. Verify environment variables
5. Check security group/firewall rules

---

## ✅ Post-Deployment Checklist

- [ ] API is accessible publicly
- [ ] Health check endpoint works
- [ ] API key authentication works
- [ ] Test with sample audio
- [ ] HTTPS is enabled
- [ ] Monitoring is set up
- [ ] Documentation is accessible
- [ ] Rate limiting configured (if needed)
- [ ] Backup API key stored securely
- [ ] Team members have access
