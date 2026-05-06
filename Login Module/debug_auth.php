<?php
// Debug version of auth.php with detailed logging
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    exit(0);
}

// Enable error reporting for debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once 'config.php';

$response = array();
$debug = array();

// Log the request
$debug['request_method'] = $_SERVER['REQUEST_METHOD'];
$debug['timestamp'] = date('Y-m-d H:i:s');

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    $debug['raw_input'] = file_get_contents('php://input');
    $debug['parsed_input'] = $input;
    
    $action = $input['action'] ?? '';
    $debug['action'] = $action;
    
    switch ($action) {
        case 'login':
            $debug['flow'] = 'login';
            handleLogin($conn, $input, $debug);
            break;
        case 'signup':
            $debug['flow'] = 'signup';
            handleSignup($conn, $input, $debug);
            break;
        default:
            $response['success'] = false;
            $response['message'] = 'Invalid action';
            $debug['error'] = 'Invalid action: ' . $action;
            break;
    }
} else {
    $response['success'] = false;
    $response['message'] = 'Only POST method allowed';
    $debug['error'] = 'Wrong request method';
}

// Add debug info to response
$response['debug'] = $debug;

echo json_encode($response, JSON_PRETTY_PRINT);

function handleLogin($conn, $input, &$debug) {
    global $response;
    
    $identifier = trim($input['identifier'] ?? '');
    $password = $input['password'] ?? '';
    
    $debug['login_identifier'] = $identifier;
    $debug['password_length'] = strlen($password);
    
    if (empty($identifier) || empty($password)) {
        $response['success'] = false;
        $response['message'] = 'All fields are required';
        $debug['validation_error'] = 'Empty fields';
        return;
    }
    
    try {
        // Check if identifier is email or username
        $sql = "SELECT id, username, email, password FROM users WHERE email = ? OR username = ?";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("ss", $identifier, $identifier);
        $stmt->execute();
        $result = $stmt->get_result();
        
        $debug['query_executed'] = true;
        $debug['rows_found'] = $result->num_rows;
        
        if ($result->num_rows == 1) {
            $user = $result->fetch_assoc();
            $debug['user_found'] = $user['username'];
            
            if (password_verify($password, $user['password'])) {
                $debug['password_verified'] = true;
                
                // Update last login
                $updateSql = "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?";
                $updateStmt = $conn->prepare($updateSql);
                $updateStmt->bind_param("i", $user['id']);
                $updateStmt->execute();
                
                $response['success'] = true;
                $response['message'] = 'Login successful';
                $response['user'] = array(
                    'id' => $user['id'],
                    'username' => $user['username'],
                    'email' => $user['email']
                );
                $debug['login_success'] = true;
            } else {
                $response['success'] = false;
                $response['message'] = 'Invalid credentials';
                $debug['password_verified'] = false;
            }
        } else {
            $response['success'] = false;
            $response['message'] = 'User not found';
            $debug['user_found'] = false;
        }
        
        $stmt->close();
    } catch (Exception $e) {
        $response['success'] = false;
        $response['message'] = 'Database error: ' . $e->getMessage();
        $debug['database_error'] = $e->getMessage();
    }
}

function handleSignup($conn, $input, &$debug) {
    global $response;
    
    $username = trim($input['username'] ?? '');
    $email = trim($input['email'] ?? '');
    $password = $input['password'] ?? '';
    $confirmPassword = $input['confirmPassword'] ?? '';
    
    $debug['signup_data'] = array(
        'username' => $username,
        'email' => $email,
        'password_length' => strlen($password),
        'confirm_password_length' => strlen($confirmPassword)
    );
    
    // Validation
    if (empty($username) || empty($email) || empty($password) || empty($confirmPassword)) {
        $response['success'] = false;
        $response['message'] = 'All fields are required';
        $debug['validation_error'] = 'Empty fields';
        return;
    }
    
    if ($password !== $confirmPassword) {
        $response['success'] = false;
        $response['message'] = 'Passwords do not match';
        $debug['validation_error'] = 'Password mismatch';
        return;
    }
    
    if (strlen($password) < 6) {
        $response['success'] = false;
        $response['message'] = 'Password must be at least 6 characters long';
        $debug['validation_error'] = 'Password too short';
        return;
    }
    
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $response['success'] = false;
        $response['message'] = 'Invalid email format';
        $debug['validation_error'] = 'Invalid email';
        return;
    }
    
    $debug['validation_passed'] = true;
    
    try {
        // Check if email already exists
        $checkSql = "SELECT id FROM users WHERE email = ?";
        $checkStmt = $conn->prepare($checkSql);
        $checkStmt->bind_param("s", $email);
        $checkStmt->execute();
        $checkResult = $checkStmt->get_result();
        
        $debug['email_check_rows'] = $checkResult->num_rows;
        
        if ($checkResult->num_rows > 0) {
            $response['success'] = false;
            $response['message'] = 'Email already registered';
            $debug['duplicate_email'] = true;
            $checkStmt->close();
            return;
        }
        $checkStmt->close();
        
        // Check if username already exists
        $checkUserSql = "SELECT id FROM users WHERE username = ?";
        $checkUserStmt = $conn->prepare($checkUserSql);
        $checkUserStmt->bind_param("s", $username);
        $checkUserStmt->execute();
        $checkUserResult = $checkUserStmt->get_result();
        
        $debug['username_check_rows'] = $checkUserResult->num_rows;
        
        if ($checkUserResult->num_rows > 0) {
            $response['success'] = false;
            $response['message'] = 'Username already taken';
            $debug['duplicate_username'] = true;
            $checkUserStmt->close();
            return;
        }
        $checkUserStmt->close();
        
        // Hash password
        $hashedPassword = password_hash($password, PASSWORD_DEFAULT);
        $debug['password_hashed'] = true;
        
        // Insert new user
        $insertSql = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)";
        $insertStmt = $conn->prepare($insertSql);
        $insertStmt->bind_param("sss", $username, $email, $hashedPassword);
        
        if ($insertStmt->execute()) {
            $userId = $conn->insert_id;
            $debug['user_inserted'] = true;
            $debug['new_user_id'] = $userId;
            
            // Initialize user progress
            $defaultProgress = json_encode(array(
                'unlockedLevels' => array(1),
                'completedLevels' => array(),
                'currentLevel' => 1
            ));
            
            $defaultPlayerData = json_encode(array(
                'name' => $username,
                'xp' => 0,
                'health' => 100,
                'totalTasksCompleted' => 0
            ));
            
            $progressSql = "INSERT INTO user_progress (user_id, level_progress, player_data) VALUES (?, ?, ?)";
            $progressStmt = $conn->prepare($progressSql);
            $progressStmt->bind_param("iss", $userId, $defaultProgress, $defaultPlayerData);
            
            if ($progressStmt->execute()) {
                $debug['progress_initialized'] = true;
            } else {
                $debug['progress_init_failed'] = true;
            }
            $progressStmt->close();
            
            $response['success'] = true;
            $response['message'] = 'Account created successfully';
            $response['user'] = array(
                'id' => $userId,
                'username' => $username,
                'email' => $email
            );
            $debug['signup_success'] = true;
        } else {
            $response['success'] = false;
            $response['message'] = 'Failed to create account';
            $debug['insert_failed'] = true;
        }
        
        $insertStmt->close();
    } catch (Exception $e) {
        $response['success'] = false;
        $response['message'] = 'Database error: ' . $e->getMessage();
        $debug['database_error'] = $e->getMessage();
    }
}
?>