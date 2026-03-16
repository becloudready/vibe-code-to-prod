# CI/CD Template Project

This repository contains a minimal template for a front-end project with a simple CI workflow.

## 📁 Structure

```
ci-cd-template/
│
├ .github/
│   └ workflows/
│        └ ci.yml
│
├ scripts/
│     └ run-tests.sh
│
├ Dockerfile.example
│
├ README.md
│
└ myapp/
   ├ index.html
   ├ styles.css
   └ script.js
```

## 🚀 Running Locally

Open `myapp/index.html` in your browser.

## 🧪 CI

GitHub Actions is configured in `.github/workflows/ci.yml` to run `scripts/run-tests.sh` on push and pull requests.

## 🐳 Docker (Optional)

To build and run the example Docker container:

```sh
cp Dockerfile.example Dockerfile
docker build -t ci-cd-template .
docker run --rm -p 8080:80 ci-cd-template
```

Then open http://localhost:8080 in your browser.
