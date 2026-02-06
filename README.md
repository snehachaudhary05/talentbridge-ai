# TalentBridge AI - Intelligent Job Portal

A modern, full-stack job portal application with AI-powered candidate screening, built with Django REST Framework and Vue 3.

## Features

### For Candidates
- **Smart Job Search** - Browse and filter jobs by type, location, and salary
- **AI Resume Analysis** - Upload resume for instant AI-powered analysis and suggestions
- **Job Matching** - Get matched with relevant jobs based on skills and experience
- **Application Tracking** - Track all job applications and their status in real-time
- **Interview Management** - View and manage scheduled interviews
- **Saved Jobs** - Bookmark jobs for later review

### For Recruiters
- **Job Posting** - Create and manage job listings with rich descriptions
- **AI Candidate Screening** - Automatically screen candidates using AI analysis
- **Application Management** - Review applications and update candidate status
- **Interview Scheduling** - Schedule and manage interviews with candidates
- **Dashboard Analytics** - View job statistics and application metrics
- **Resume Download** - Access candidate resumes directly from applications

### AI-Powered Features
- **Resume Analysis** - Intelligent parsing and analysis of candidate resumes
- **Candidate Screening** - Automated candidate evaluation against job requirements
- **Job Matching** - AI-driven job recommendations for candidates
- **Smart Insights** - Detailed analysis with strengths, weaknesses, and recommendations

## Tech Stack

### Backend
- **Django 4.2.27** - Python web framework
- **Django REST Framework** - RESTful API development
- **SQLite** - Database (production-ready with PostgreSQL support)
- **JWT Authentication** - Secure token-based authentication
- **OpenRouter API** - AI integration with Gemma 3 12B model

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Vite** - Next-generation frontend tooling
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API requests
- **Pinia** - State management

## Project Structure

```
job-portal/
├── job-portal-backend/          # Django backend
│   ├── accounts/                # User authentication & profiles
│   ├── jobs/                    # Job listings & applications
│   ├── ai_assistant/            # AI screening & analysis
│   ├── notifications/           # Notification system
│   ├── config/                  # Django settings
│   └── manage.py
│
└── frontend/                    # Vue 3 frontend
    ├── src/
    │   ├── views/               # Page components
    │   ├── components/          # Reusable components
    │   ├── stores/              # Pinia state management
    │   └── router/              # Vue Router configuration
    └── package.json
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd job-portal-backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env` (if exists) or use the existing `.env`
   - Update sensitive values for production

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server:**
   ```bash
   python manage.py runserver
   ```

   Backend will be available at `http://127.0.0.1:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run development server:**
   ```bash
   npm run dev
   ```

   Frontend will be available at `http://localhost:5173`

## Configuration

### Environment Variables

Create a `.env` file in `job-portal-backend/` with:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite by default, no configuration needed)

# AI Configuration
OPENROUTER_API_KEY=your-openrouter-api-key
OPENROUTER_MODEL=google/gemma-3-12b-it:free

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:5173

# Email Configuration (Optional)
RESEND_API_KEY=your-resend-api-key
EMAIL_FROM=noreply@yourdomain.com
FRONTEND_URL=http://localhost:5173
```

## API Documentation

### Authentication Endpoints
- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/login/` - User login
- `POST /api/accounts/token/refresh/` - Refresh JWT token

### Job Endpoints
- `GET /api/jobs/jobs/` - List all jobs
- `POST /api/jobs/jobs/` - Create job (recruiters only)
- `GET /api/jobs/jobs/{id}/` - Get job details
- `POST /api/jobs/jobs/{id}/apply/` - Apply for job

### AI Assistant Endpoints
- `POST /api/ai/analyze-resume/` - Analyze resume
- `POST /api/ai/match-jobs/` - Match jobs to resume
- `POST /api/ai/screen-candidate/` - Screen candidate

## Features in Detail

### Authentication & Authorization
- Role-based access control (Candidate, Recruiter, Admin)
- JWT token authentication with refresh mechanism
- Protected routes with permission guards

### Job Management
- Full CRUD operations for job listings
- Advanced filtering (job type, location, salary range)
- Job status management (published/draft)
- Application tracking with status updates

### AI Integration
- Resume text extraction from PDF files
- Intelligent job matching algorithms
- Automated candidate screening
- Detailed analysis with actionable insights

### Interview System
- Interview scheduling with calendar integration
- Multiple interview types (video, phone, in-person)
- Email notifications for scheduled interviews
- Interview status tracking

## Development

### Code Style
- Backend: Follow PEP 8 Python style guide
- Frontend: ESLint configuration for Vue 3
- Use meaningful variable and function names
- Comment complex logic

### Testing
```bash
# Backend tests
python manage.py test

# Frontend tests
npm run test
```

## Deployment

### Production Checklist
- [ ] Generate new SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up PostgreSQL database
- [ ] Configure static files serving
- [ ] Set up SSL certificate
- [ ] Configure environment variables on hosting platform

### Recommended Platforms
- **Backend:** PythonAnywhere, Render, Railway
- **Frontend:** Vercel, Netlify, Cloudflare Pages
- **Database:** PostgreSQL on Render, Supabase, or hosting provider

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

**Sneha Choudhary**
- GitHub: [@snehachaudhary05](https://github.com/snehachaudhary05)
- Project Link: [https://github.com/snehachaudhary05/talentbridge-ai](https://github.com/snehachaudhary05/talentbridge-ai)

## Acknowledgments

- OpenRouter for providing free AI model access
- Django & Vue communities for excellent documentation
- All contributors and testers

---

Built with ❤️ by Sneha Choudhary
