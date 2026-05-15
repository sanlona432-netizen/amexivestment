# AmexIvestment - Complete Setup & Launch Guide

## PART 1: Local Testing (Do This First)

### Install Dependencies
```bash
py -m pip install --upgrade pip
py -m pip install flask flask-sqlalchemy flask-bcrypt flask-login flask-mail werkzeug jinja2 requests gunicorn
```

### Create Admin & Run
```bash
cd amexinvestment
py fix_admin.py
py app.py
```

Open browser: http://localhost:5000

Login: admin@amexivestment.com / admin123

---

## PART 2: Get Your API Keys (FREE)

### A. Google reCAPTCHA (Stop Spam)
1. Go to: https://www.google.com/recaptcha/admin
2. Sign in with Google
3. Click **"Create"**
4. Label: `AmexIvestment`
5. Choose **reCAPTCHA v2** → **"I'm not a robot" Checkbox**
6. Domains: `amexivestment.com`, `www.amexivestment.com`, `localhost`
7. Accept terms → Submit
8. You'll get TWO keys:
   - **Site key** (starts with `6Ld...`) → Put in HTML files
   - **Secret key** (starts with `6Ld...`) → Put in app.py

### B. Zoho Mail (Professional Email)
1. Go to: https://www.zoho.com/mail/
2. Click **"Sign Up Now"** → Choose **"Forever Free Plan"**
3. Select **"Add Domain"** → Enter: `amexivestment.com`
4. Verify domain:
   - Zoho gives you a TXT record (like `zoho-verification=abc123`)
   - Add it in GoDaddy DNS
5. Create mailbox: `support@amexivestment.com`
6. Generate **App Password** in Zoho settings (not your login password!)

---

## PART 3: Update Your Code With Real Keys

### Edit `app.py`:
Find these lines and replace:
```python
app.config['MAIL_PASSWORD'] = 'YOUR_ZOHO_APP_PASSWORD'
# Change to:
app.config['MAIL_PASSWORD'] = 'your-actual-zoho-app-password'

def verify_recaptcha(token):
    secret_key = 'YOUR_RECAPTCHA_SECRET_KEY'
    # Change to:
    secret_key = 'your-actual-recaptcha-secret-key'
```

### Edit `templates/register.html`:
Find:
```html
data-sitekey="YOUR_RECAPTCHA_SITE_KEY"
```
Change to:
```html
data-sitekey="your-actual-recaptcha-site-key"
```

### Edit `templates/index.html`:
Same change as above for the contact form reCAPTCHA.

---

## PART 4: Deploy to PythonAnywhere (FREE)

Follow `PYTHONANYWHERE_DEPLOY.md` in this folder.

Quick version:
1. Sign up at pythonanywhere.com
2. Upload files via Files tab or Git
3. Install: `pip install --user -r requirements.txt`
4. Web tab → Manual config → Python 3.10
5. Set WSGI file to import your app
6. Set working directory
7. Run `python fix_admin.py` in Bash
8. Reload web app
9. Test at `YOURNAME.pythonanywhere.com`

---

## PART 5: Connect Your GoDaddy Domain

### In PythonAnywhere:
1. Web tab → click your app
2. Add custom domain: `amexivestment.com`
3. Note your PythonAnywhere URL (like `yourname.pythonanywhere.com`)

### In GoDaddy:
1. My Products → DNS → Manage
2. Add records:
```
Type: A Record     Host: @     Value: 35.172.51.6      TTL: 600
Type: CNAME Record Host: www   Value: yourname.pythonanywhere.com  TTL: 600
```
3. Save

### Back in PythonAnywhere:
1. Click **"Enable HTTPS"**
2. Wait 5-30 minutes
3. Visit https://amexivestment.com ✅

---

## PART 6: Stripe Payments (When Ready)

1. Sign up at https://stripe.com
2. Get API keys from Dashboard → Developers → API keys
3. Add `stripe` to requirements.txt
4. Follow Stripe integration code in comments of app.py
5. Switch from test keys (`sk_test_...`) to live keys (`sk_live_...`) when ready

---

## Files in This Package

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application |
| `requirements.txt` | Python dependencies |
| `fix_admin.py` | Create/reset admin account |
| `setup_windows.bat` | One-click Windows setup |
| `run.bat` | One-click start app |
| `templates/` | All HTML pages |
| `SETUP_GUIDE.md` | This file - complete guide |
| `PYTHONANYWHERE_DEPLOY.md` | PythonAnywhere specific |
| `RENDER_DEPLOY.md` | Render.com specific |

---

## Support Contacts

| Issue | Where to Get Help |
|-------|-------------------|
| Domain/DNS | GoDaddy support or community |
| Hosting | PythonAnywhere forums |
| Flask/Python | Stack Overflow |
| Stripe | Stripe Discord or support |
| reCAPTCHA | Google reCAPTCHA docs |
| Zoho Mail | Zoho support |

---

## You're Live! 🚀

Once done, your site will be:
- **URL:** https://amexivestment.com
- **Email:** support@amexivestment.com
- **Admin:** https://amexivestment.com/admin
- **Protected:** reCAPTCHA on all forms

Good luck with AmexIvestment!
