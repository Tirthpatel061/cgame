<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    exit(0);
}

require_once 'config.php';

$response = array();

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    $action = $input['action'] ?? '';
    
    switch ($action) {
        case 'login':
            handleLogin($conn, $input);
            break;
        case 'signup':
            handleSignup($conn, $input);
            break;
        default:
            $response['success'] = false;
            $response['message'] = 'Invalid action';
            break;
    }
} else {
    $response['success'] = false;
    $response['message'] = 'Only POST method allowed';
}

echo json_encode($response);

function handleLogin($conn, $input) {
    global $response;
    
    $identifier = trim($input['identifier'] ?? '');
    $password = $input['password'] ?? '';
    
    if (empty($identifier) || empty($password)) {
        $response['success'] = false;
        $response['message'] = 'All fields are required';
        return;
    }
    
    try {
        // Check if identifier is email or username
        $sql = "SELECT id, username, email, password FROM users WHERE email = ? OR username = ?";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("ss", $identifier, $identifier);
        $stmt->execute();
        $result = $stmt->get_result();
        
        if ($result->num_rows == 1) {
            $user = $result->fetch_assoc();
            
            if (password_verify($password, $user['password'])) {
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
            } else {
                $response['success'] = false;
                $response['message'] = 'Invalid credentials';
            }
        } else {
            $response['success'] = false;
            $response['message'] = 'User not found';
        }
        
        $stmt->close();
    } catch (Exception $e) {
        $response['success'] = false;
        $response['message'] = 'Database error: ' . $e->getMessage();
    }
}

function handleSignup($conn, $input) {
    global $response;
    
    $username = trim($input['username'] ?? '');
    $email = trim($input['email'] ?? '');
    $password = $input['password'] ?? '';
    $confirmPassword = $input['confirmPassword'] ?? '';
    
    // Validation
    if (empty($username) || empty($email) || empty($password) || empty($confirmPassword)) {
        $response['success'] = false;
        $response['message'] = 'All fields are required';
        return;
    }
    
    if ($password !== $confirmPassword) {
        $response['success'] = false;
        $response['message'] = 'Passwords do not match';
        return;
    }
    
    if (strlen($password) < 6) {
        $response['success'] = false;
        $response['message'] = 'Password must be at least 6 characters long';
        return;
    }
    
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $response['success'] = false;
        $response['message'] = 'Invalid email format';
        return;
    }
    
    try {
        // Check if email already exists
        $checkSql = "SELECT id FROM users WHERE email = ?";
        $checkStmt = $conn->prepare($checkSql);
        $checkStmt->bind_param("s", $email);
        $checkStmt->execute();
        $checkResult = $checkStmt->get_result();
        
        if ($checkResult->num_rows > 0) {
            $response['success'] = false;
            $response['message'] = 'Email already registered';
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
        
        if ($checkUserResult->num_rows > 0) {
            $response['success'] = false;
            $response['message'] = 'Username already taken';
            $checkUserStmt->close();
            return;
        }
        $checkUserStmt->close();
        
        // Hash password
        $hashedPassword = password_hash($password, PASSWORD_DEFAULT);
        
        // Insert new user
        $insertSql = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)";
        $insertStmt = $conn->prepare($insertSql);
        $insertStmt->bind_param("sss", $username, $email, $hashedPassword);
        
        if ($insertStmt->execute()) {
            $userId = $conn->insert_id;
            
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
            $progressStmt->execute();
            $progressStmt->close();
            
            $response['success'] = true;
            $response['message'] = 'Account created successfully';
            $response['user'] = array(
                'id' => $userId,
                'username' => $username,
                'email' => $email
            );
        } else {
            $response['success'] = false;
            $response['message'] = 'Failed to create account';
        }
        
        $insertStmt->close();
    } catch (Exception $e) {
        $response['success'] = false;
        $response['message'] = 'Database error: ' . $e->getMessage();
    }
}
?>