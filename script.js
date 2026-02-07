// Game state
let gameState = {
    game_state: 'waiting_for_user',
    streak: 0,
    ai_streak: 0,
    question_count: 0
};

// DOM Elements
const chatContainer = document.getElementById('chat-container');
const chatMessages = document.getElementById('chat-messages');
const questionInput = document.getElementById('question-input');
const sendBtn = document.getElementById('send-btn');
const validationHint = document.getElementById('validation-hint');
const userStreakEl = document.getElementById('user-streak');
const aiStreakEl = document.getElementById('ai-streak');
const totalQuestionsEl = document.getElementById('total-questions');
const welcomeMessage = document.getElementById('welcome-message');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Focus input
    questionInput.focus();
    
    // Event listeners
    questionInput.addEventListener('keypress', handleKeyPress);
    questionInput.addEventListener('input', handleInput);
});

// Handle Enter key
function handleKeyPress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendQuestion();
    }
}

// Handle input changes
function handleInput() {
    const text = questionInput.value.trim();
    validationHint.innerHTML = '';
    validationHint.className = 'input-hint';
}

// Send question to server
async function sendQuestion() {
    const question = questionInput.value.trim();
    
    if (!question) {
        showValidationError('Please enter a question');
        return;
    }
    
    if (!question.endsWith('?')) {
        showValidationError('Your question must end with a question mark (?)');
        return;
    }
    
    // Disable input during processing
    setInputEnabled(false);
    
    try {
        const response = await fetch('/api/play', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });
        
        const result = await response.json();
        
        // Update game state
        gameState = {
            game_state: result.game_state,
            streak: result.streak,
            ai_streak: result.ai_streak,
            question_count: result.streak
        };
        
        // Hide welcome message
        if (welcomeMessage) {
            welcomeMessage.style.display = 'none';
        }
        
        if (result.valid) {
            // Add user's question to chat
            addMessage(question, 'user');
            updateStats();
            
            // Add AI's response question
            if (result.ai_question) {
                addMessage(result.ai_question, 'ai');
            }
            
            // Show streak message if any
            if (result.message) {
                showStreakMessage(result.message);
            }
        } else {
            // Game over - user made a mistake
            addMessage(question, 'user');
            showGameOver('ai_won', result.message);
        }
        
        // Clear input
        questionInput.value = '';
        validationHint.innerHTML = '';
        
    } catch (error) {
        console.error('Error:', error);
        showValidationError('An error occurred. Please try again.');
    } finally {
        setInputEnabled(true);
    }
}

// Add message to chat
function addMessage(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const textP = document.createElement('p');
    textP.textContent = text;
    
    const timestamp = document.createElement('div');
    timestamp.className = 'message-timestamp';
    timestamp.textContent = formatTime(new Date());
    
    contentDiv.appendChild(textP);
    contentDiv.appendChild(timestamp);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Format time
function formatTime(date) {
    return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Update stats display
function updateStats() {
    userStreakEl.textContent = gameState.streak;
    aiStreakEl.textContent = gameState.ai_streak;
    totalQuestionsEl.textContent = gameState.question_count;
    
    // Add animation
    userStreakEl.style.transform = 'scale(1.2)';
    setTimeout(() => {
        userStreakEl.style.transform = 'scale(1)';
    }, 200);
}

// Show validation error
function showValidationError(message) {
    validationHint.innerHTML = `<span class="error">❌ ${message}</span>`;
    validationHint.className = 'input-hint';
    questionInput.focus();
}

// Show success message
function showValidationSuccess(message) {
    validationHint.innerHTML = `<span class="success">✅ ${message}</span>`;
    validationHint.className = 'input-hint';
}

// Show streak message
function showStreakMessage(message) {
    validationHint.innerHTML = `<span class="success">🎉 ${message}</span>`;
    validationHint.className = 'input-hint';
    setTimeout(() => {
        validationHint.innerHTML = '';
        validationHint.className = 'input-hint';
    }, 3000);
}

// Set input enabled/disabled
function setInputEnabled(enabled) {
    questionInput.disabled = !enabled;
    sendBtn.disabled = !enabled;
    
    if (enabled) {
        questionInput.focus();
    }
}

// Show rules modal
async function showRules() {
    try {
        const response = await fetch('/api/rules');
        const result = await response.json();
        
        document.getElementById('rules-modal').classList.add('active');
    } catch (error) {
        console.error('Error fetching rules:', error);
    }
}

// Close rules modal
function closeRules() {
    document.getElementById('rules-modal').classList.remove('active');
}

// Show game over modal
function showGameOver(result, message) {
    const modal = document.getElementById('gameover-modal');
    const titleEl = document.getElementById('gameover-title');
    const messageEl = document.getElementById('gameover-message');
    
    if (result === 'ai_won') {
        titleEl.textContent = '🎉 AI Wins!';
        messageEl.innerHTML = `${message}<br><br>The game lasted ${gameState.question_count} questions.`;
    } else {
        titleEl.textContent = '🎊 You Win!';
        messageEl.innerHTML = `${message}<br><br>Great job keeping the questions going!`;
    }
    
    document.getElementById('final-user-streak').textContent = gameState.streak;
    document.getElementById('final-ai-streak').textContent = gameState.ai_streak;
    document.getElementById('final-total').textContent = gameState.question_count;
    
    modal.classList.add('active');
    setInputEnabled(false);
}

// Close game over modal
function closeGameOver() {
    document.getElementById('gameover-modal').classList.remove('active');
}

// Reset game
async function resetGame() {
    try {
        const response = await fetch('/api/reset', {
            method: 'POST'
        });
        
        const result = await response.json();
        
        // Reset game state
        gameState = {
            game_state: result.state.game_state,
            streak: 0,
            ai_streak: 0,
            question_count: 0
        };
        
        // Reset UI
        updateStats();
        chatMessages.innerHTML = '';
        
        if (welcomeMessage) {
            welcomeMessage.style.display = 'block';
        }
        
        // Close modals
        document.getElementById('gameover-modal').classList.remove('active');
        document.getElementById('rules-modal').classList.remove('active');
        
        // Enable input
        setInputEnabled(true);
        questionInput.focus();
        
    } catch (error) {
        console.error('Error resetting game:', error);
    }
}

// Close modals when clicking outside
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
    }
});

// Close modals with Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.getElementById('rules-modal').classList.remove('active');
        document.getElementById('gameover-modal').classList.remove('active');
    }
});
