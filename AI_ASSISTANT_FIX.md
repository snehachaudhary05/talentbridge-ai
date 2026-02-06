# AI Assistant Authentication Fix

## Issues Found and Fixed

### Problem
The AI Assistant features for both candidates and recruiters were giving 401 Unauthorized errors intermittently. When one role worked, the other didn't, creating an inconsistent experience.

### Root Causes Identified

1. **Missing Axios Interceptor**
   - The Authorization header wasn't consistently included in all API requests
   - Some requests were being sent without the JWT token

2. **Redundant Permission Classes**
   - Backend views had both `IsAuthenticated` and role-specific permissions (e.g., `IsRecruiter`)
   - The role-specific permissions already check for authentication, making the redundancy potentially problematic

### Fixes Applied

#### 1. Frontend Fix ([main.js](frontend/src/main.js))
Added axios interceptors to ensure the Authorization header is ALWAYS included:

```javascript
// Add axios interceptor to ensure Authorization header is always included
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add axios response interceptor to handle 401 errors
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.error('Authentication error - token might be invalid or expired')
      console.error('Error details:', error.response?.data)
    }
    return Promise.reject(error)
  }
)
```

#### 2. Backend Fix ([ai_assistant/views.py](job-portal-backend/ai_assistant/views.py))
Simplified permission classes by removing redundant `IsAuthenticated`:

**Before:**
```python
permission_classes = [IsAuthenticated, IsCandidate]
permission_classes = [IsAuthenticated, IsRecruiter]
permission_classes = [IsAuthenticated, IsAdmin]
```

**After:**
```python
permission_classes = [IsCandidate]
permission_classes = [IsRecruiter]
permission_classes = [IsAdmin]
```

Since `IsCandidate`, `IsRecruiter`, and `IsAdmin` already check for authentication, the redundant `IsAuthenticated` was removed.

## Testing the Fix

### For Candidates:
1. Log in as a candidate
2. Go to AI Assistant page
3. Try these features:
   - **Resume Analysis**: Upload or paste your resume
   - **Job Matching**: Enter your skills (e.g., "Python, Django, React")
   - **Skill Recommendations**: Enter current skills and target role

### For Recruiters:
1. Log in as a recruiter
2. Go to AI Assistant page
3. Try these features:
   - **Generate Job Description**: Enter job title, company, skills, experience
   - **Screen Candidates**: Upload candidate resume with job requirements
   - **Interview Questions**: Enter role and skills to test

### Expected Behavior:
- ✅ All features should work without 401 errors
- ✅ Switching between different AI features should work consistently
- ✅ Both candidate and recruiter features should work independently

## If You Still See Errors

### Check These:
1. **Clear browser cache and localStorage**:
   - Open browser DevTools (F12)
   - Go to Application/Storage tab
   - Clear localStorage
   - Refresh the page and log in again

2. **Check browser console for errors**:
   - Open DevTools (F12)
   - Go to Console tab
   - Look for any red errors
   - Check the Network tab for failed requests

3. **Verify you're logged in**:
   - Check that you see the navbar with your role
   - Try logging out and logging back in

4. **Check backend logs**:
   - Look at the terminal running the Django server
   - Check for any error messages or stack traces

## Architecture Overview

### Authentication Flow:
1. User logs in → JWT token stored in localStorage
2. Axios interceptor adds token to every request automatically
3. Backend validates token and checks user role
4. Role-specific permissions grant or deny access

### Permission Hierarchy:
- `IsCandidate` → Checks: authenticated + role == 'candidate'
- `IsRecruiter` → Checks: authenticated + role == 'recruiter'
- `IsAdmin` → Checks: authenticated + role == 'admin'

## Troubleshooting Commands

```bash
# Check if user is properly authenticated in Django
cd job-portal-backend
python show_users.py

# Test API endpoint directly
curl -X POST http://localhost:8000/api/ai/candidate/suggest_jobs/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"skills": ["Python", "Django"], "limit": 5}'
```

## Additional Notes

- The system uses **mock AI** by default (no API keys required)
- All AI features work with simulated responses
- The frontend automatically proxies `/api` requests to `http://localhost:8000`
- JWT tokens are stored in localStorage and automatically refreshed
