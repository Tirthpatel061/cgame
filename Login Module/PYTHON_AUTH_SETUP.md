## Python Auth + OTP Setup

### 1) Install dependencies
```
pip install -r "Login Module/requirements.txt"
```

### 2) Create environment file
- Copy `Login Module/.env.example` to `Login Module/.env`
- Update MySQL and SMTP values

### 2.1) Gmail SMTP example
- Use an **App Password** (not your normal Gmail password).
- Set:
  - `SMTP_HOST=smtp.gmail.com`
  - `SMTP_PORT=587`
  - `SMTP_STARTTLS=true`
  - `SMTP_USE_SSL=false`

### 3) Create/Update database tables
- Run `Login Module/database_setup.sql` in MySQL (phpMyAdmin or CLI)
- If you already had `email_otps` without a `purpose` column, the auth server will try to add it on startup; otherwise run: `ALTER TABLE email_otps ADD COLUMN purpose VARCHAR(20) NOT NULL DEFAULT 'signup';`

### 4) Start the auth server
```
python "Login Module/auth_server.py"
```

### 5) Use the login page
- Open `Login Module/login.html`
- Signup triggers OTP flow and email verification
- **Forgot password**: use "Forgot password?" on the login form; OTP is sent to the user’s email, then they set a new password (stored in the database).

### Notes
- If SMTP is not configured, the server returns a `dev_otp` in the response (only for local testing).
- `user_store.json` mirrors verified users and is synced into MySQL on server start.
