# fullstack-vibebuilder
# 🚀 Full-Stack Vibe Coding: 5-Day Portfolio App Course

Theme: **Build Fast. Ship Clean. Feel the Vibe.**

Build and deploy a modern full-stack portfolio app using **Tech Stack**
Backend: **Java, Spring Boot, concepts related to API/RestAPI, MVC**,
Frontend: **React** 
Database: **SQL, MySql, MySqlWorkbench IDE**
Devops: Git, GitHub, concepts related to CI-CD pipelines(Github Actions), Dockerisation
Deployment: Free/Open-source providers like Vercel

---

## 🧱 Tech Stack Details

### Backend
- Java + Spring Boot (Spring Annotations, API. REST API Development)
- Spring Data REST (concepts related to ORM, SQL)
- MySQL Database with MySQL Workbench IDE

### Frontend
- React (Vite)
- Axios

### Tools
- Git + GitHub
- Postman
- Docker

---

## 📅 Course Roadmap

----------------------------------------------------------------------------------
## 🚀 Task 1 — Backend Foundations

### Goal 1.1
Set up a working Spring Boot API

### Topics
- Full-stack architecture overview(with examples)
- Spring Boot concepts
- REST API design
- MVC(Controllers, Services, Models)

### Build
- Initialize project (Spring Initializr)
- Add dependencies:
  - Spring Web
  - Spring Data JPA
  - MySQL / H2

### Features(Portfolio Project)
- GET,POST,DELETE,UPATE Crud for Projects,Profiles,Technologies etc

### Example Model
```java
class Project {
  Long id;
  String title;
  String description;
  String techStack;
  String githubUrl;
}

Delivery:-
1) Architect flow for MVC, REST API
2) Integration of Claude/Copilot in VSCode IDE, and refactoring task using Claude as below:-
"Each project should have a list of technologies listed 
i.e Project model should have a list, List<Technology>"
3) Git essentials and demo to push to a git repo/branch(From now on, students to keep pushing code to git)

4) Students Practice Exercise:
"Using Claude, design the backend of a fresh project starting from scratch. 
Some suggestions: BankingApp, RetailApp, MoviePlayStoreApp etc"
PortfolioApp to be used for traienr demo throughout, and/or personal apps like above can be used by students for self-practice throughout for the rest of the course

### Goal 1.2
1) Demo TDD(TestDrivenDevelopment)(Junit, Mockito) using "Profiles:GetAll,GetByID etc"

### Goal 1.3
1) API Testing using Postman

### Goal 1.4
1) API Documentation using Swagger
---------------------------------------------------------------------------------------------

## 🚀 Task 2 — Frontend Foundations
1) React concepts and creating foundational React UI
2) Explain general idea of React concepts(Components, Parent/Child Component with nesting, props and props system, passing props between parent to child and vice-versa, JSX, Routing, Hooks system like useState, useEffect, Services/Data or API Service, Consuming API, DOM Vs Virtual DOM, tables, styling, conditional rendering in UI)
--Using Claude/VibeCoding

---------------------------------------------------------------------------------------------

## 🚀 Task 3 — Connecting Frontend With Backend API
-- understanding API calls, browser network tab, debugging techniques, understanding and resolving errors such as CORS errors

-----------------------------------------------------------------
## 🚀 Task 4 — Connecting Backend API With Database using Spring-Data-Rest/Mysql
-- basic concepts of SQL, SpringDataRest, mappings, custom methods, understanding application.properties(for db properties) and pom.xml(for dependencies)

-----------------------------------------------------------------
## 🚀 Task 5 — CiCd Pipeline with Github Actions
--understand CiCd workflow/pipelines, yaml configuration, test cases/runners, invocation, understanding pipeline errors and resolution

------------------------------------------------------------------
## 🚀 Task 7 — Containerisation With Docker

------------------------------------------------------------------
## 🚀 Task 8 — Exposure to non-relational databases like MongoDB

-------------------------------------------------------------------
## 🚀 Task 9 — Deployment on Vercel, Render and/or cloud vendors etc

--------------------------------------------------------------------
## 🚀 Task 10: Best-Practices(SonarLint/SonarCube) & Security considerations(CORS,XSS,Phising,SQL-Injection,Validations,Hashing Passwords)

---------------------------------------------------------------------------
## 🚀 Task 11: Performance considerations(caching, pagination) etc


----------------------------------------------------------------------------
## 🚀 Task 12: Data-Structure Optimizations

----------------------------------------------------------------------------
## 🚀 Task 13: Design Standards and System Design/Architecture Foundations
--Threads and Concurrency
--Singleton
--Factory
--MVC
--Monoliths Vs Microservices(Web Client for Inter-Services-Communication)
--CQRS
--Apache Kafka/Message Queue

-------------------------------------------------------------------------
## 🚀 Task 14: Miscellaneous Topics
--Logging, Monitoring, Instrumentation, Eureka
--Cloud Foundations

