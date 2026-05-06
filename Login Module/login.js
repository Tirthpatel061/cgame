// ============================================
// Among Us Auth UI Logic with PHP Backend
// ============================================

// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
    // --------------------------------------------
    // Get references to all key elements
    // --------------------------------------------
    const loginTab = document.getElementById("loginTab");
    const signupTab = document.getElementById("signupTab");

    const loginForm = document.getElementById("loginForm");
    const signupForm = document.getElementById("signupForm");

    const toSignupLink = document.getElementById("toSignupLink");
    const toLoginLink = document.getElementById("toLoginLink");

    const statusMessage = document.getElementById("statusMessage");
    const signupSubmitBtn = document.getElementById("signupSubmitBtn");
    const otpSection = document.getElementById("otpSection");
    const verifyOtpBtn = document.getElementById("verifyOtpBtn");
    const resendOtpBtn = document.getElementById("resendOtpBtn");
    const otpInput = document.getElementById("signup-otp");

    const forgotPasswordLink = document.getElementById("forgotPasswordLink");
    const forgotBackToLogin = document.getElementById("forgotBackToLogin");
    const forgotPasswordSection = document.getElementById("forgotPasswordSection");
    const forgotStep1 = document.getElementById("forgotStep1");
    const forgotStep2 = document.getElementById("forgotStep2");
    const forgotEmailInput = document.getElementById("forgot-email");
    const forgotOtpInput = document.getElementById("forgot-otp");
    const forgotNewPasswordInput = document.getElementById("forgot-new-password");
    const forgotConfirmPasswordInput = document.getElementById("forgot-confirm-password");
    const forgotSendOtpBtn = document.getElementById("forgotSendOtpBtn");
    const forgotResetBtn = document.getElementById("forgotResetBtn");
    const forgotResendOtpBtn = document.getElementById("forgotResendOtpBtn");

    const AUTH_API_BASE = window.AUTH_API_BASE || "http://localhost:5002";
    let pendingSignup = null;
    let forgotPasswordEmail = null;

    // Password requirements validation elements
    const passwordInput = document.getElementById("signup-password");
    const reqLength = document.getElementById("req-length");
    const reqUppercase = document.getElementById("req-uppercase");
    const reqLowercase = document.getElementById("req-lowercase");
    const reqDigit = document.getElementById("req-digit");
    const reqSpecial = document.getElementById("req-special");

    // Real-time password validation
    if (passwordInput) {
        passwordInput.addEventListener("input", function() {
            const password = passwordInput.value;
            
            // Check length
            if (password.length >= 8) {
                reqLength.classList.add("valid");
                reqLength.classList.remove("invalid");
            } else {
                reqLength.classList.add("invalid");
                reqLength.classList.remove("valid");
            }
            
            // Check uppercase
            if (/[A-Z]/.test(password)) {
                reqUppercase.classList.add("valid");
                reqUppercase.classList.remove("invalid");
            } else {
                reqUppercase.classList.add("invalid");
                reqUppercase.classList.remove("valid");
            }
            
            // Check lowercase
            if (/[a-z]/.test(password)) {
                reqLowercase.classList.add("valid");
                reqLowercase.classList.remove("invalid");
            } else {
                reqLowercase.classList.add("invalid");
                reqLowercase.classList.remove("valid");
            }
            
            // Check digit
            if (/[0-9]/.test(password)) {
                reqDigit.classList.add("valid");
                reqDigit.classList.remove("invalid");
            } else {
                reqDigit.classList.add("invalid");
                reqDigit.classList.remove("valid");
            }
            
            // Check special character
            if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
                reqSpecial.classList.add("valid");
                reqSpecial.classList.remove("invalid");
            } else {
                reqSpecial.classList.add("invalid");
                reqSpecial.classList.remove("valid");
            }
        });
    }

    // Small helper: show a status message with a type (success or error)
    function showStatus(message, type) {
        statusMessage.textContent = message;
        statusMessage.classList.remove("success", "error");
        if (type) {
            statusMessage.classList.add(type);
        }
    }

    // Small helper: clear existing status
    function clearStatus() {
        showStatus("", null);
    }

    function setSignupLocked(isLocked) {
        if (!signupSubmitBtn) return;
        signupSubmitBtn.disabled = isLocked;
        signupSubmitBtn.setAttribute("aria-disabled", isLocked ? "true" : "false");
    }

    function toggleOtpSection(show) {
        if (!otpSection) return;
        otpSection.classList.toggle("active", show);
    }

    // --------------------------------------------
    // Tab & Form Switching
    // --------------------------------------------
    function activateLogin() {
        loginTab.classList.add("active");
        signupTab.classList.remove("active");

        loginForm.classList.add("active-form");
        signupForm.classList.remove("active-form");
        if (forgotPasswordSection) forgotPasswordSection.style.display = "none";

        // Clear previous messages
        clearStatus();
        toggleOtpSection(false);
        setSignupLocked(false);
        pendingSignup = null;
        if (otpInput) {
            otpInput.value = "";
        }
    }

    function activateSignup() {
        signupTab.classList.add("active");
        loginTab.classList.remove("active");

        signupForm.classList.add("active-form");
        loginForm.classList.remove("active-form");
        if (forgotPasswordSection) forgotPasswordSection.style.display = "none";

        // Clear previous messages
        clearStatus();
        toggleOtpSection(false);
        setSignupLocked(false);
        pendingSignup = null;
        if (otpInput) {
            otpInput.value = "";
        }
    }

    // When user clicks the Login tab
    loginTab.addEventListener("click", activateLogin);

    // When user clicks the Sign Up tab
    signupTab.addEventListener("click", activateSignup);

    // When user clicks "New crewmate? Sign Up"
    toSignupLink.addEventListener("click", activateSignup);

    // When user clicks "Already a crewmate? Login"
    toLoginLink.addEventListener("click", activateLogin);

    // --------------------------------------------
    // FORGOT PASSWORD
    // --------------------------------------------
    function showForgotPassword() {
        loginForm.classList.remove("active-form");
        signupForm.classList.remove("active-form");
        loginTab.classList.remove("active");
        signupTab.classList.remove("active");
        if (forgotPasswordSection) forgotPasswordSection.style.display = "block";
        forgotStep1.style.display = "block";
        forgotStep2.style.display = "none";
        forgotPasswordEmail = null;
        clearStatus();
        if (forgotEmailInput) forgotEmailInput.value = "";
        if (forgotOtpInput) forgotOtpInput.value = "";
        if (forgotNewPasswordInput) forgotNewPasswordInput.value = "";
        if (forgotConfirmPasswordInput) forgotConfirmPasswordInput.value = "";
    }

    function hideForgotPassword() {
        if (forgotPasswordSection) forgotPasswordSection.style.display = "none";
        loginForm.classList.add("active-form");
        loginTab.classList.add("active");
        clearStatus();
    }

    if (forgotPasswordLink) forgotPasswordLink.addEventListener("click", showForgotPassword);
    if (forgotBackToLogin) forgotBackToLogin.addEventListener("click", hideForgotPassword);

    if (forgotSendOtpBtn) {
        forgotSendOtpBtn.addEventListener("click", function () {
            clearStatus();
            const email = forgotEmailInput ? forgotEmailInput.value.trim() : "";
            if (!email) {
                showStatus("Please enter your email.", "error");
                return;
            }
            showStatus("Sending OTP to your email...", "info");
            fetch(`${AUTH_API_BASE}/auth/forgot-password`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: email })
            })
                .then(function (res) { return res.json(); })
                .then(function (data) {
                    if (data.success) {
                        forgotPasswordEmail = email;
                        forgotStep1.style.display = "none";
                        forgotStep2.style.display = "block";
                        if (forgotOtpInput) { forgotOtpInput.value = ""; forgotOtpInput.focus(); }
                        var msg = data.message || "Check your email for the code.";
                        if (data.dev_otp) msg += " Dev OTP: " + data.dev_otp;
                        showStatus(msg, data.dev_otp ? "info" : "success");
                    } else {
                        showStatus(data.message || "Failed to send OTP.", "error");
                    }
                })
                .catch(function (err) {
                    console.error("Forgot password error:", err);
                    showStatus("Connection error. Please try again.", "error");
                });
        });
    }

    if (forgotResetBtn) {
        forgotResetBtn.addEventListener("click", function () {
            clearStatus();
            var email = forgotPasswordEmail || (forgotEmailInput && forgotEmailInput.value.trim());
            var otp = forgotOtpInput ? forgotOtpInput.value.trim() : "";
            var newPassword = forgotNewPasswordInput ? forgotNewPasswordInput.value : "";
            var confirmPassword = forgotConfirmPasswordInput ? forgotConfirmPasswordInput.value : "";
            if (!email || !otp) {
                showStatus("Please enter the code from your email.", "error");
                return;
            }
            if (!newPassword) {
                showStatus("Please enter a new password.", "error");
                return;
            }
            if (newPassword !== confirmPassword) {
                showStatus("Passwords do not match.", "error");
                return;
            }
            var pwdErr = validatePassword(newPassword);
            if (pwdErr) {
                showStatus(pwdErr, "error");
                return;
            }
            showStatus("Updating password...", "info");
            fetch(`${AUTH_API_BASE}/auth/reset-password`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: email, otp: otp, newPassword: newPassword })
            })
                .then(function (res) { return res.json(); })
                .then(function (data) {
                    if (data.success) {
                        showStatus("Password updated! Please log in.", "success");
                        setTimeout(function () {
                            hideForgotPassword();
                            if (document.getElementById("login-identifier")) document.getElementById("login-identifier").value = email;
                        }, 1500);
                    } else {
                        showStatus(data.message || "Failed to reset password.", "error");
                    }
                })
                .catch(function (err) {
                    console.error("Reset password error:", err);
                    showStatus("Connection error. Please try again.", "error");
                });
        });
    }

    if (forgotResendOtpBtn) {
        forgotResendOtpBtn.addEventListener("click", function () {
            clearStatus();
            var email = forgotPasswordEmail || (forgotEmailInput && forgotEmailInput.value.trim());
            if (!email) {
                showStatus("Please enter your email in step 1 first.", "error");
                return;
            }
            showStatus("Resending OTP...", "info");
            fetch(`${AUTH_API_BASE}/auth/forgot-password`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: email })
            })
                .then(function (res) { return res.json(); })
                .then(function (data) {
                    if (data.success) {
                        var msg = data.message || "OTP sent.";
                        if (data.dev_otp) msg += " Dev OTP: " + data.dev_otp;
                        showStatus(msg, data.dev_otp ? "info" : "success");
                    } else {
                        showStatus(data.message || "Resend failed.", "error");
                    }
                })
                .catch(function (err) {
                    console.error("Resend OTP error:", err);
                    showStatus("Connection error. Please try again.", "error");
                });
        });
    }

    // --------------------------------------------
    // LOGIN VALIDATION WITH PHP BACKEND
    // --------------------------------------------
    loginForm.addEventListener("submit", function (event) {
        // Prevent actual form submission
        event.preventDefault();

        clearStatus();

        // Get form field values
        const identifier = document.getElementById("login-identifier").value.trim();
        const password = document.getElementById("login-password").value.trim();

        // Simple empty-field validation
        if (!identifier || !password) {
            showStatus("Impostor detected! All fields must be filled.", "error");
            return;
        }

        // Show loading message
        showStatus("Verifying crewmate credentials...", "info");

        // Send login request to PHP backend
        fetch(`${AUTH_API_BASE}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                identifier: identifier,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showStatus("Crewmate verified! Logging you into the ship...", "success");
                
                // Store user data in localStorage for the game
                localStorage.setItem('currentPlayer', data.user.username);
                localStorage.setItem('userId', data.user.id);
                localStorage.setItem('userEmail', data.user.email);
                
                // Redirect to map.html after successful login with loading animation
                setTimeout(function () {
                    window.location.href = '../Loading Page Animation/loading_page_animation.html?next=../kings-and-pigs-main/map.html?player=' + encodeURIComponent(data.user.username);
                }, 1500);
            } else {
                showStatus("Impostor detected! " + data.message, "error");
            }
        })
        .catch(error => {
            console.error('Login error:', error);
            showStatus("Connection error! Please try again.", "error");
        });
    });

    // --------------------------------------------
    // Password validation function
    // --------------------------------------------
    function validatePassword(password) {
        // At least 8 characters
        if (password.length < 8) {
            return "Password must be at least 8 characters long.";
        }
        // At least one uppercase letter
        if (!/[A-Z]/.test(password)) {
            return "Password must contain at least one uppercase letter.";
        }
        // At least one lowercase letter
        if (!/[a-z]/.test(password)) {
            return "Password must contain at least one lowercase letter.";
        }
        // At least one digit
        if (!/[0-9]/.test(password)) {
            return "Password must contain at least one digit.";
        }
        // At least one special character
        if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
            return "Password must contain at least one special character.";
        }
        return null; // Valid password
    }

    // --------------------------------------------
    // SIGN UP VALIDATION WITH PHP BACKEND
    // --------------------------------------------
    signupForm.addEventListener("submit", function (event) {
        event.preventDefault();

        clearStatus();

        // Get the field values
        const username = document.getElementById("signup-username").value.trim();
        const email = document.getElementById("signup-email").value.trim();
        const password = document.getElementById("signup-password").value.trim();
        const confirmPassword = document.getElementById("signup-confirm-password").value.trim();

        // Empty fields check
        if (!username || !email || !password || !confirmPassword) {
            showStatus("Impostor detected! Please complete all fields.", "error");
            return;
        }

        // Password strength validation
        const passwordError = validatePassword(password);
        if (passwordError) {
            showStatus(passwordError, "error");
            return;
        }

        // Password match check
        if (password !== confirmPassword) {
            showStatus("Impostor detected! Passwords do not match.", "error");
            return;
        }

        // Show loading message
        showStatus("Creating crewmate account...", "info");

        // Send OTP request to Python backend
        fetch(`${AUTH_API_BASE}/auth/request-otp`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const otpNote = data.dev_otp ? ` Dev OTP: ${data.dev_otp}` : "";
                const smtpNote = data.smtp_error ? " Email not sent. Please check SMTP settings." : "";
                showStatus(`OTP sent to your email.${smtpNote}${otpNote}`, data.dev_otp ? "info" : "success");
                pendingSignup = { username, email, password };
                toggleOtpSection(true);
                setSignupLocked(true);
                if (otpInput) {
                    otpInput.value = "";
                    otpInput.focus();
                }
            } else {
                showStatus("Registration failed! " + data.message, "error");
            }
        })
        .catch(error => {
            console.error('Signup error:', error);
            showStatus("Connection error! Please try again.", "error");
        });
    });

    if (verifyOtpBtn) {
        verifyOtpBtn.addEventListener("click", function () {
            clearStatus();

            if (!pendingSignup) {
                showStatus("Please request an OTP first.", "error");
                return;
            }

            const otp = otpInput ? otpInput.value.trim() : "";
            if (!otp) {
                showStatus("Please enter the OTP from your email.", "error");
                return;
            }

            showStatus("Verifying OTP...", "info");

            fetch(`${AUTH_API_BASE}/auth/verify-otp`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: pendingSignup.email,
                    otp: otp
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showStatus("Registration complete. Please log in with your account.", "success");
                    toggleOtpSection(false);
                    setSignupLocked(false);
                    pendingSignup = null;

                    const loginIdentifier = document.getElementById("login-identifier");
                    if (loginIdentifier && data.user && data.user.email) {
                        loginIdentifier.value = data.user.email;
                    }
                    activateLogin();
                } else {
                    showStatus("OTP verification failed! " + data.message, "error");
                    setSignupLocked(false);
                }
            })
            .catch(error => {
                console.error('OTP verify error:', error);
                showStatus("Connection error! Please try again.", "error");
                setSignupLocked(false);
            });
        });
    }

    if (resendOtpBtn) {
        resendOtpBtn.addEventListener("click", function () {
            clearStatus();
            const username = pendingSignup?.username || document.getElementById("signup-username").value.trim();
            const email = pendingSignup?.email || document.getElementById("signup-email").value.trim();
            const password = pendingSignup?.password || document.getElementById("signup-password").value.trim();

            if (!username || !email || !password) {
                showStatus("Please fill the signup form first.", "error");
                return;
            }

            showStatus("Resending OTP...", "info");

            fetch(`${AUTH_API_BASE}/auth/request-otp`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    email: email,
                    password: password
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const otpNote = data.dev_otp ? ` Dev OTP: ${data.dev_otp}` : "";
                    const smtpNote = data.smtp_error ? " Email not sent. Please check SMTP settings." : "";
                    showStatus(`OTP sent to your email.${smtpNote}${otpNote}`, data.dev_otp ? "info" : "success");
                    pendingSignup = { username, email, password };
                    toggleOtpSection(true);
                } else {
                    showStatus("OTP resend failed! " + data.message, "error");
                }
            })
            .catch(error => {
                console.error('Resend OTP error:', error);
                showStatus("Connection error! Please try again.", "error");
            });
        });
    }
});