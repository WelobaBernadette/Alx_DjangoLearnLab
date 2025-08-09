# ----------------------------
# 🔒 HTTPS & Security Settings
# ----------------------------

# Redirect all HTTP traffic to HTTPS
SECURE_SSL_REDIRECT = True  # Enforces HTTPS by redirecting all HTTP requests

# Enable HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Applies HSTS to all subdomains
SECURE_HSTS_PRELOAD = True  # Enables preload option for browser HSTS preload lists

# Secure cookies
SESSION_COOKIE_SECURE = True  # Ensures session cookies are only sent over HTTPS
CSRF_COOKIE_SECURE = True  # Ensures CSRF cookies are only sent over HTTPS

# Prevent MIME-sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevents the browser from guessing content types

# XSS Protection
SECURE_BROWSER_XSS_FILTER = True  # Enables basic browser XSS protection

# Clickjacking protection
X_FRAME_OPTIONS = "DENY"  # Prevents your site from being embedded in frames

# Additional Optional Headers
# SECURE_REFERRER_POLICY = "strict-origin"  # Optional: helps protect referrer data
