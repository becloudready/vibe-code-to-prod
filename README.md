# Vibe Code to Prod

A hands-on bootcamp curriculum for building and shipping full-stack applications to production using AI-assisted (vibe) coding — covering backend APIs, databases, security, testing, infrastructure, and cloud deployment on AWS.

---

## Curriculum

| Chapter | Topic | What's Covered |
|---------|-------|----------------|
| [01 — Vibe Coding](./chapters/01-vibe-coding/) | Fundamentals | Prompting strategies, building a FastAPI app with AI |
| [02 — Backend & Databases](./chapters/02-backend-databases/) | Backend | Employee CRUD API, MongoDB integration |
| [03 — Testing](./chapters/03-testing/) | TDD | TDD cycle, writing tests with AI assistance |
| [04 — Security](./chapters/04-security/) | Auth | API key security, JWT authentication |
| [05 — Infrastructure](./chapters/05-infrastructure/) | IaC | Terraform fundamentals, provisioning AWS resources |
| [06 — Cloud & CI/CD](./chapters/06-cloud-cicd/) | AWS | EC2, Lambda, API Gateway, S3, GitHub Actions |

---

## Projects

| Project | Stack | Description |
|---------|-------|-------------|
| [01 — Task Tracker](./projects/01-task-tracker/) | React + Lambda + MongoDB | Kanban-style task board — full-stack capstone |
| [02 — Notice Board](./projects/02-notice-board/) | React + S3 + Lambda | Assignment project with 3 difficulty tiers |

---

## Prerequisites

- Basic programming knowledge (Python or JavaScript)
- AWS account
- Installed: AWS CLI, Terraform, Node.js, Git

---

## Repository Structure

```
chapters/          # Course content, one folder per chapter
  01-vibe-coding/
  02-backend-databases/
  03-testing/
  04-security/
  05-infrastructure/
  06-cloud-cicd/
    labs/          # Step-by-step lab instructions
    scripts/       # Helper scripts
    starter-apps/  # Starter code for labs
    terraform/     # Terraform templates

projects/          # Capstone and assignment projects
  01-task-tracker/
  02-notice-board/
```

---

## License

MIT
