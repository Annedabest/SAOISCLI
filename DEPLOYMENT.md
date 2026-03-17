# SAOIS Website Deployment Guide

## Deploying to Coolify

### Prerequisites
- Coolify instance running
- GitHub repository connected to Coolify
- Domain configured: `saois.cli.victorconsultancy.cloud`

### Step 1: Push to GitHub

```bash
cd SAOISCLI
git add .
git commit -m "v2.0.0 - Simplified CLI with landing page"
git push origin main
```

### Step 2: Create New Application in Coolify

1. **Login to Coolify Dashboard**
2. **Click "New Resource" → "Application"**
3. **Select "GitHub" as source**
4. **Choose repository:** `Annedabest/SAOISCLI`
5. **Select branch:** `main`

### Step 3: Configure Build Settings

| Setting | Value |
|---------|-------|
| **Build Pack** | Dockerfile |
| **Dockerfile Location** | `website/Dockerfile` |
| **Build Context** | `website` |
| **Port** | 80 |

### Step 4: Configure Domain

1. **Go to "Domains" tab**
2. **Add domain:** `saois.cli.victorconsultancy.cloud`
3. **Enable HTTPS** (Let's Encrypt)
4. **Force HTTPS:** Yes

### Step 5: Environment Variables (Optional)

No environment variables required for static site.

### Step 6: Deploy

1. **Click "Deploy"**
2. **Wait for build to complete** (~1-2 minutes)
3. **Verify at:** https://saois.cli.victorconsultancy.cloud

---

## Alternative: Manual Docker Deployment

If not using Coolify's GitHub integration:

```bash
# Build the image
cd website
docker build -t saois-website .

# Run the container
docker run -d -p 80:80 --name saois-website saois-website
```

---

## DNS Configuration

Add these DNS records to your domain:

| Type | Name | Value |
|------|------|-------|
| A | saois.cli | [Your Coolify Server IP] |
| CNAME | www.saois.cli | saois.cli.victorconsultancy.cloud |

---

## Verification Checklist

After deployment, verify:

- [ ] Homepage loads at https://saois.cli.victorconsultancy.cloud
- [ ] Documentation page loads at /docs.html
- [ ] Download link works
- [ ] All images/assets load
- [ ] HTTPS certificate is valid
- [ ] Mobile responsive design works

---

## Updating the Website

To update after deployment:

```bash
# Make changes to website/ files
git add .
git commit -m "Update website"
git push origin main

# Coolify will auto-deploy if webhook is configured
# Or manually trigger deploy in Coolify dashboard
```

---

## Rollback

If something goes wrong:

1. Go to Coolify Dashboard
2. Click on the application
3. Go to "Deployments" tab
4. Click "Rollback" on a previous successful deployment
