# 🚀 Quick Deployment Guide

## Deploy to Streamlit Cloud (FREE)

### Step 1: Create GitHub Repository

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Gym Exercise Database"

# Create a new repository on GitHub (go to github.com/new)
# Then link it:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. **Go to**: [share.streamlit.io](https://share.streamlit.io)
2. **Sign in** with your GitHub account
3. **Click** "New app" button
4. **Fill in**:
   - Repository: `YOUR_USERNAME/YOUR_REPO_NAME`
   - Branch: `main`
   - Main file path: `app.py`
5. **Click** "Deploy!"

⏱️ Your app will be live in 2-3 minutes!

### Step 3: Access Your App

Your app will be available at:
```
https://YOUR_USERNAME-YOUR_REPO_NAME.streamlit.app
```

## What Gets Deployed

✅ Your Python app (`app.py`)  
✅ Your data (`cb.csv`)  
✅ Dependencies (`requirements.txt`)  
✅ Theme settings (`.streamlit/config.toml`)  

## Updating Your App

After making changes:

```bash
git add .
git commit -m "Description of changes"
git push
```

Streamlit Cloud will **automatically redeploy** your app! 🎉

## Troubleshooting

### App won't start?
- Check the logs in Streamlit Cloud dashboard
- Make sure `cb.csv` exists in your repository
- Verify `requirements.txt` has all dependencies

### Need help?
- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Community Forum](https://discuss.streamlit.io)

## Alternative: Deploy to Vercel (Advanced)

If you prefer Vercel, you'll need to:
1. Convert the Streamlit app to Next.js/Flask
2. Set up API routes
3. Configure Vercel deployment

**Recommendation**: Stick with Streamlit Cloud for this app - it's designed for Python data apps!

