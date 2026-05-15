# AmexIvestment - Windows Setup Guide

## Quick Start (3 Steps)

### Step 1: Double-click to Install
In your `primelend` folder, **double-click** `setup_windows.bat`

This will:
- Check Python is installed
- Install all dependencies
- Create the database

### Step 2: Start the App
Double-click `run.bat`

Or open PowerShell/CMD in the folder and type:
```
py app.py
```

### Step 3: Open Browser
Go to: http://localhost:5000

---

## If `setup_windows.bat` doesn't work, do this manually:

### 1. Open PowerShell in your primelend folder
Right-click in the folder → "Open PowerShell window here"

### 2. Install dependencies using `py -m pip`:
```powershell
py -m pip install --upgrade pip
py -m pip install flask flask-sqlalchemy flask-bcrypt flask-login flask-mail werkzeug jinja2
```

### 3. Create the database:
```powershell
py -c "from app import app, db; app.app_context().push(); db.create_all(); print('Done!')"
```

### 4. Run the app:
```powershell
py app.py
```

---

## Default Login

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@amexivestment.com | admin123 |

---

## Troubleshooting

### "py is not recognized"
- Download Python from https://python.org/downloads
- During install, CHECK "Add Python to PATH"
- Restart PowerShell after install

### "Permission denied" when installing
Run PowerShell as Administrator:
1. Press Windows key
2. Type "PowerShell"
3. Right-click → "Run as administrator"
4. Navigate to your primelend folder: `cd C:\Users\LONA\Desktop\primelend`
5. Run the commands above

### Port 5000 already in use
Edit `app.py`, change the last line from:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```
to:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```
Then open http://localhost:5001

---

## Making it Live (Free Hosting)

### Option 1: PythonAnywhere (Easiest)
1. Go to https://www.pythonanywhere.com
2. Sign up for free
3. Upload your primelend folder
4. Follow their Flask setup guide
5. Get a free `yourname.pythonanywhere.com` URL

### Option 2: Ngrok (Temporary live URL)
```powershell
py -m pip install pyngrok
py -m ngrok http 5000
```
This gives you a public URL like `https://abc123.ngrok.io` that anyone can visit!

---

Happy lending!
