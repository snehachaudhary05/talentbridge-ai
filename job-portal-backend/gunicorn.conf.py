# Gunicorn configuration file
import multiprocessing

# Bind to the port provided by Render
bind = "0.0.0.0:10000"

# Worker configuration
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"

# Timeout configuration - IMPORTANT for AI API calls
# Default is 30s, but AI responses can take 60-90s
timeout = 120  # 2 minutes for AI processing
graceful_timeout = 30
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "talentbridge-backend"

# Connection settings
max_requests = 1000
max_requests_jitter = 50

# Worker timeout (for debugging)
worker_tmp_dir = "/dev/shm"  # Use RAM for worker heartbeat files
