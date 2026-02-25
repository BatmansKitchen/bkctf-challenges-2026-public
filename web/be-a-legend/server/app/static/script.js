let ws = null;
let commandHistory = [];
let historyIndex = -1;
let playerDead = false;

// DOM Elements
const output = document.getElementById('output');
const commandInput = document.getElementById('command-input');
const statusIndicator = document.getElementById('status-indicator');
const statusText = document.getElementById('status-text');
const resetBtn = document.getElementById('reset-btn');

// Stat display elements
const playerHp = document.getElementById('player-hp');
const playerAtk = document.getElementById('player-atk');
const dragonHp = document.getElementById('dragon-hp');
const dragonAtk = document.getElementById('dragon-atk');
const playerHpBar = document.getElementById('player-hp-bar');
const dragonHpBar = document.getElementById('dragon-hp-bar');

// Initial stats for percentage calculation
let initialPlayerHp = 100;
let initialDragonHp = 1000;

// Connect to WebSocket
function connect() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;
    
    addOutput('Connecting to server...', 'info');
    
    ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
        updateStatus(true);
        addOutput('Connection established!', 'success');
    };
    
    ws.onmessage = (event) => {
        handleMessage(event.data);
    };
    
    ws.onerror = (error) => {
        addOutput('WebSocket error occurred', 'error');
        console.error('WebSocket error:', error);
    };
    
    ws.onclose = () => {
        updateStatus(false);
        addOutput('Connection closed. Refresh to reconnect.', 'warning');
    };
}

// Handle incoming messages
function handleMessage(message) {
    // Check for special signals
    if (message === "CLEAR_TERMINAL") {
        output.innerHTML = '';
        return;
    }
    
    if (message === "PLAYER_DIED") {
        playerDead = true;
        resetBtn.style.display = 'inline-block';
        return;
    }
    
    if (message === "GAME_RESET") {
        playerDead = false;
        resetBtn.style.display = 'none';
        // Reset stats display
        updatePlayerHp(100);
        updatePlayerAtk(10);
        updateDragonHp(1000);
        updateDragonAtk(999);
        return;
    }
    
    addOutput(message);
    
    // Parse message for stat updates
    updateStatsFromMessage(message);
    
    // Auto-scroll to bottom
    output.scrollTop = output.scrollHeight;
}

// Update stats from server messages
function updateStatsFromMessage(message) {
    // Player HP
    const playerHpMatch = message.match(/Your HP:\s*(-?\d+)/);
    if (playerHpMatch) {
        const hp = parseInt(playerHpMatch[1]);
        updatePlayerHp(hp);
    }
    
    // Dragon HP
    const dragonHpMatch = message.match(/Dragon HP:\s*([\d,]+)/);
    if (dragonHpMatch) {
        const hp = parseInt(dragonHpMatch[1].replace(/,/g, ''));
        updateDragonHp(hp);
    }
    
    // Parse STATS command response
    const statsMatch = message.match(/Player HP:\s*(\d+).*ATK:\s*(\d+).*Dragon HP:\s*([\d,]+)/s);
    if (statsMatch) {
        updatePlayerHp(parseInt(statsMatch[1]));
        updatePlayerAtk(parseInt(statsMatch[2]));
        updateDragonHp(parseInt(statsMatch[3].replace(/,/g, '')));
    }
}

// Update player HP
function updatePlayerHp(hp) {
    playerHp.textContent = hp;
    const percentage = Math.max(0, (hp / initialPlayerHp) * 100);
    playerHpBar.style.width = `${percentage}%`;
    
    // Change color based on HP
    if (percentage < 25) {
        playerHpBar.style.background = 'linear-gradient(90deg, #ff3333, #cc0000)';
    } else if (percentage < 50) {
        playerHpBar.style.background = 'linear-gradient(90deg, #ffcc00, #ff9900)';
    } else {
        playerHpBar.style.background = 'linear-gradient(90deg, #00ff00, #00cc00)';
    }
}

// Update player ATK
function updatePlayerAtk(atk) {
    playerAtk.textContent = atk;
}

// Update dragon HP
function updateDragonHp(hp) {
    dragonHp.textContent = hp.toLocaleString();
    const percentage = Math.max(0, (hp / initialDragonHp) * 100);
    dragonHpBar.style.width = `${percentage}%`;
}

// Update dragon ATK
function updateDragonAtk(atk) {
    dragonAtk.textContent = atk.toLocaleString();
}

// Add output to terminal
function addOutput(text, className = '') {
    const line = document.createElement('div');
    line.className = `output-line ${className}`;
    
    // Process text for colors
    text = processColorCodes(text);
    line.innerHTML = text;
    
    output.appendChild(line);
    
    // Limit output lines to prevent memory issues
    const maxLines = 1000;
    while (output.children.length > maxLines) {
        output.removeChild(output.firstChild);
    }
}

// Process color codes and emojis
function processColorCodes(text) {
    text = text.replace(/&/g, '&amp;')
               .replace(/</g, '&lt;')
               .replace(/>/g, '&gt;');
    
    // Highlight flag - hardcode this because i hate js
    if (text.includes('bkctf{')) {
        text = text.replace(/(bkctf\{[^}]+\})/g, '<span class="success" style="font-weight: bold; text-shadow: 0 0 10px #00ff00;">$1</span>');
    }
    
    // Preserve line breaks
    text = text.replace(/\n/g, '<br>');
    
    return text;
}

// Send command
function sendCommand(cmd) {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
        addOutput('Not connected to server!', 'error');
        return;
    }
    
    const command = cmd || commandInput.value.trim();
    
    if (!command) return;
    
    // Add to history
    if (cmd === undefined) { // Only add to history if typed manually
        commandHistory.unshift(command);
        if (commandHistory.length > 50) {
            commandHistory.pop();
        }
        historyIndex = -1;
    }
    
    // Display command
    addOutput(`warrior@dragon:~$ ${command}`, 'info');
    
    // Send to server
    ws.send(command);
    
    // Clear input
    commandInput.value = '';
}

// Update connection status
function updateStatus(connected) {
    if (connected) {
        statusIndicator.className = 'status-dot connected';
        statusText.textContent = 'Connected';
    } else {
        statusIndicator.className = 'status-dot disconnected';
        statusText.textContent = 'Disconnected';
    }
}

// Event Listeners
commandInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        sendCommand();
    } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (historyIndex < commandHistory.length - 1) {
            historyIndex++;
            commandInput.value = commandHistory[historyIndex];
        }
    } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (historyIndex > 0) {
            historyIndex--;
            commandInput.value = commandHistory[historyIndex];
        } else if (historyIndex === 0) {
            historyIndex = -1;
            commandInput.value = '';
        }
    } else if (e.key === 'Tab') {
        e.preventDefault();
        // Simple autocomplete
        const commands = ['STATS', 'FIGHT', 'SAVE', 'LOAD', 'RESET', 'QUIT'];
        const input = commandInput.value.toUpperCase();
        const matches = commands.filter(cmd => cmd.startsWith(input));
        if (matches.length === 1) {
            commandInput.value = matches[0];
        }
    }
});

// Initialize
window.addEventListener('load', () => {
    connect();
    commandInput.focus();
});