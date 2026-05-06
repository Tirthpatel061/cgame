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
        case 'save_progress':
            saveProgress($conn, $input);
            break;
        case 'load_progress':
            loadProgress($conn, $input);
            break;
        case 'get_user_stats':
            getUserStats($conn, $input);
            break;
        default:
            $response['success'] = false;
            $response['message'] = 'Invalid action';
            break;
    }
} else if ($_SERVER['REQUEST_METHOD'] == 'GET') {
    // Handle GET requests for loading progress
    $action = $_GET['action'] ?? '';
    $userId = $_GET['user_id'] ?? '';
    
    if ($action === 'load_progress' && $userId) {
        loadProgress($conn, array('user_id' => $userId));
    } else {
        $response['success'] = false;
        $response['message'] = 'Invalid GET request';
    }
} else {
    $response['success'] = false;
    $response['message'] = 'Only POST and GET methods allowed';
}

echo json_encode($response);

function saveProgress($conn, $input) {
    global $response;
    
    $userId = $input['user_id'] ?? '';
    $levelProgress = $input['level_progress'] ?? '';
    $playerData = $input['player_data'] ?? '';
    
    if (empty($userId)) {
        $response['success'] = false;
        $response['message'] = 'User ID is required';
        return;
    }
    
    try {
        // Check if user progress exists
        $checkSql = "SELECT id FROM user_progress WHERE user_id = ?";
        $checkStmt = $conn->prepare($checkSql);
        $checkStmt->bind_param("i", $userId);
        $checkStmt->execute();
        $checkResult = $checkStmt->get_result();
        
        if ($checkResult->num_rows > 0) {
            // Update existing progress
            $updateSql = "UPDATE user_progress SET level_progress = ?, player_data = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?";
            $updateStmt = $conn->prepare($updateSql);
            $updateStmt->bind_param("ssi", $levelProgress, $playerData, $userId);
            
            if ($updateStmt->execute()) {
                $response['success'] = true;
                $response['message'] = 'Progress updated successfully';
            } else {
                $response['success'] = false;
                $response['message'] = 'Failed to update progress';
            }
            $updateStmt->close();
        } else {
            // Insert new progress
            $insertSql = "INSERT INTO user_progress (user_id, level_progress, player_data) VALUES (?, ?, ?)";
            $insertStmt = $conn->prepare($insertSql);
            $insertStmt->bind_param("iss", $userId, $levelProgress, $playerData);
            
            if ($insertStmt->execute()) {
                $response['success'] = true;
                $response['message'] = 'Progress saved successfully';
            } else {
                $response['success'] = false;
                $response['message'] = 'Failed to save progress';
            }
            $insertStmt->close();
        }
        
        $checkStmt->close();
    } catch (Exception $e) {
        $response['success'] = false;
        $response['message'] = 'Database error: ' . $e->getMessage();
    }
}

function loadProgress($conn, $input) {
    global $response;
    
    $userId = $input['user_id'] ?? '';
    
    if (empty($userId)) {
        $response['success'] = false;
        $response['message'] = 'User ID is required';
        return;
    }
    
    try {
        $sql = "SELECT level_progress, player_data, updated_at FROM user_progress WHERE user_id = ?";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("i", $userId);
        $stmt->execute();
        $result = $stmt->get_result();
        
        if ($result->num_rows > 0) {
            $progress = $result->fetch_assoc();
            $response['success'] = true;
            $response['level_progress'] = json_decode($progress['level_progress'], true);
            $response['player_data'] = json_decode($progress['player_data'], true);
            $response['last_updated'] = $progress['updated_at'];
        } else {
            // Return default progress if none exists
            $response['success'] = true;
            $response['level_progress'] = array(
                'unlockedLevels' => array(1),
                'completedLevels' => array(),
                'currentLevel' => 1
            );
            $response['player_data'] = array(
                'name' => 'Player',
                'xp' => 0,
                'health' => 100,
                'totalTasksCompleted' => 0
            );
            $response['message'] = 'No progress found, returning defaults';
        }
        
        $stmt->close();
    } catch (Exception $e) {
        $response['success'] = false;
        $response['message'] = 'Database error: ' . $e->getMessage();
    }
}

function getUserStats($conn, $input) {
    global $response;
    
    try {
        // Get total users
        $totalUsersSql = "SELECT COUNT(*) as total_users FROM users";
        $totalUsersResult = $conn->query($totalUsersSql);
        $totalUsers = $totalUsersResult->fetch_assoc()['total_users'];
        
        // Get users with progress
        $activeUsersSql = "SELECT COUNT(DISTINCT user_id) as active_users FROM user_progress";
        $activeUsersResult = $conn->query($activeUsersSql);
        $activeUsers = $activeUsersResult->fetch_assoc()['active_users'];
        
        // Get recent registrations (last 7 days)
        $recentUsersSql = "SELECT COUNT(*) as recent_users FROM users WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)";
        $recentUsersResult = $conn->query($recentUsersSql);
        $recentUsers = $recentUsersResult->fetch_assoc()['recent_users'];
        
        $response['success'] = true;
        $response['stats'] = array(
            'total_users' => $totalUsers,
            'active_users' => $activeUsers,
            'recent_users' => $recentUsers
        );
        
    } catch (Exception $e) {
        $response['success'] = false;
        $response['message'] = 'Database error: ' . $e->getMessage();
    }
}
?>