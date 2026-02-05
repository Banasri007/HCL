# 🚀 Quick Start Guide - Deploy in 15 Minutes

This guide will get your Voice Deepfake Detection API deployed and publicly accessible in 15 minutes.

## ⚡ Super Fast Deploy (Choose One)

### Option A: Render.com (Recommended - Easiest)

**Time: ~10 minutes**

1. **Sign up**: Go to [render.com](https://render.com) and create free account

2. **Create Web Service**:
   - Click "New +" → "Web Service"
   - Choose "Build and deploy from a Git repository"
   - Connect GitHub (or use public repo option)

3. **Configure**:
   ```
   Name: voice-deepfake-api
   Environment: Docker
   Instance Type: Free
   ```

4. **Add Environment Variable**:
   - Key: `API_KEY`
   - Value: Generate secure key (see below)

5. **Deploy**: Click "Create Web Service"
   - Wait 5-8 minutes for first build
   - You'll get URL: `https://voice-deepfake-api.onrender.com`

6. **Test**:
   ```bash
   curl https://voice-deepfake-api.onrender.com/api/v1/health
   ```

---

### Option B: Railway.app (Also Easy)

**Time: ~8 minutes**

1. **Sign up**: Go to [railway.app](https://railway.app)

2. **New Project**: 
   - Click "New Project"
   - "Deploy from GitHub repo" or "Empty Project"

3. **Deploy**: Railway auto-detects everything

4. **Add Variables**:
   ```
   API_KEY=your-secure-key-here
   ```

5. **Get URL**: Railway provides public URL automatically

6. **Test**: Visit your URL + `/api/v1/health`

---

## 🔑 Generate Secure API Key

**Method 1: Python**
```python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Method 2: OpenSSL**
```bash
openssl rand -base64 32
```

**Method 3: Online**
- Visit: https://www.uuidgenerator.net/
- Use API Key Generator

Copy the generated key and use it as your `API_KEY` environment variable.

---

## 📦 Project Setup (If Not Using Git)

If deploying manually:

1. **Download files** or clone repository:
   ```bash
   git clone [your-repo-url]
   cd voice-deepfake-api
   ```

2. **Verify files exist**:
   ```bash
   ls -la
   # Should see: main.py, Dockerfile, requirements.txt, README.md
   ```

3. **Test locally** (optional):
   ```bash
   pip install -r requirements.txt
   python main.py
   # Visit http://localhost:8000/api/v1/health
   ```

---

## 🧪 Quick Test After Deployment

### 1. Health Check
```bash
API_URL="https://your-app.onrender.com"  # Replace with your URL

curl $API_URL/api/v1/health
```

**Expected**:
```json
{
  "status": "healthy",
  "supported_languages": ["tamil", "english", "hindi", "malayalam", "telugu"],
  "timestamp": "2024-02-05T..."
}
```

### 2. API Info
```bash
curl $API_URL/api/v1/info
```

### 3. Test with Sample Audio

Create test file `test.py`:

```python
import requests
import base64

# Your API details
API_URL = "https://your-app.onrender.com/api/v1/analyze"  # CHANGE THIS
API_KEY = "your-api-key-here"  # CHANGE THIS

# Create tiny test audio (silent MP3)
# In production, use real audio file
import io
from pydub import AudioSegment
from pydub.generators import Sine

# Generate 1 second test tone
tone = Sine(440).to_audio_segment(duration=1000)
buffer = io.BytesIO()
tone.export(buffer, format="mp3")
audio_base64 = base64.b64encode(buffer.getvalue()).decode()

# Make request
response = requests.post(
    API_URL,
    headers={"X-API-Key": API_KEY},
    json={"audio_base64": audio_base64, "language": "english"}
)

print("Status:", response.status_code)
print("Response:", response.json())
```

Run:
```bash
pip install requests pydub
python test.py
```

---

## 📝 Your Submission Details

Fill this out after deployment:

```
✅ DEPLOYED API DETAILS

API Endpoint: https://_________________/api/v1/analyze
API Key: _________________________________
Platform: [ ] Render [ ] Railway [ ] Other: _______

Health Check URL: https://_________________/api/v1/health
Status: [ ] Working [ ] Not Working

Test Result:
[ ] Successfully analyzed test audio
[ ] Got classification response
[ ] Got confidence score
[ ] Response format correct

Deployment Time: _____ minutes
Issues Encountered: _________________
```

---

## 🎯 Quick Troubleshooting

### Problem: Build fails
**Solution**: Check Dockerfile syntax, ensure all files committed

### Problem: API returns 403
**Solution**: Check API key matches between client and server

### Problem: API times out
**Solution**: 
- Free tier may have cold starts (first request slow)
- Increase timeout to 60s in your test
- Wait 30 seconds and try again

### Problem: Can't access API
**Solution**:
- Check deployment logs
- Verify URL is correct
- Try health check first
- Check platform status page

---

## ⏱️ Timeline Checklist

**Minutes 0-5: Setup**
- [ ] Choose platform (Render recommended)
- [ ] Create account
- [ ] Generate API key
- [ ] Have GitHub repo ready (or manual deploy)

**Minutes 5-10: Deploy**
- [ ] Create web service
- [ ] Configure environment variables
- [ ] Start deployment
- [ ] Wait for build to complete

**Minutes 10-13: Test**
- [ ] Test health endpoint
- [ ] Test API info endpoint
- [ ] Verify API key authentication

**Minutes 13-15: Document**
- [ ] Record API URL
- [ ] Record API key
- [ ] Test one full request
- [ ] Prepare submission

---

## 🎓 Pro Tips

1. **Use Free Tier Initially**: Test everything before upgrading
2. **Keep API Key Safe**: Don't commit to Git, use environment variables
3. **Test Before Submitting**: Always verify API works from external network
4. **Have Backup**: Deploy to 2 platforms if possible
5. **Monitor Logs**: Keep deployment logs open during submission
6. **Read Docs**: Each platform has specific quirks

---

## 📞 Getting Help

If stuck:

1. **Check Platform Docs**:
   - Render: https://render.com/docs
   - Railway: https://docs.railway.app

2. **Review Logs**: Most issues visible in deployment logs

3. **Test Locally First**: Run `python main.py` to verify code works

4. **Common Issues**: See DEPLOYMENT.md troubleshooting section

---

## ✅ Pre-Submission Verification

Before submitting, verify:

```bash
# 1. Health check works
curl https://your-api.com/api/v1/health

# 2. Info works  
curl https://your-api.com/api/v1/info

# 3. Authentication works
curl -X POST https://your-api.com/api/v1/analyze \
  -H "X-API-Key: wrong-key" \
  -d '{"audio_base64":"test","language":"english"}'
# Should return 403

# 4. Valid request works (with real audio)
curl -X POST https://your-api.com/api/v1/analyze \
  -H "X-API-Key: your-real-key" \
  -H "Content-Type: application/json" \
  -d '{"audio_base64":"[real-base64]","language":"english"}'
# Should return classification
```

All 4 must pass! ✓

---

## 🎉 You're Ready!

Once all checks pass:

1. ✅ Note your API endpoint URL
2. ✅ Note your API key  
3. ✅ Fill out submission form
4. ✅ Submit!
5. ✅ Keep API running during evaluation

**Total Time**: 15 minutes or less!

---

## 🚨 Emergency: Something Broke?

**30 minutes before deadline?**

1. Don't panic
2. Check health endpoint
3. Review recent changes
4. Restart application
5. If needed, redeploy from scratch (only 10 min!)
6. Have backup API key ready

**During evaluation?**

1. Monitor uptime
2. Don't make changes
3. Keep logs accessible
4. Be ready to answer questions

---

**Good luck! You've got this! 🎯**
