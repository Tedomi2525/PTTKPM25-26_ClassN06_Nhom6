# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

QLDT (Quản Lý Đào Tạo) is a **full-stack academic management system** with facial recognition attendance features. The project consists of:

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL with facial recognition using YOLO
- **Frontend**: Nuxt.js 4 + TailwindCSS + Vue.js 3
- **Database**: PostgreSQL 17.6 with Alembic migrations
- **AI Component**: Face detection and recognition system using YOLOv8

## Development Commands

### Backend (Python/FastAPI)

**Setup and Installation:**
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Database Operations:**
```bash
# Run database migrations (if Alembic is configured)
alembic revision --autogenerate -m "migration message"
alembic upgrade head

# Or use the provided SQL file
# Import qldt.sql into PostgreSQL database named 'qldt'
```

**Development Server:**
```bash
# Start FastAPI development server with hot reload
uvicorn app.main:app --reload

# Server runs on http://127.0.0.1:8000
# API docs available at http://127.0.0.1:8000/docs
```

### Frontend (Nuxt.js)

**Setup and Development:**
```bash
# Navigate to frontend directory
cd new-frontend

# Install dependencies
npm install

# Start development server
npm run dev
# Server runs on http://localhost:3000

# Build for production
npm run build

# Preview production build
npm run preview
```

### Full Stack Development

**Start both services:**
```bash
# Terminal 1: Backend
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload

# Terminal 2: Frontend  
cd new-frontend
npm run dev
```

## Architecture Overview

### Backend Architecture (FastAPI)

The backend follows a **layered architecture pattern** with clear separation of concerns:

**Core Structure:**
- `app/main.py` - FastAPI application entry point with CORS middleware and router registration
- `app/database.py` - SQLAlchemy database configuration and session management
- `app/core/` - Configuration management and security utilities (JWT, password hashing)

**Domain Layers:**
- `models/` - SQLAlchemy ORM models representing database tables
- `schemas/` - Pydantic models for request/response validation and serialization
- `services/` - Business logic layer containing core domain operations
- `routers/` - FastAPI route handlers (controllers) that orchestrate requests

**Key Models and Relationships:**
- `User` → `Teacher`/`Student` (role-based inheritance)
- `Program` → `Course` → `CourseClass` (academic hierarchy)
- `Schedule`/`ScheduleTemplate` (timetabling system)
- `Attendance` + `StudentFaces` (facial recognition attendance)
- `Room`/`Period` (resource management)

**Face Recognition System:**
- `face_service/detector/` - YOLOv8-based face detection
- `face_service/embedding/` - Face embedding generation for recognition
- `face_service/face_alignment/` - MTCNN face alignment preprocessing
- Integration with attendance tracking in main application

### Frontend Architecture (Nuxt.js)

**Framework Configuration:**
- **SSR enabled** for proper routing and SEO
- **TailwindCSS** for utility-first styling
- **Vue 3 Composition API** as the reactive framework

**Component Organization:**
- Reusable UI components in `components/` (CButton, DataTable, DropDown, etc.)
- Page-based routing following Nuxt conventions
- FullCalendar integration for schedule visualization

### Database Design

The system uses **PostgreSQL** with a normalized schema supporting:
- **Multi-role user system** (admin, teacher, student)
- **Academic program management** with flexible course-program relationships
- **Timetable generation** with template-based scheduling
- **Facial recognition attendance** with face embedding storage

### Development Patterns

**Service Layer Pattern:** Business logic is encapsulated in service classes, keeping routers thin and focused on HTTP concerns.

**Repository Pattern:** Database operations are abstracted through SQLAlchemy ORM with session dependency injection.

**Schema Validation:** All API inputs/outputs use Pydantic schemas for type safety and validation.

**Authentication Flow:** JWT-based authentication with role-based access control integrated into route dependencies.

## Environment Configuration

**Required Environment Variables (.env in backend/):**
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT signing secret
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time

**Database Requirements:**
- PostgreSQL 17.6+
- Database name: `qldt`
- Connection example: `postgresql://postgres:password@localhost:5432/qldt`

## API Structure

The API follows RESTful conventions with these main endpoint groups:
- `/auth/*` - Authentication and authorization
- `/api/users/*` - User management (admin, teacher, student)
- `/api/courses/*` - Course and class management
- `/api/programs/*` - Academic program management  
- `/api/schedules/*` - Timetable and scheduling
- `/api/attendances/*` - Attendance tracking with facial recognition
- `/api/rooms/*` - Room and resource management

## Common Development Scenarios

**Adding a new model:**
1. Create SQLAlchemy model in `models/`
2. Create Pydantic schemas in `schemas/`
3. Implement service logic in `services/`
4. Add router endpoints in `routers/`
5. Generate and apply Alembic migration

**Facial Recognition Integration:**
- Face detection uses YOLOv8 model (`yolov8n-face.pt`)
- Face embeddings stored in `student_faces` table
- Attendance verification compares live face with stored embeddings

**Frontend API Integration:**
- Use Axios for HTTP requests to backend API
- Backend CORS configured for `localhost:3000` and `localhost:3001`
- Authentication tokens managed client-side for API calls