# Deploy to GitHub Pages

## Option 1: GitHub Pages (Recommended - Free)

1. **Create a new GitHub repository:**
   ```bash
   git init
   git add parallel_gtm_landing.html
   git commit -m "Add Parallel GTM landing page"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/parallel-gtm-landing.git
   git push -u origin main
   ```

2. **Enable GitHub Pages:**
   - Go to your repository on GitHub
   - Click "Settings" → "Pages"
   - Select "Deploy from a branch"
   - Choose "main" branch and "/ (root)" folder
   - Click "Save"

3. **Your site will be available at:**
   `https://YOUR_USERNAME.github.io/parallel-gtm-landing`

## Option 2: Netlify (Free Tier)

1. **Drag & Drop:**
   - Go to [netlify.com](https://netlify.com)
   - Drag your `parallel_gtm_landing.html` file to the deploy area
   - Get a URL like: `https://random-name.netlify.app`

2. **Custom Domain:** You can add a custom domain later

## Option 3: Vercel (Free Tier)

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Deploy:**
   ```bash
   vercel
   ```

## Option 4: Docker (If you prefer containerization)

Create a simple Dockerfile:

```dockerfile
FROM nginx:alpine
COPY parallel_gtm_landing.html /usr/share/nginx/html/index.html
EXPOSE 80
```

Then:
```bash
docker build -t parallel-gtm-landing .
docker run -p 8080:80 parallel-gtm-landing
```

## Recommendation: GitHub Pages
- ✅ **Free forever**
- ✅ **Simple setup**
- ✅ **Custom domain support**
- ✅ **Automatic HTTPS**
- ✅ **Version control**
- ✅ **Easy updates**

Would you like me to help you set up any of these options?
