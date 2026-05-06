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
        case 'save_level_completion':
            saveLevelCompletion($conn, $input);
            break;
        case 'save_task_completion':
            saveTaskCompletion($conn, $input);
            break;
        case 'update_player_stats':
            updatePlayerStats($conn, $input);
            break;
        case 'get_leaderboard':
            getLeaderboard($conn, $input);
            break;
        case 'log_game_session':
            logGameSession($conn, $input);
            break;
        case 'save_code_submission':
            saveCodeSubmission($conn, $input);
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

// Save level completion
function saveLevelCompletion($conn, $input) {
    global $response;
    
    $userId = $input['user_id'] ?? '';
    $level = $input['level'] ?? '';
    $completionTime = $input['completion_time'] ?? 0;
    $score = $input['score'] ?? 0;
    
    if (empty($userId) || empty($level)) {
        $response['success'] = false;
        $response['message'] = 'User ID and level are required';
        return;
    }
    
    try {
        // Create level_completions table if it doesn't exist
        $createTableSql = "CREATE TABLE IF NOT EXISTS level_completions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            level INT NOT NULL,
            completion_time INT DEFAULT 0,
            score INT DEFAULT 0,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE KEY unique_user_level (user_id, level)
        )";
        $conn->query($createTableSql);
        
        // Insert or update level completion
        $sql = "INSERT INTO level_completions (user_id, level, completion_time, score) 
                VALUES (?, ?, ?, ?) 
                ON DUPLICATE KEY UPDATE 
                completion_time = VALUES(completion_time), 
                score = VALUES(score), 
                completed_at = CURRENT_TIMESTAMP";
        
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("iiii", $userId, $level, $completionTime, $score);
        
        if ($stmt->execute()) {
            $response['success'] = true;
            $response['message'] = 'Level completion saved successfully';
        } else {
            $response['success'] = false;
            $response['message'] = 'Failed to save level completion';
        }
        
        $stmt->close();
    } catch (Exception $e) {
        $response['success'] = false;
        $response['message'] = 'Database error: ' . $e->getMessage();
    }
}

// Save task completion
function saveTaskCompletion($conn, $input) {
    global $response;
    
    $userId = $input['user_id'] ?? '';
    $level = $input['level'] ?? '';
    $taskNumber = $input['task_number'] ?? '';
    $code = $input['code'] ?? '';
    $isCorrect = $input['is_correct'] ?? false;
    
    if (empty($userId) || empty($level) || empty($taskNumber)) {
        $response['success'] = false;
        $response['message'] = 'User ID, level, and task number are required';
        return;
    }
    
    try {
        // Create task_submissions table if it doesn't exist
        $createTableSql = "CREATE TABLE IF NOT EXISTS task_submissions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            level INT NOT NULL,
            task_number INT NOT NULL,
            code TEXT,
            is_correct BOOLEAN DEFAULT FALSE,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )";
        $conn->query($createTableSql);
        
        // Insert task submission
        $sql = "INSERT INTO task_submissions (user_id, level, task_number, code, is_correct) 
                VALUES (?, ?, ?, ?, ?)";
        
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("iiiis", $userId, $level, $taskNumber, $code, $isCorrect);
        
        if ($stmt->execute()) {
            $response['success'] = true;
            $response['message'] = 'Task submission saved successfully';
        } else {
            $response['success'] = false;
            $response['message'] = 'Failed to save task submission';
        }
        
        $stmt->close();
    } catch (Exception $e) {
        $response['success'] = false;
        $response['message'] = 'Database error: ' . $e->getMessage();
    }
}

// Update player stats
function updatePlayerStats($conn, $input) {
    global $response;
    
    $userId = $input['user_id'] ?? '';
    $xp = $input['xp'] ?? 0;
    $health = $input['health'] ?? 100;
    $currentLevel = $input['current_level'] ?? 1;
    
    if (empty($userId)) {
        $response['success'] = false;
        $response['message'] = 'User ID is required';
        return;
    }
    
    try {
        // Create player_stats table if it doesn't exist
        $createTableSql = "CREATE TABLE IF NOT EXISTS player_stats (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            xp INT DEFAULT 0,
            health INT DEFAULT 100,
            current_level INT DEFAULT 1,
            total_playtime INT DEFAULT 0,
            last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE KEY unique_user (user_id)
        )";
        $conn->query($createTableSql);
        
        // Insert or update player stats
        $sql = "INSERT INTO player_stats (user_id, xp, health, current_level) 
                VALUES (?, ?, ?, ?) 
                ON DUPLICATE KEY UPDATE 
                xp = VALUES(xp), 
                health = VALUES(health), 
                current_level = VALUES(current_level),
                last_played = CURRENT_TIMESTAMP";
        
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("iiii", $userId, $xp, $health, $currentLevel);
        
        if ($stmt->execute()) {
            $response['success'] = true;
            $response['message'] = 'Player stats updated successfully';
        } else {
            $response['success'] = false;
            $response['message'] = 'Failed to update player stats';
        }
        
        $stmt->close();
    } catch (Exception $e) {
        $response['success'] = false;
        $response['message'] = 'Database error: ' . $e->getMessage();
    }
}

// Get leaderboard
function getLeaderboard($conn, $input) {
    global $response;
    
    $limit = $input['limit'] ?? 10;
    
    try {
        $sql = "SELECT u.username, ps.xp, ps.current_level, ps.last_played,
                       COUNT(lc.level) as levels_completed
                FROM users u
                LEFT JOIN player_stats ps ON u.id = ps.user_id
                LEFT JOIN level_completions lc ON u.id = lc.user_id
                GROUP BY u.id
                ORDER BY ps.xp DESC, ps.current_level DESC
                LIMIT ?";
        
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("i", $limit);
        $stmt->execute();
        $result = $stmt->get_result();
        
        $leaderboard = array();
        while ($row = $result->fetch_assoc()) {
            $leaderboard[] = $row;
        }
        
        $response['success'] = true;
        $response['leaderboard'] = $leaderboard;
        
        $stmt->close();
    } catch (Exception $e) {
        $response['success'] = false;
        $response['message'] = 'Database error: ' . $e->getMessage();
    }
}

// Log game session
function logGameSession($conn, $input) {
    global $response;
    
    $userId = $input['user_id'] ?? '';
    $sessionDuration = $input['session_duration'] ?? 0;
    $levelsPlayed = $input['levels_played'] ?? '';
    
    if (empty($userId)) {
        $response['success'] = false;
        $response['message'] = 'User ID is required';
        return;
    }
    
    try {
        // Create game_sessions table if it doesn't exist
        $createTableSql = "CREATE TABLE IF NOT EXISTS game_sessions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            session_duration INT DEFAULT 0,
            levels_played TEXT,
            session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )";
        $conn->query($createTableSql);
        
        // Insert game session
        $sql = "INSERT INTO game_sessions (user_id, session_duration, levels_played) 
                VALUES (?, ?, ?)";
        
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("iis", $userId, $sessionDuration, $levelsPlayed);
        
        if ($stmt->execute()) {
            $response['success'] = true;
            $response['message'] = 'Game session logged successfully';
        } else {
            $response['success'] = false;
            $response['message'] = 'Failed to log game session';
        }
        
        $stmt->close();
    } catch (Exception $e) {
        $response['success'] = false;
        $response['message'] = 'Database error: ' . $e->getMessage();
    }
}

// Save code submission
function saveCodeSubmission($conn, $input) {
    global $response;
    
    $userId = $input['user_id'] ?? '';
    $level = $input['level'] ?? '';
    $taskNumber = $input['task_number'] ?? '';
    $code = $input['code'] ?? '';
    $compileResult = $input['compile_result'] ?? '';
    $executionResult = $input['execution_result'] ?? '';
    
    if (empty($userId) || empty($level) || empty($taskNumber)) {
        $response['success'] = false;
        $response['message'] = 'User ID, level, and task number are required';
        return;
    }
    
    try {
        // Create code_submissions table if it doesn't exist
        $createTableSql = "CREATE TABLE IF NOT EXISTS code_submissions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            level INT NOT NULL,
            task_number INT NOT NULL,
            code TEXT,
            compile_result TEXT,
            execution_result TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )";
        $conn->query($createTableSql);

        // Create detailed code_runs table if it doesn't exist
        $createRunsSql = "CREATE TABLE IF NOT EXISTS code_runs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            level INT NOT NULL,
            task_number INT NOT NULL,
            code TEXT,
            result_text TEXT,
            status VARCHAR(20) NOT NULL,
            error_type VARCHAR(50),
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            INDEX idx_code_runs_user (user_id),
            INDEX idx_code_runs_level (level),
            INDEX idx_code_runs_status (status)
        )";
        $conn->query($createRunsSql);
        
        // Insert code submission
        $sql = "INSERT INTO code_submissions (user_id, level, task_number, code, compile_result, execution_result) 
                VALUES (?, ?, ?, ?, ?, ?)";
        
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("iiisss", $userId, $level, $taskNumber, $code, $compileResult, $executionResult);
        
        $status = (strpos($compileResult, 'Success') !== false) ? 'success' : 'error';
        $errorType = null;
        if ($status === 'error') {
            if (stripos($compileResult, 'Compilation Failed') !== false) {
                $errorType = 'compile';
            } elseif (stripos($compileResult, 'Runtime Error') !== false) {
                $errorType = 'runtime';
            } elseif (stripos($compileResult, 'Wrong Output') !== false) {
                $errorType = 'wrong_output';
            } elseif (stripos($compileResult, 'Timeout') !== false) {
                $errorType = 'timeout';
            } else {
                $errorType = 'other';
            }
        }

        $runSql = "INSERT INTO code_runs (user_id, level, task_number, code, result_text, status, error_type) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)";
        $runStmt = $conn->prepare($runSql);
        $runStmt->bind_param("iiissss", $userId, $level, $taskNumber, $code, $compileResult, $status, $errorType);

        if ($stmt->execute() && $runStmt->execute()) {
            $response['success'] = true;
            $response['message'] = 'Code submission saved successfully';
        } else {
            $response['success'] = false;
            $response['message'] = 'Failed to save code submission';
        }
        
        $stmt->close();
        $runStmt->close();
    } catch (Exception $e) {
        $response['success'] = false;
        $response['message'] = 'Database error: ' . $e->getMessage();
    }
}
?>