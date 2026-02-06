"""
Mock AI Client - Free implementation for testing without API keys
Provides realistic sample responses for all AI features
"""
import time
import json
import random
from typing import List, Dict, Optional


class MockAIClient:
    """
    Mock AI client that simulates AI responses without requiring API keys
    Perfect for development, testing, and demos
    """

    def __init__(self):
        self.model = "mock-ai-v1"

    def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> Dict:
        """
        Generate mock AI response based on the last user message
        """
        start_time = time.time()

        # Get the last user message
        user_message = ""
        for msg in reversed(messages):
            if msg.get('role') == 'user':
                user_message = msg.get('content', '').lower()
                break

        # Determine response type based on system prompt and user message
        response_content = self._generate_contextual_response(
            user_message, system_prompt
        )

        # Simulate token usage
        input_tokens = sum(len(m.get('content', '').split()) for m in messages) * 1.3
        output_tokens = len(response_content.split()) * 1.3

        response_time_ms = int((time.time() - start_time) * 1000)

        return {
            'content': response_content,
            'usage': {
                'input_tokens': int(input_tokens),
                'output_tokens': int(output_tokens)
            },
            'model': self.model,
            'stop_reason': 'end_turn',
            'response_time_ms': response_time_ms,
            'success': True
        }

    def _generate_contextual_response(
        self, user_message: str, system_prompt: Optional[str]
    ) -> str:
        """Generate contextually appropriate response"""

        # Resume analysis
        if 'resume' in user_message or 'cv' in user_message:
            if 'feedback' in user_message or 'improve' in user_message:
                return self._mock_resume_feedback()
            elif 'analyze' in user_message or 'extract' in user_message:
                return self._mock_resume_analysis()

        # Job matching
        if 'job' in user_message and ('match' in user_message or 'suggest' in user_message):
            return self._mock_job_match()

        # Skills
        if 'skill' in user_message:
            if 'recommend' in user_message or 'learn' in user_message:
                return self._mock_skill_recommendations()
            else:
                return self._mock_skill_extraction()

        # Job description
        if 'job description' in user_message or 'job posting' in user_message:
            return self._mock_job_description()

        # Interview questions
        if 'interview' in user_message and 'question' in user_message:
            return self._mock_interview_questions()

        # Candidate ranking/summary
        if 'candidate' in user_message:
            if 'rank' in user_message:
                return self._mock_candidate_ranking()
            elif 'summary' in user_message or 'summarize' in user_message:
                return self._mock_candidate_summary()

        # Analytics/Admin
        if 'analytics' in user_message or 'statistics' in user_message:
            return self._mock_analytics_summary()

        if 'spam' in user_message:
            return self._mock_spam_detection()

        if 'trend' in user_message or 'analysis' in user_message:
            return self._mock_trend_analysis()

        # Default conversational response
        return self._mock_general_response(user_message)

    def _mock_resume_analysis(self) -> str:
        """Mock resume analysis response"""
        return json.dumps({
            "skills": [
                "Python", "Django", "React", "PostgreSQL", "Docker",
                "REST APIs", "Git", "AWS", "Problem Solving", "Team Leadership"
            ],
            "experience_years": random.choice([3, 5, 7, 10]),
            "education": "Bachelor's Degree in Computer Science",
            "strengths": [
                "Strong full-stack development experience",
                "Proven track record of delivering scalable applications",
                "Excellent problem-solving abilities",
                "Experience with modern cloud technologies"
            ],
            "achievements": [
                "Led development of microservices architecture",
                "Reduced API response time by 40%",
                "Mentored junior developers"
            ],
            "areas_for_improvement": [
                "Add more quantifiable metrics to achievements",
                "Include specific project outcomes",
                "Highlight leadership experiences more prominently"
            ],
            "ats_score": random.randint(75, 95)
        }, indent=2)

    def _mock_resume_feedback(self) -> str:
        """Mock resume improvement feedback"""
        return """## Resume Improvement Recommendations

### Formatting (Score: 85/100)
- Use consistent bullet points throughout
- Ensure adequate white space between sections
- Consider using a more ATS-friendly font (Arial, Calibri)

### Content Optimization
1. **Add Quantifiable Achievements**
   - Instead of: "Improved application performance"
   - Better: "Improved application performance by 45%, reducing load time from 3s to 1.6s"

2. **Strengthen Action Verbs**
   - Replace weak verbs like "responsible for" with "spearheaded", "architected", "orchestrated"

3. **Keywords for ATS**
   - Add relevant technologies: cloud computing, CI/CD, agile methodologies
   - Include industry-standard certifications if applicable

### Sections to Enhance
- **Projects**: Add 2-3 key projects with tech stack and outcomes
- **Certifications**: List relevant certifications (AWS, Azure, etc.)
- **Summary**: Add a powerful 2-3 line professional summary at the top

### ATS Compatibility Score: 82/100
Your resume is largely ATS-friendly but could benefit from:
- Removing tables and complex formatting
- Using standard section headers
- Adding more industry keywords

### Next Steps
1. Quantify all major achievements
2. Add a skills matrix
3. Include relevant certifications
4. Proofread for typos and consistency
"""

    def _mock_skill_extraction(self) -> str:
        """Mock skill extraction"""
        return json.dumps([
            {"category": "Programming Languages", "skills": ["Python", "JavaScript", "Java"]},
            {"category": "Frameworks", "skills": ["Django", "React", "Node.js"]},
            {"category": "Databases", "skills": ["PostgreSQL", "MongoDB", "Redis"]},
            {"category": "DevOps", "skills": ["Docker", "Kubernetes", "AWS"]},
            {"category": "Tools", "skills": ["Git", "Jenkins", "Jira"]},
            {"category": "Soft Skills", "skills": ["Leadership", "Communication", "Problem Solving"]}
        ], indent=2)

    def _mock_job_match(self) -> str:
        """Mock job matching analysis"""
        match_score = random.randint(70, 95)
        return json.dumps({
            "match_score": match_score,
            "matching_skills": ["Python", "Django", "PostgreSQL", "REST APIs", "Docker"],
            "missing_skills": ["Kubernetes", "Redis", "GraphQL"],
            "recommendations": [
                "Strong match! Your Python and Django experience aligns perfectly with the requirements.",
                "Consider learning Kubernetes to strengthen your DevOps skills.",
                "Your experience with REST APIs is a key strength for this role.",
                "Adding GraphQL to your skillset would make you an even stronger candidate."
            ],
            "confidence": "high" if match_score > 80 else "medium"
        }, indent=2)

    def _mock_skill_recommendations(self) -> str:
        """Mock skill recommendations"""
        return json.dumps({
            "recommended_skills": [
                {
                    "skill": "Kubernetes",
                    "priority": "High",
                    "reason": "Essential for modern container orchestration and cloud deployments",
                    "timeline": "2-3 months",
                    "resources": ["Official Kubernetes docs", "KodeKloud courses"]
                },
                {
                    "skill": "GraphQL",
                    "priority": "Medium",
                    "reason": "Increasingly popular for API development, complements REST knowledge",
                    "timeline": "3-4 weeks",
                    "resources": ["GraphQL official tutorial", "Apollo documentation"]
                },
                {
                    "skill": "TypeScript",
                    "priority": "High",
                    "reason": "Industry standard for large-scale JavaScript applications",
                    "timeline": "4-6 weeks",
                    "resources": ["TypeScript Handbook", "Frontend Masters courses"]
                },
                {
                    "skill": "System Design",
                    "priority": "High",
                    "reason": "Critical for senior roles and technical interviews",
                    "timeline": "Ongoing",
                    "resources": ["Grokking System Design", "System Design Primer"]
                },
                {
                    "skill": "AWS Certifications",
                    "priority": "Medium",
                    "reason": "Validates cloud expertise and opens more opportunities",
                    "timeline": "2-3 months",
                    "resources": ["AWS Certified Solutions Architect course"]
                }
            ]
        }, indent=2)

    def _mock_job_description(self) -> str:
        """Mock job description generation"""
        return """# Senior Backend Engineer

## About the Role

We're seeking an experienced Senior Backend Engineer to join our growing engineering team. In this role, you'll architect and build scalable backend systems that power our platform, serving millions of users worldwide.

## Key Responsibilities

- Design and implement robust, scalable backend services using modern technologies
- Collaborate with cross-functional teams to define and ship new features
- Optimize application performance and ensure system reliability
- Mentor junior engineers and contribute to technical decisions
- Participate in code reviews and maintain high code quality standards
- Drive best practices for testing, deployment, and monitoring

## Required Qualifications

- 5+ years of professional software development experience
- Strong proficiency in Python and Django framework
- Deep understanding of RESTful API design and microservices architecture
- Experience with relational databases (PostgreSQL, MySQL)
- Solid understanding of software design patterns and principles
- Experience with cloud platforms (AWS, GCP, or Azure)
- Strong problem-solving skills and attention to detail

## Nice to Have

- Experience with containerization (Docker, Kubernetes)
- Knowledge of message queues (RabbitMQ, Kafka)
- Familiarity with CI/CD pipelines
- Open source contributions
- Experience with distributed systems

## What We Offer

- Competitive salary and equity package
- Flexible remote work options
- Professional development budget
- Health, dental, and vision insurance
- Collaborative and innovative work environment

## About Us

We're a fast-growing tech company revolutionizing the job search industry with AI-powered solutions. Join us in building the future of work!

**Equal Opportunity Employer**: We celebrate diversity and are committed to creating an inclusive environment for all employees.
"""

    def _mock_interview_questions(self) -> str:
        """Mock interview questions"""
        return json.dumps({
            "technical_questions": [
                {
                    "question": "Explain the difference between REST and GraphQL. When would you use each?",
                    "what_to_look_for": "Understanding of API paradigms, ability to evaluate trade-offs"
                },
                {
                    "question": "How would you design a rate limiting system for our API?",
                    "what_to_look_for": "System design skills, understanding of distributed systems"
                },
                {
                    "question": "Walk me through how you would optimize a slow database query.",
                    "what_to_look_for": "Database optimization knowledge, systematic problem-solving approach"
                }
            ],
            "behavioral_questions": [
                {
                    "question": "Tell me about a time when you had to make a difficult technical decision with limited information.",
                    "what_to_look_for": "Decision-making process, handling ambiguity"
                },
                {
                    "question": "Describe a situation where you mentored a junior developer. What was the outcome?",
                    "what_to_look_for": "Leadership skills, patience, communication ability"
                }
            ],
            "situational_questions": [
                {
                    "question": "If you discovered a critical security vulnerability in production, how would you handle it?",
                    "what_to_look_for": "Priority assessment, incident response, communication skills"
                }
            ]
        }, indent=2)

    def _mock_candidate_ranking(self) -> str:
        """Mock candidate ranking"""
        return "Candidates have been ranked based on skill match scores. See the ranked_candidates response."

    def _mock_candidate_summary(self) -> str:
        """Mock candidate summary"""
        return """## Candidate Profile Summary

**Key Strengths:**
- 7 years of backend development experience with Python and Django
- Strong track record of building scalable systems at high-growth companies
- Technical leadership experience managing teams of 3-5 engineers
- Excellent problem-solving skills with focus on system optimization

**Relevant Experience:**
- Led migration of monolithic application to microservices architecture
- Reduced API latency by 60% through caching and query optimization
- Implemented CI/CD pipeline that reduced deployment time by 75%

**Notable Achievements:**
- Architected payment processing system handling $10M+ in transactions
- Open source contributor to popular Django packages
- Speaker at regional tech conferences

**Technical Fit:**
- Matches 90% of required skills
- Strong alignment with company's tech stack
- Experience with similar scale and complexity

**Recommendation:** Strong candidate for senior backend role. Proceed to technical interview.
"""

    def _mock_analytics_summary(self) -> str:
        """Mock analytics summary"""
        return """## Platform Analytics Summary

### User Growth
- Total users: 1,250 (+12% MoM)
- New signups this month: 85
- Active users: 890 (71% engagement rate)

### Job Market Activity
- Total jobs posted: 450 (+8% MoM)
- Published jobs: 320
- Average applications per job: 7.1

### Application Trends
- Total applications: 3,200
- Success rate (interviews): 18%
- Average time to first response: 3.2 days

### Key Insights
1. Tech sector shows highest growth (35% of all jobs)
2. Remote positions receive 2.3x more applications
3. Peak activity: Tuesday-Thursday, 10am-2pm
4. Mobile usage increased 15% this quarter

### Recommendations
- Focus marketing on tech sector
- Promote remote opportunities more prominently
- Optimize for mobile experience
- Consider expanding to new geographic markets
"""

    def _mock_spam_detection(self) -> str:
        """Mock spam detection"""
        is_spam = random.choice([True, False])
        return json.dumps({
            "is_spam": is_spam,
            "confidence": random.randint(75, 98),
            "red_flags": [
                "Unusual posting pattern detected",
                "Generic company description",
                "Suspicious salary range"
            ] if is_spam else [],
            "recommended_action": "block" if is_spam else "approve",
            "reasoning": "Content matches known spam patterns" if is_spam else "Content appears legitimate"
        }, indent=2)

    def _mock_trend_analysis(self) -> str:
        """Mock trend analysis"""
        return """## Platform Trend Analysis (Last 30 Days)

### Growth Patterns
- User acquisition rate: +12% MoM (healthy growth)
- Job posting frequency: Steady increase, peaking mid-week
- Application volume: +8% compared to previous period

### User Engagement
- Average session duration: 8.5 minutes (up from 7.2 minutes)
- Return user rate: 65% (strong retention)
- Feature adoption: AI resume analysis most popular (78% of candidates)

### Job Categories
Top performing categories:
1. Software Engineering (35%)
2. Data Science (18%)
3. Product Management (12%)
4. Design (10%)
5. Marketing (8%)

### Geographic Trends
- Strongest markets: San Francisco, New York, Austin
- Emerging markets: Remote positions (global)
- Remote jobs: 45% of total postings (up from 32%)

### Issues Identified
- Slight increase in spam job postings (2.3% vs 1.8% baseline)
- Mobile application completion rate lower than desktop (68% vs 89%)
- Response time from recruiters increased slightly (3.2 days vs 2.8 days)

### Recommendations
1. Implement enhanced spam detection for job postings
2. Optimize mobile application flow to improve completion rate
3. Send reminder notifications to recruiters for pending applications
4. Consider adding AI-powered job matching to increase application quality
5. Expand marketing in emerging remote-first markets
"""

    def _mock_general_response(self, user_message: str) -> str:
        """Mock general conversational response"""
        responses = [
            "I understand your question. Based on the information provided, I can help you with that.",
            "That's a great question! Let me provide some insights based on current best practices.",
            "I'd be happy to help you with that. Here's what I recommend based on industry standards.",
            "Based on my analysis, here are some suggestions that might help.",
        ]
        return random.choice(responses) + "\n\n" + \
               "This is a mock AI response for testing purposes. " + \
               "The system is working correctly and will provide real AI responses when configured with an API key."

    def analyze_text(
        self,
        text: str,
        analysis_type: str,
        context: Optional[Dict] = None
    ) -> str:
        """Analyze text with specific instructions"""
        messages = [{"role": "user", "content": text}]
        response = self.generate_response(messages)
        return response.get('content', '')


# Singleton instance
_mock_ai_client_instance = None


def get_mock_ai_client() -> MockAIClient:
    """Get or create mock AI client instance"""
    global _mock_ai_client_instance
    if _mock_ai_client_instance is None:
        _mock_ai_client_instance = MockAIClient()
    return _mock_ai_client_instance
