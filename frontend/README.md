# Job Portal Frontend - Vue.js

Beautiful, modern frontend for the AI-powered job portal built with Vue 3 + Vite + Tailwind CSS.

## Features

- Modern, responsive UI with Tailwind CSS
- Vue 3 Composition API
- Pinia for state management
- Vue Router for navigation
- Axios for API calls
- JWT authentication
- Role-based dashboards (Candidate, Recruiter, Admin)
- AI-powered features integration

## Pages Included

- **Home**: Beautiful landing page with hero section
- **Login**: User authentication
- **Register**: Account creation with role selection
- **Jobs**: Browse and filter job listings
- **Job Details**: View individual job information
- **Dashboard**: Personalized dashboard based on role
- **AI Assistant**: Resume analysis, job matching, skill recommendations
- **Profile**: User settings and account management

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The frontend will be available at: **http://localhost:5173/**

### 3. Build for Production

```bash
npm run build
```

### 4. Preview Production Build

```bash
npm run preview
```

## API Configuration

The frontend is configured to proxy API requests to the backend:
- Backend URL: `http://127.0.0.1:8000`
- API Prefix: `/api`

All API calls (e.g., `/api/jobs/jobs/`) are automatically proxied to the backend.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Navbar.vue           # Navigation bar
│   │   └── Footer.vue           # Footer component
│   ├── views/
│   │   ├── Home.vue             # Landing page
│   │   ├── Login.vue            # Login page
│   │   ├── Register.vue         # Registration page
│   │   ├── Jobs.vue             # Job listings
│   │   ├── JobDetails.vue       # Job details
│   │   ├── Dashboard.vue        # User dashboard
│   │   ├── AIAssistant.vue      # AI features
│   │   └── Profile.vue          # User profile
│   ├── stores/
│   │   └── auth.js              # Authentication store
│   ├── router/
│   │   └── index.js             # Route definitions
│   ├── App.vue                  # Root component
│   ├── main.js                  # App entry point
│   └── style.css                # Global styles
├── index.html                    # HTML template
├── package.json                  # Dependencies
├── vite.config.js               # Vite configuration
└── tailwind.config.js           # Tailwind configuration
```

## Features by Role

### For Candidates

- Browse published jobs
- AI resume analysis
- Job matching based on skills
- Skill recommendations
- Application tracking
- Profile management

### For Recruiters

- Post and manage jobs
- View applications
- AI candidate ranking
- Interview question generation
- Resume summarization

### For Admins

- Platform analytics
- User management
- Spam detection
- Trend analysis

## Styling

The app uses Tailwind CSS with a custom color scheme:

- **Primary Color**: Blue (customizable in tailwind.config.js)
- **Font**: Inter (Google Fonts)
- **Components**: Pre-styled buttons, cards, badges, input fields

### Custom CSS Classes

- `.btn-primary` - Primary action button
- `.btn-secondary` - Secondary button
- `.btn-outline` - Outlined button
- `.input-field` - Styled input field
- `.card` - Card container
- `.badge` - Badge/tag component

## Environment Variables

Create a `.env` file if you need to customize:

```bash
VITE_API_URL=http://localhost:8000
```

## Authentication

The app uses JWT token authentication:
- Tokens stored in localStorage
- Automatic token refresh
- Protected routes with navigation guards
- Role-based access control

## API Integration

All API calls use Axios with automatic authentication:

```javascript
import axios from 'axios'

// API call example
const response = await axios.get('/api/jobs/jobs/')
```

## Tips & Tricks

1. **Hot Module Replacement**: Changes are reflected instantly
2. **Vue Devtools**: Install for better debugging
3. **Tailwind IntelliSense**: Install VS Code extension for autocomplete
4. **API Proxy**: No CORS issues - requests proxied to backend

## Troubleshooting

### Port Already in Use
If port 5173 is taken, Vite will automatically use the next available port.

### API Connection Issues
Ensure the backend is running at `http://127.0.0.1:8000/`

### Authentication Errors
Clear localStorage and login again:
```javascript
localStorage.clear()
```

## Next Steps

1. Customize colors in `tailwind.config.js`
2. Add more features to views
3. Enhance AI assistant UI
4. Add real-time notifications
5. Implement file upload for resumes
6. Add chat functionality

## Production Deployment

### Using Vercel
```bash
npm run build
vercel --prod
```

### Using Netlify
```bash
npm run build
# Deploy the dist/ folder
```

### Using Static Hosting
```bash
npm run build
# Upload dist/ folder to your hosting
```

## License

MIT License

## Support

The frontend connects seamlessly with the Django backend's FREE Mock AI - no API keys needed!

Enjoy your beautiful job portal! 🚀
