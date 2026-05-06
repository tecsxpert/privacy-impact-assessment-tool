# Privacy Impact Assessment Tool

An AI-powered web application for managing Privacy Impact
Assessments built as an internship capstone project.

## Team
- Java Developer 1: Raksha V Kadagi
- Java Developer 2: Bhavani Rajshekhar Bhavanur

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Java 17, Spring Boot 3.x |
| Database | PostgreSQL 15 |
| Cache | Redis 7 |
| Migrations | Flyway |
| Security | Spring Security + JWT |
| AI Service | Python Flask, Groq API |
| Frontend | React 18, Vite, Tailwind CSS |
| Charts | Recharts |
| Docs | Swagger/OpenAPI |
| Container | Docker + Docker Compose |

## Prerequisites

Before running this project install:
- Java 17 (https://adoptium.net)
- Node 20 LTS (https://nodejs.org)
- Maven 3.9+ (https://maven.apache.org)
- Docker Desktop (https://docker.com)
- Git 2.x (https://git-scm.com)

## Setup Instructions

### Step 1 — Clone Repository
```bash
git clone https://github.com/tecsxpert/privacy-impact-assessment-tool.git
cd privacy-impact-assessment-tool
```

### Step 2 — Create .env File
```bash
cp .env.example .env
```
Fill in your actual values in `.env`

### Step 3 — Run with Docker
```bash
docker-compose up --build
```

### Step 4 — Access Application
- Frontend: http://localhost
- Backend API: http://localhost:8080
- Swagger UI: http://localhost:8080/swagger-ui.html
- AI Service: http://localhost:5000

## Run Without Docker

### Frontend Only
```bash
cd frontend
npm install
npm run dev
```
Access at: http://localhost:5173

### Backend Only
```bash
cd backend
mvn clean install -DskipTests
mvn spring-boot:run
```

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| DB_URL | PostgreSQL URL | jdbc:postgresql://localhost:5432/privacy_tool |
| DB_USERNAME | Database username | postgres |
| DB_PASSWORD | Database password | postgres |
| REDIS_HOST | Redis host | localhost |
| REDIS_PORT | Redis port | 6379 |
| JWT_SECRET | JWT secret key | mySecretKey123 |

## API Endpoints (Java Developer 2)

| Method | Endpoint | Description |
|---|---|---|
| PUT | /api/assessments/{id} | Update assessment |
| DELETE | /api/assessments/{id} | Soft delete |
| GET | /api/assessments/search | Search and filter |
| GET | /api/assessments/export | Export CSV |
| GET | /api/assessments/stats | Dashboard stats |
| POST | /api/assessments/{id}/upload | Upload file |

## Features

### Frontend (Java Developer 2)
- Login page with JWT authentication
- Dashboard with 4 KPI cards and Recharts charts
- Assessment list with debounced search
- Status dropdown and date range filter
- Create and edit assessment form with validation
- Detail page with AI panel
- Analytics page with line and bar charts
- CSV export functionality
- Responsive design (mobile/tablet/desktop)
- Audit logging via Spring AOP

### Backend (Java Developer 2)
- REST endpoints PUT/DELETE/search/export
- Flyway V1 and V2 database migrations
- Swagger/OpenAPI documentation
- File upload with type and size validation
- MockMvc tests (10 tests)

## Project Structure
privacy-impact-assessment-tool/
├── backend/                 ← Spring Boot
│   ├── src/main/java/
│   │   └── com/internship/tool/
│   │       ├── controller/
│   │       ├── service/
│   │       ├── entity/
│   │       ├── repository/
│   │       ├── config/
│   │       └── dto/
│   └── src/main/resources/
│       └── db/migration/
├── frontend/                ← React + Vite
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       └── context/
├── ai-service/              ← Flask Python
├── docker-compose.yml
├── .env.example
└── README.md

## Demo Video
See `demo_video.mp4` in root folder for 90 second
feature walkthrough.

## Sprint
April 14 – May 9, 2026
Demo Day: May 9, 2026