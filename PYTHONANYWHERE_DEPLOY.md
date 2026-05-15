# AmexIvestment - PythonAnywhere Deployment Guide

## Step 1: Sign Up (FREE)
1. Go to https://www.pythonanywhere.com
2. Click "Start running Python online in less than a minute"
3. Create account (username = your choice, remember it!)
4. Confirm email

## Step 2: Upload Your Files
1. In PythonAnywhere Dashboard, go to **Files** tab
2. Click **"Upload a file"** or use **"Open Bash console"**
3. Upload your entire `amexinvestment` folder (or ZIP and extract)

OR use Git:
```bash
git clone https://github.com/YOUR_USERNAME/amexinvestment.git
```

## Step 3: Install Dependencies
Open a **Bash console** and run:
```bash
cd amexinvestment
pip install --user -r requirements.txt
```

## Step 4: Create Web App
1. Go to **Web** tab
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Select **Python 3.10** (or latest)
5. Click **Next**

## Step 5: Configure WSGI
1. In Web tab, click **WSGI configuration file** link
2. Replace EVERYTHING with this:

```python
import sys
path = '/home/YOUR_USERNAME/amexinvestment'
if path not in sys.path:
    sys.path.insert(0, path)

from app import app as application
```

Replace `YOUR_USERNAME` with your actual PythonAnywhere username.

3. **Save**

## Step 6: Set Working Directory
1. In Web tab, find **"Working directory"**
2. Set it to: `/home/YOUR_USERNAME/amexinvestment`
3. Click the green checkmark to save

## Step 7: Initialize Database
Open Bash console:
```bash
cd amexinvestment
python fix_admin.py
```

## Step 8: Reload Web App
Click the big green **"Reload"** button on the Web tab.

## Step 9: Test Your Site
Your site is now live at:
```
https://YOUR_USERNAME.pythonanywhere.com
```

Login with:
- Email: admin@amexivestment.com
- Password: admin123

## Step 10: Connect Your Domain (GoDaddy)

### In PythonAnywhere:
1. Web tab → click your app
2. Scroll to **"Custom domains"**
3. Enter: `amexivestment.com`
4. Click **"Add"**
5. Note the **CNAME target** shown (like `YOUR_USERNAME.pythonanywhere.com`)

### In GoDaddy:
1. Log in → My Products → DNS → Manage
2. Add these records:

```
Type: A Record     Host: @     Value: 35.172.51.6      TTL: 600
Type: CNAME Record Host: www   Value: YOUR_USERNAME.pythonanywhere.com  TTL: 600
```

3. Save

### Back in PythonAnywhere:
1. Web tab → click **"Enable HTTPS"**
2. Let PythonAnywhere generate free SSL certificate
3. Done! Your site is now https://amexivestment.com

## Step 11: Set Up Zoho Email (FREE)

1. Go to https://www.zoho.com/mail/
2. Sign up for **Forever Free Plan** (up to 5 users)
3. Choose "Add domain" → Enter: `amexivestment.com`
4. Verify domain ownership:
   - Zoho gives you a TXT record
   - Add it in GoDaddy DNS
5. Create email: `support@amexivestment.com`
6. Update `app.py` with your Zoho password
7. Restart your app

## Step 12: Set Up Google reCAPTCHA (FREE)

1. Go to https://www.google.com/recaptcha/admin
2. Sign in with Google account
3. Click **"Create"**
4. Label: `AmexIvestment`
5. Choose **reCAPTCHA v2** → **"I'm not a robot" Checkbox**
6. Domains: `amexivestment.com`, `www.amexivestment.com`
7. Accept terms → Submit
8. Copy:
   - **Site key** → paste into `templates/register.html` and `index.html`
   - **Secret key** → paste into `app.py`
9. Reload your web app

## Troubleshooting

### "Module not found"
```bash
pip install --user flask flask-sqlalchemy flask-bcrypt flask-login flask-mail requests
```

### "Database locked"
SQLite doesn't work well on PythonAnywhere free tier for multiple workers.
Consider upgrading to MySQL (free with paid plan) or use a single worker.

### Site shows "Coming Soon"
You uploaded to wrong folder. Make sure files are in `/home/YOUR_USERNAME/amexinvestment/`

## Going Live Checklist

- [ ] Domain connected (amexivestment.com loads your site)
- [ ] SSL working (https:// shows green lock)
- [ ] Admin login works
- [ ] Registration works
- [ ] reCAPTCHA shows on signup
- [ ] Contact form sends to support@amexivestment.com
- [ ] Stripe payments configured (optional)

## Support
PythonAnywhere forums: https://www.pythonanywhere.com/forums/
