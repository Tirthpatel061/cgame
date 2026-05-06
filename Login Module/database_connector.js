// Database Connector for C Programming Game
// This file handles all database operations from the frontend

class DatabaseConnector {
    constructor() {
        this.baseUrl = '../Login Module/';
        this.baseUrls = this.resolveBaseUrls();
        this.userId = localStorage.getItem('userId');
    }

    resolveBaseUrls() {
        const bases = [];
        if (Array.isArray(window.DB_API_BASES)) {
            bases.push(...window.DB_API_BASES);
        }
        if (window.DB_API_BASE) {
            bases.push(window.DB_API_BASE);
        }
        bases.push(this.baseUrl);

        const origin = window.location && window.location.origin ? window.location.origin : '';
        if (origin.includes('localhost:5000') || origin.includes('127.0.0.1:5000')) {
            bases.push('http://localhost/MAIN/Login Module/');
            bases.push('http://localhost/MAIN/MAIN/Login Module/');
        }

        bases.push('http://localhost:5002/');

        const seen = new Set();
        return bases
            .map((base) => base.endsWith('/') ? base : `${base}/`)
            .filter((base) => {
                if (seen.has(base)) return false;
                seen.add(base);
                return true;
            });
    }

    // Generic API call method
    async apiCall(endpoint, data) {
        const errors = [];
        for (const baseUrl of this.baseUrls) {
            try {
                const response = await fetch(baseUrl + endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                if (!response.ok) {
                    errors.push(`${baseUrl} -> HTTP ${response.status}`);
                    continue;
                }

                const result = await response.json();
                return result;
            } catch (error) {
                errors.push(`${baseUrl} -> ${error.message || error}`);
            }
        }

        console.error('API call failed:', errors);
        return { success: false, message: 'Connection error', details: errors };
    }

    // Save level completion
    async saveLevelCompletion(level, completionTime = 0, score = 0) {
        if (!this.userId) {
            console.warn('User not logged in, cannot save level completion');
            return { success: false, message: 'User not logged in' };
        }

        return await this.apiCall('game_api.php', {
            action: 'save_level_completion',
            user_id: this.userId,
            level: level,
            completion_time: completionTime,
            score: score
        });
    }

    // Save task completion
    async saveTaskCompletion(level, taskNumber, code, isCorrect) {
        if (!this.userId) {
            console.warn('User not logged in, cannot save task completion');
            return { success: false, message: 'User not logged in' };
        }

        return await this.apiCall('game_api.php', {
            action: 'save_task_completion',
            user_id: this.userId,
            level: level,
            task_number: taskNumber,
            code: code,
            is_correct: isCorrect
        });
    }

    // Update player stats
    async updatePlayerStats(xp, health, currentLevel) {
        if (!this.userId) {
            console.warn('User not logged in, cannot update player stats');
            return { success: false, message: 'User not logged in' };
        }

        return await this.apiCall('game_api.php', {
            action: 'update_player_stats',
            user_id: this.userId,
            xp: xp,
            health: health,
            current_level: currentLevel
        });
    }

    // Save code submission
    async saveCodeSubmission(level, taskNumber, code, compileResult = '', executionResult = '') {
        if (!this.userId) {
            console.warn('User not logged in, cannot save code submission');
            return { success: false, message: 'User not logged in' };
        }

        return await this.apiCall('game_api.php', {
            action: 'save_code_submission',
            user_id: this.userId,
            level: level,
            task_number: taskNumber,
            code: code,
            compile_result: compileResult,
            execution_result: executionResult
        });
    }

    // Log game session
    async logGameSession(sessionDuration, levelsPlayed) {
        if (!this.userId) {
            console.warn('User not logged in, cannot log game session');
            return { success: false, message: 'User not logged in' };
        }

        return await this.apiCall('game_api.php', {
            action: 'log_game_session',
            user_id: this.userId,
            session_duration: sessionDuration,
            levels_played: JSON.stringify(levelsPlayed)
        });
    }

    // Get leaderboard
    async getLeaderboard(limit = 10) {
        return await this.apiCall('game_api.php', {
            action: 'get_leaderboard',
            limit: limit
        });
    }

    // Save game progress (existing method)
    async saveProgress(levelProgress, playerData) {
        if (!this.userId) {
            console.warn('User not logged in, cannot save progress');
            return { success: false, message: 'User not logged in' };
        }

        return await this.apiCall('game_progress.php', {
            action: 'save_progress',
            user_id: this.userId,
            level_progress: JSON.stringify(levelProgress),
            player_data: JSON.stringify(playerData)
        });
    }

    // Load game progress (existing method)
    async loadProgress() {
        if (!this.userId) {
            console.warn('User not logged in, cannot load progress');
            return { success: false, message: 'User not logged in' };
        }

        return await this.apiCall('game_progress.php', {
            action: 'load_progress',
            user_id: this.userId
        });
    }

    // Update user ID (call this after login)
    setUserId(userId) {
        this.userId = userId;
        localStorage.setItem('userId', userId);
    }

    // Get current user ID
    getUserId() {
        return this.userId || localStorage.getItem('userId');
    }

    // Check if user is logged in
    isLoggedIn() {
        return !!this.getUserId();
    }
}

// Create global instance
window.dbConnector = new DatabaseConnector();

// Auto-update user ID from localStorage on page load
document.addEventListener('DOMContentLoaded', function() {
    const userId = localStorage.getItem('userId');
    if (userId) {
        window.dbConnector.setUserId(userId);
    }
});

// Session tracking
class SessionTracker {
    constructor() {
        this.sessionStart = Date.now();
        this.levelsPlayed = [];
        this.isTracking = false;
    }

    startTracking() {
        if (this.isTracking) return;
        
        this.isTracking = true;
        this.sessionStart = Date.now();
        
        // Track when user leaves the page
        window.addEventListener('beforeunload', () => {
            this.endSession();
        });
        
        // Track visibility changes
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.pauseSession();
            } else {
                this.resumeSession();
            }
        });
    }

    addLevelPlayed(level) {
        if (!this.levelsPlayed.includes(level)) {
            this.levelsPlayed.push(level);
        }
    }

    pauseSession() {
        // Could implement pause logic here
    }

    resumeSession() {
        // Could implement resume logic here
    }

    endSession() {
        if (!this.isTracking) return;
        
        const sessionDuration = Math.floor((Date.now() - this.sessionStart) / 1000); // in seconds
        
        if (window.dbConnector && window.dbConnector.isLoggedIn()) {
            window.dbConnector.logGameSession(sessionDuration, this.levelsPlayed);
        }
        
        this.isTracking = false;
    }

    getSessionDuration() {
        return Math.floor((Date.now() - this.sessionStart) / 1000);
    }
}

// Create global session tracker
window.sessionTracker = new SessionTracker();

// Auto-start session tracking when user is logged in
document.addEventListener('DOMContentLoaded', function() {
    if (window.dbConnector && window.dbConnector.isLoggedIn()) {
        window.sessionTracker.startTracking();
    }
});

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { DatabaseConnector, SessionTracker };
}