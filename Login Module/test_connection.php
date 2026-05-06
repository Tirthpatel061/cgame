<?php
// Simple test to verify database connection and table creation
require_once 'config.php';

echo "<h1>🔧 Database Connection Test</h1>";

// Test database connection
try {
    echo "<h2>✅ Database Connection: SUCCESS</h2>";
    echo "<p>Connected to database: <strong>" . $conn->server_info . "</strong></p>";
    
    // Test if tables exist
    $tables = ['users', 'user_progress', 'player_stats', 'level_completions', 'task_submissions', 'code_submissions', 'game_sessions'];
    
    echo "<h2>📋 Table Status:</h2>";
    echo "<ul>";
    
    foreach ($tables as $table) {
        $result = $conn->query("SHOW TABLES LIKE '$table'");
        if ($result->num_rows > 0) {
            echo "<li>✅ <strong>$table</strong> - EXISTS</li>";
        } else {
            echo "<li>❌ <strong>$table</strong> - MISSING</li>";
        }
    }
    echo "</ul>";
    
    // Test user count
    $userResult = $conn->query("SELECT COUNT(*) as count FROM users");
    if ($userResult) {
        $userCount = $userResult->fetch_assoc()['count'];
        echo "<h2>👥 Current Users: $userCount</h2>";
    }
    
    // Show recent users
    $recentUsers = $conn->query("SELECT username, email, created_at FROM users ORDER BY created_at DESC LIMIT 5");
    if ($recentUsers && $recentUsers->num_rows > 0) {
        echo "<h2>🆕 Recent Users:</h2>";
        echo "<table border='1' style='border-collapse: collapse; width: 100%;'>";
        echo "<tr><th>Username</th><th>Email</th><th>Registered</th></tr>";
        while ($row = $recentUsers->fetch_assoc()) {
            echo "<tr>";
            echo "<td>" . htmlspecialchars($row['username']) . "</td>";
            echo "<td>" . htmlspecialchars($row['email']) . "</td>";
            echo "<td>" . $row['created_at'] . "</td>";
            echo "</tr>";
        }
        echo "</table>";
    } else {
        echo "<h2>📝 No users registered yet</h2>";
        echo "<p>Try registering a new user to test the system!</p>";
    }
    
} catch (Exception $e) {
    echo "<h2>❌ Database Connection: FAILED</h2>";
    echo "<p>Error: " . $e->getMessage() . "</p>";
}

echo "<hr>";
echo "<h2>🔗 Quick Links:</h2>";
echo "<ul>";
echo "<li><a href='../Home Page/arena.html'>🎮 Start Game</a></li>";
echo "<li><a href='login.html'>🔐 Login Page</a></li>";
echo "<li><a href='admin_dashboard.php'>📊 Admin Dashboard</a></li>";
echo "<li><a href='../kings-and-pigs-main/map.html'>🗺️ Game Map</a></li>";
echo "</ul>";

echo "<hr>";
echo "<p><strong>📅 Test completed at:</strong> " . date('Y-m-d H:i:s') . "</p>";
?>

<style>
body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
h1 { color: #333; }
h2 { color: #666; }
table { background: white; padding: 10px; }
th { background: #007bff; color: white; padding: 8px; }
td { padding: 8px; }
ul { background: white; padding: 15px; border-radius: 5px; }
li { margin: 5px 0; }
a { color: #007bff; text-decoration: none; }
a:hover { text-decoration: underline; }
</style>