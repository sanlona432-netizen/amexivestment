# AmexIvestment - Render.com Deployment Guide

## Step 1: Push to GitHub
1. Create GitHub repo: `amexinvestment`
2. Upload all your files
3. Make sure `requirements.txt` is in root

## Step 2: Sign Up on Render
1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repos

## Step 3: Create Web Service
1. Dashboard → **"New +"** → **"Web Service"**
2. Connect your `amexinvestment` GitHub repo
3. Settings:
   - **Name:** `amexinvestment`
   - **Region:** Oregon (US West) or Ohio (US East)
   - **Branch:** `main`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Click **"Create Web Service"**

## Step 4: Environment Variables
In Render dashboard → your app → **Environment**:
```
SECRET_KEY = amexinvestment-secret-key-2026-secure
DATABASE_URL = sqlite:///amexinvestment.db
MAIL_USERNAME = support@amexivestment.com
MAIL_PASSWORD = YOUR_ZOHO_APP_PASSWORD
RECAPTCHA_SECRET_KEY = YOUR_RECAPTCHA_SECRET_KEY
```

## Step 5: Initialize Database
In Render → **Shell** tab:
```bash
python fix_admin.py
```

## Step 6: Custom Domain
1. Render → your app → **Settings** → **Custom Domains**
2. Add: `amexivestment.com`
3. Add: `www.amexivestment.com`
4. Copy the **DNS Target** shown

## In GoDaddy DNS:
```
Type: CNAME  Host: www  Value: [Render DNS Target]  TTL: 600
Type: A      Host: @    Value: 76.76.21.21           TTL: 600
```

## Step 7: SSL
Render auto-provides free SSL for custom domains. Just wait 10 minutes.

## Done!
Your site is live at https://amexivestment.com
