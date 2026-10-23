# Jenkins + GitHub CI/CD Demo

A Flask application demonstrating Jenkins checkout, dependency installation, automated tests, Docker image build, deployment, and live HTTP verification.

## Contents
- `app.py` — Flask application with `/` and `/health`.
- `tests/test_app.py` — automated tests.
- `requirements.txt` — Python dependencies.
- `Dockerfile` — container image definition.
- `Jenkinsfile` — pipeline as code.

## Prerequisites
The Jenkins build agent needs Git, Python 3, Docker Engine/CLI, and curl. The Jenkins agent account must be able to run Docker commands. Docker socket access is effectively root-level access; use a dedicated trusted agent and do not run untrusted pull-request jobs on it. Docker installation instructions: https://docs.docker.com/engine/install/

Install the Jenkins **Pipeline** and **Git** plugins. This Jenkinsfile uses the Docker CLI directly, so the Docker Pipeline plugin is not required.

## 1. Push to GitHub
Create an empty GitHub repository, extract these files into it, then run:

```bash
git init
git add .
git commit -m "Add Jenkins CI/CD demo"
git branch -M main
git remote add origin https://github.com/YOUR-USER/YOUR-REPO.git
git push -u origin main
```

Replace `YOUR-USER/YOUR-REPO` with your repository path.

## 2. Create the Jenkins job
1. Select **New Item**, enter `github-flask-cicd`, and choose **Pipeline**.
2. Under **Pipeline**, set **Definition** to **Pipeline script from SCM**.
3. Select **Git**, enter the repository URL, add credentials if private, and set branch to `*/main`.
4. Set **Script Path** to `Jenkinsfile`, save, and click **Build Now**.

## 3. Enable automatic GitHub builds
For a public, reachable Jenkins server:
1. In the job configuration, enable **GitHub hook trigger for GITScm polling** if available.
2. In GitHub, open **Settings → Webhooks → Add webhook**.
3. Payload URL: `https://YOUR-JENKINS-URL/github-webhook/`
4. Content type: `application/json`; select push events and save.
5. Confirm GitHub reports successful delivery.

Jenkins must be reachable by GitHub for webhooks. For a local lab, enable **Poll SCM** instead, for example `H/2 * * * *` (roughly every two minutes).

## 4. Verify deployment
After a successful pipeline, on the Docker host run:

```bash
docker ps --filter name=jenkins-github-cicd-demo
curl --fail http://127.0.0.1:5000/health
curl --fail http://127.0.0.1:5000/
```

Expected `/health` response:

```json
{"status":"healthy"}
```

The home endpoint returns JSON containing `"application":"Jenkins CI/CD Demo"` and `"message":"Deployment successful!"`. The pipeline checks both endpoints and fails if the health check does not become ready or the expected response is absent.

## 5. Test continuous deployment
Edit `app.py`, commit, and push:

```bash
git add app.py
git commit -m "Update application response"
git push
```

A webhook (or SCM polling) should trigger a new run. Check Jenkins **Console Output** and use `curl` to verify the updated response.

## Notes
- This sample deploys to the Docker host accessible to the Jenkins agent and publishes port 5000. Ensure it is free and allowed by the firewall.
- For a separate production server, use a dedicated deployment agent or secure SSH deployment with Jenkins-managed credentials, and change the verification URL to the target host.
- This demonstration removes the old container before starting the new one. Production deployments should use health-gated replacement and rollback to the last known-good image.
- Do not expose Jenkins publicly without HTTPS, authentication, and appropriate network controls.
