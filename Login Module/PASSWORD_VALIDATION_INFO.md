# Password Validation & Username Policy

## Password Requirements

All new user passwords must meet the following criteria:

1. **Minimum Length**: At least 8 characters
2. **Uppercase Letter**: At least one uppercase letter (A-Z)
3. **Lowercase Letter**: At least one lowercase letter (a-z)
4. **Digit**: At least one number (0-9)
5. **Special Character**: At least one special character (!@#$%^&*()_+-=[]{}; ':"\\|,.<>/?)

### Example Valid Passwords:
- `Password123!`
- `MyP@ssw0rd`
- `Secure#2024`

### Example Invalid Passwords:
- `password` (no uppercase, no digit, no special char)
- `PASSWORD123` (no lowercase, no special char)
- `Pass123` (less than 8 characters, no special char)
- `Password!` (no digit)

## Username Policy

- **Usernames can be duplicated** across different accounts
- Multiple users can have the same username (e.g., "shubham")
- **Emails must be unique** - each email can only be registered once
- Users are identified by their unique email address, not username

### Example:
✅ User 1: username="shubham", email="shubham1@gmail.com"
✅ User 2: username="shubham", email="shubham2@gmail.com"
❌ User 3: username="john", email="shubham1@gmail.com" (email already exists)

## Validation Locations

1. **Frontend (login.js)**: Client-side validation for immediate feedback
2. **Backend (auth_server.py)**: Server-side validation for security

Both validations are enforced to ensure data integrity.
