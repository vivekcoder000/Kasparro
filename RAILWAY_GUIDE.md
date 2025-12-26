# 🚂 Railway Deployment Guide

Here is the **COMPLETE** recommended setup for your project.

## 1. Create the Project
1.  Log in to [Railway.app](https://railway.app/).
2.  Click **"New Project"** -> **"Deploy from GitHub repo"**.
3.  Select your repository: **`kasparro-vivek-vardhan`**.
4.  Click **"Deploy Now"**.

## 2. Add a Database (Crucial Step)
Your app needs a database. Railway makes this easy.
1.  In your project view, click the **"New"** button (top right or big card).
2.  Select **"Database"** -> **"PostgreSQL"**.
3.  Wait a moment for it to appear.

## 3. Connect the App to the Database
Now tell your Backend to use that new Database.
1.  Click on the **PostgreSQL** card.
2.  Go to the **"Variables"** tab.
3.  Copy the value of **`DATABASE_URL`**.
4.  Close that card.
5.  Click on your **Backend application** card (`kasparro-vivek-vardhan`).
6.  Go to the **"Variables"** tab.
7.  Click **"New Variable"** and add these two:

| Variable Name | Value |
| :--- | :--- |
| `API_KEY` | `testkey` |
| `DATABASE_URL` | *(Paste the URL you copied from the Database card)* |

## 4. Final Success
- Once you add the variables, Railway will automatically **Restart** (Redeploy) your app.
- Watch the **"Deployments"** tab.
- **Generate Public URL (Crucial Step)**:
    1.  **Click the Purple Service Card** on the main canvas (titled `kasparro-backend`).
    2.  A pane will open on the right. Click the **Settings** tab *inside that pane*.
    3.  Scroll down to **Networking**.
    4.  Click **"Generate Domain"**.
- Go to `https://<YOUR_DOMAIN>/health` to verify it's working!
