<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>C Game - Admin Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #f8f9fa;
            font-weight: bold;
        }
        tr:hover {
            background: #f5f5f5;
        }
        .progress-bar {
            width: 100px;
            height: 10px;
            background: #e0e0e0;
            border-radius: 5px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #45a049);
            transition: width 0.3s ease;
        }
        .level-badge {
            background: #007bff;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8em;
        }
        .xp-badge {
            background: #28a745;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8em;
        }
        .refresh-btn {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-bottom: 20px;
        }
        .refresh-btn:hover {
            background: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎮 C Programming Game - Admin Dashboard</h1>
        
        <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Data</button>
        
        <?php
        require_once 'config.php';
        
        // Get statistics
        try {
            // Total users
            $totalUsersResult = $conn->query("SELECT COUNT(*) as count FROM users");
            $totalUsers = $totalUsersResult->fetch_assoc()['count'];
            
            // Users with progress
            $activeUsersResult = $conn->query("SELECT COUNT(DISTINCT user_id) as count FROM user_progress");
            $activeUsers = $activeUsersResult->fetch_assoc()['count'];
            
            // Recent users (last 7 days)
            $recentUsersResult = $conn->query("SELECT COUNT(*) as count FROM users WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)");
            $recentUsers = $recentUsersResult->fetch_assoc()['count'];
            
            // Average level
            $avgLevelResult = $conn->query("SELECT AVG(JSON_EXTRACT(level_progress, '$.currentLevel')) as avg_level FROM user_progress");
            $avgLevel = round($avgLevelResult->fetch_assoc()['avg_level'], 1);
            
            echo '<div class="stats-grid">';
            echo '<div class="stat-card"><div class="stat-number">' . $totalUsers . '</div><div class="stat-label">Total Users</div></div>';
            echo '<div class="stat-card"><div class="stat-number">' . $activeUsers . '</div><div class="stat-label">Active Players</div></div>';
            echo '<div class="stat-card"><div class="stat-number">' . $recentUsers . '</div><div class="stat-label">New This Week</div></div>';
            echo '<div class="stat-card"><div class="stat-number">' . $avgLevel . '</div><div class="stat-label">Average Level</div></div>';
            echo '</div>';
            
        } catch (Exception $e) {
            echo '<p style="color: red;">Error loading statistics: ' . $e->getMessage() . '</p>';
        }
        ?>
        
        <h2>👥 User List</h2>
        
        <h2>📊 Detailed Analytics</h2>
        <div class="stats-grid">
            <?php
            try {
                // Code submissions today
                $todaySubmissionsResult = $conn->query("SELECT COUNT(*) as count FROM code_submissions WHERE DATE(submitted_at) = CURDATE()");
                $todaySubmissions = $todaySubmissionsResult->fetch_assoc()['count'];
                
                // Average session duration
                $avgSessionResult = $conn->query("SELECT AVG(session_duration) as avg_duration FROM game_sessions WHERE session_duration > 0");
                $avgSession = round($avgSessionResult->fetch_assoc()['avg_duration'] / 60, 1); // Convert to minutes
                
                // Total tasks completed
                $totalTasksResult = $conn->query("SELECT COUNT(*) as count FROM task_submissions WHERE is_correct = 1");
                $totalTasks = $totalTasksResult->fetch_assoc()['count'];
                
                // Success rate
                $totalAttemptsResult = $conn->query("SELECT COUNT(*) as count FROM task_submissions");
                $totalAttempts = $totalAttemptsResult->fetch_assoc()['count'];
                $successRate = $totalAttempts > 0 ? round(($totalTasks / $totalAttempts) * 100, 1) : 0;
                
                echo '<div class="stat-card"><div class="stat-number">' . $todaySubmissions . '</div><div class="stat-label">Code Submissions Today</div></div>';
                echo '<div class="stat-card"><div class="stat-number">' . $avgSession . 'm</div><div class="stat-label">Avg Session Duration</div></div>';
                echo '<div class="stat-card"><div class="stat-number">' . $totalTasks . '</div><div class="stat-label">Tasks Completed</div></div>';
                echo '<div class="stat-card"><div class="stat-number">' . $successRate . '%</div><div class="stat-label">Success Rate</div></div>';
                
            } catch (Exception $e) {
                echo '<div class="stat-card"><div class="stat-number">Error</div><div class="stat-label">Loading Analytics</div></div>';
            }
            ?>
        </div>
        
        <h2>👥 User List</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Current Level</th>
                    <th>XP Points</th>
                    <th>Progress</th>
                    <th>Completed Levels</th>
                    <th>Last Login</th>
                    <th>Registered</th>
                </tr>
            </thead>
            <tbody>
                <?php
                try {
                    $sql = "SELECT u.id, u.username, u.email, u.last_login, u.created_at,
                                   up.level_progress, up.player_data, up.updated_at
                            FROM users u 
                            LEFT JOIN user_progress up ON u.id = up.user_id 
                            ORDER BY u.created_at DESC";
                    
                    $result = $conn->query($sql);
                    
                    if ($result->num_rows > 0) {
                        while($row = $result->fetch_assoc()) {
                            $levelProgress = $row['level_progress'] ? json_decode($row['level_progress'], true) : null;
                            $playerData = $row['player_data'] ? json_decode($row['player_data'], true) : null;
                            
                            $currentLevel = $levelProgress ? $levelProgress['currentLevel'] : 1;
                            $completedLevels = $levelProgress ? count($levelProgress['completedLevels']) : 0;
                            $xpPoints = $playerData ? $playerData['xp'] : 0;
                            $progressPercent = round(($completedLevels / 8) * 100);
                            
                            echo '<tr>';
                            echo '<td>' . $row['id'] . '</td>';
                            echo '<td><strong>' . htmlspecialchars($row['username']) . '</strong></td>';
                            echo '<td>' . htmlspecialchars($row['email']) . '</td>';
                            echo '<td><span class="level-badge">Level ' . $currentLevel . '</span></td>';
                            echo '<td><span class="xp-badge">' . $xpPoints . ' XP</span></td>';
                            echo '<td>';
                            echo '<div class="progress-bar">';
                            echo '<div class="progress-fill" style="width: ' . $progressPercent . '%"></div>';
                            echo '</div>';
                            echo '<small>' . $progressPercent . '%</small>';
                            echo '</td>';
                            echo '<td>' . $completedLevels . '/8</td>';
                            echo '<td>' . ($row['last_login'] ? date('M j, Y H:i', strtotime($row['last_login'])) : 'Never') . '</td>';
                            echo '<td>' . date('M j, Y', strtotime($row['created_at'])) . '</td>';
                            echo '</tr>';
                        }
                    } else {
                        echo '<tr><td colspan="9" style="text-align: center; color: #666;">No users found</td></tr>';
                    }
                } catch (Exception $e) {
                    echo '<tr><td colspan="9" style="color: red;">Error loading users: ' . $e->getMessage() . '</td></tr>';
                }
                ?>
            </tbody>
        </table>
        
        <h2>📊 Level Completion Statistics</h2>
        <table>
            <thead>
                <tr>
                    <th>Level</th>
                    <th>Completed By</th>
                    <th>Completion Rate</th>
                    <th>Progress Bar</th>
                </tr>
            </thead>
            <tbody>
                <?php
                try {
                    for ($level = 1; $level <= 8; $level++) {
                        $sql = "SELECT COUNT(*) as count FROM user_progress 
                                WHERE JSON_CONTAINS(JSON_EXTRACT(level_progress, '$.completedLevels'), '$level')";
                        $result = $conn->query($sql);
                        $completedCount = $result->fetch_assoc()['count'];
                        $completionRate = $activeUsers > 0 ? round(($completedCount / $activeUsers) * 100) : 0;
                        
                        echo '<tr>';
                        echo '<td><strong>Level ' . $level . '</strong></td>';
                        echo '<td>' . $completedCount . ' users</td>';
                        echo '<td>' . $completionRate . '%</td>';
                        echo '<td>';
                        echo '<div class="progress-bar">';
                        echo '<div class="progress-fill" style="width: ' . $completionRate . '%"></div>';
                        echo '</div>';
                        echo '</td>';
                        echo '</tr>';
                    }
                } catch (Exception $e) {
                    echo '<tr><td colspan="4" style="color: red;">Error loading level statistics: ' . $e->getMessage() . '</td></tr>';
                }
                ?>
            </tbody>
        </table>
        
        <div style="margin-top: 30px; padding: 15px; background: #e9ecef; border-radius: 5px; font-size: 0.9em; color: #666;">
            <strong>📝 Note:</strong> This dashboard shows real-time data from your C Programming Game. 
            Users' progress is automatically saved to the database when they play the game.
            <br><br>
            <strong>🔗 Database:</strong> <?php echo $dbname; ?> | 
            <strong>📅 Last Updated:</strong> <?php echo date('Y-m-d H:i:s'); ?>
        </div>
    </div>
</body>
</html>
        
        <h2>💻 Recent Code Submissions</h2>
        <table>
            <thead>
                <tr>
                    <th>User</th>
                    <th>Level</th>
                    <th>Task</th>
                    <th>Code Preview</th>
                    <th>Status</th>
                    <th>Submitted</th>
                </tr>
            </thead>
            <tbody>
                <?php
                try {
                    $sql = "SELECT u.username, cs.level, cs.task_number, cs.code, 
                                   cs.compile_result, cs.execution_result, cs.submitted_at
                            FROM code_submissions cs
                            JOIN users u ON cs.user_id = u.id
                            ORDER BY cs.submitted_at DESC
                            LIMIT 20";
                    
                    $result = $conn->query($sql);
                    
                    if ($result->num_rows > 0) {
                        while($row = $result->fetch_assoc()) {
                            $codePreview = strlen($row['code']) > 50 ? substr($row['code'], 0, 50) . '...' : $row['code'];
                            $status = empty($row['compile_result']) ? '✅ Success' : '❌ Error';
                            $statusClass = empty($row['compile_result']) ? 'style="color: green;"' : 'style="color: red;"';
                            
                            echo '<tr>';
                            echo '<td><strong>' . htmlspecialchars($row['username']) . '</strong></td>';
                            echo '<td>Level ' . $row['level'] . '</td>';
                            echo '<td>Task ' . $row['task_number'] . '</td>';
                            echo '<td><code style="background: #f5f5f5; padding: 2px 4px; border-radius: 3px;">' . htmlspecialchars($codePreview) . '</code></td>';
                            echo '<td ' . $statusClass . '>' . $status . '</td>';
                            echo '<td>' . date('M j, H:i', strtotime($row['submitted_at'])) . '</td>';
                            echo '</tr>';
                        }
                    } else {
                        echo '<tr><td colspan="6" style="text-align: center; color: #666;">No code submissions yet</td></tr>';
                    }
                } catch (Exception $e) {
                    echo '<tr><td colspan="6" style="color: red;">Error loading code submissions: ' . $e->getMessage() . '</td></tr>';
                }
                ?>
            </tbody>
        </table>
        
        <h2>🎮 Game Sessions</h2>
        <table>
            <thead>
                <tr>
                    <th>User</th>
                    <th>Duration</th>
                    <th>Levels Played</th>
                    <th>Session Start</th>
                </tr>
            </thead>
            <tbody>
                <?php
                try {
                    $sql = "SELECT u.username, gs.session_duration, gs.levels_played, gs.session_start
                            FROM game_sessions gs
                            JOIN users u ON gs.user_id = u.id
                            ORDER BY gs.session_start DESC
                            LIMIT 15";
                    
                    $result = $conn->query($sql);
                    
                    if ($result->num_rows > 0) {
                        while($row = $result->fetch_assoc()) {
                            $duration = gmdate("H:i:s", $row['session_duration']);
                            $levelsPlayed = $row['levels_played'] ? json_decode($row['levels_played'], true) : [];
                            $levelsText = is_array($levelsPlayed) ? implode(', ', $levelsPlayed) : 'None';
                            
                            echo '<tr>';
                            echo '<td><strong>' . htmlspecialchars($row['username']) . '</strong></td>';
                            echo '<td>' . $duration . '</td>';
                            echo '<td>' . $levelsText . '</td>';
                            echo '<td>' . date('M j, Y H:i', strtotime($row['session_start'])) . '</td>';
                            echo '</tr>';
                        }
                    } else {
                        echo '<tr><td colspan="4" style="text-align: center; color: #666;">No game sessions recorded</td></tr>';
                    }
                } catch (Exception $e) {
                    echo '<tr><td colspan="4" style="color: red;">Error loading game sessions: ' . $e->getMessage() . '</td></tr>';
                }
                ?>
            </tbody>
        </table>
    </div>
</body>
</html>