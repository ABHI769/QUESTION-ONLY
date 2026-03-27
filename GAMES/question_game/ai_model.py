import random
import re
from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple


class GameState(Enum):
    """Enum representing the possible states of the game."""
    WAITING_FOR_USER = "waiting_for_user"
    WAITING_FOR_AI = "waiting_for_ai"
    GAME_OVER = "game_over"
    USER_WON = "user_won"
    AI_WON = "ai_won"


@dataclass
class Question:
    """Represents a question in the game."""
    text: str
    is_ai: bool
    timestamp: float


class QuestionDetector:
    """Detects if a given text is a valid question."""
    
    QUESTION_STARTERS = [
        'what', 'who', 'where', 'when', 'why', 'how', 'which', 'whose',
        'whom', 'can', 'could', 'would', 'should', 'will', 'do', 'does',
        'did', 'is', 'are', 'am', 'have', 'has', 'had', 'if', "aren't",
        "can't", "won't", "isn't", "don't", "doesn't", "didn't",
        "haven't", "hasn't", "hadn't", 'is it', 'are they', 'do you',
        'did you', 'have you', 'can you', 'could you', 'would you',
        'should you', 'will you', 'are we', 'is this', 'is that'
    ]
    
    @classmethod
    def is_question(cls, text: str) -> Tuple[bool, str]:
        """
        Determine if the given text is a valid question.
        Returns (is_valid, reason_if_invalid)
        """
        if not text or not text.strip():
            return False, "Empty input"
        
        cleaned = text.strip()
        
        # Check for question mark
        if not cleaned.endswith('?'):
            return False, "No question mark found"
        
        # Check for question starters
        lower_text = cleaned.lower()
        has_question_starter = any(
            lower_text.startswith(starter) 
            for starter in cls.QUESTION_STARTERS
        )
        
        # Check for question structure
        question_patterns = [
            r'^(what|who|where|when|why|how|which|whose)\s+\w+',
            r'^(can|could|would|should|will|do|does|did)\s+\w+',
            r'^(is|are|am|have|has|had)\s+\w+',
            r"^isn't|^aren't|^can't|^won't|^wouldn't|^shouldn't",
            r"^didn't|^doesn't|^haven't|^hasn't|^hadn't",
        ]
        
        has_question_structure = any(
            re.search(pattern, lower_text) 
            for pattern in question_patterns
        )
        
        if not (has_question_starter or has_question_structure):
            words = lower_text.split()
            if words and words[0] in ['what', 'who', 'where', 'when', 'why', 'how', 'which', 'whose']:
                return True, ""
            return False, "Doesn't appear to be a question"
        
        # Check for minimum length
        if len(cleaned.split()) < 2:
            return False, "Question too short"
        
        # Check for maximum length
        if len(cleaned.split()) > 30:
            return False, "Question too long"
        
        return True, ""


class QuestionGenerator:
    """Generates contextually relevant questions based on the conversation history."""
    
    # Question templates organized by category
    QUESTION_TEMPLATES = {
        'clarification': [
            "What do you mean by {topic}?",
            "Could you elaborate on {topic}?",
            "What specifically interests you about {topic}?",
            "How does {topic} relate to what we were discussing?",
            "What aspect of {topic} would you like to explore further?",
            "Why do you think {topic} is important in this context?",
            "How would you define {topic}?",
            "What makes {topic} different from similar concepts?",
        ],
        'exploration': [
            "How did you first become interested in {topic}?",
            "What experiences have shaped your view on {topic}?",
            "Why do you think {topic} matters?",
            "What would you do differently if you could revisit {topic}?",
            "How might {topic} evolve in the future?",
            "What are the key challenges with {topic} today?",
            "How does {topic} impact our daily lives?",
            "What misconceptions exist about {topic}?",
        ],
        'connection': [
            "How does {topic} connect to your interests?",
            "What other topics relate to {topic} that you find fascinating?",
            "Have you explored how {topic} intersects with other fields?",
            "What parallels can be drawn between {topic} and other concepts?",
            "How might understanding {topic} help us understand other things?",
        ],
        'deepening': [
            "What would you say is the most surprising thing about {topic}?",
            "How has your understanding of {topic} changed over time?",
            "What questions about {topic} still remain unanswered for you?",
            "How would you explain {topic} to someone unfamiliar with it?",
            "What evidence supports your view on {topic}?",
        ],
        'fun': [
            "What's the most interesting fact you know about {topic}?",
            "If you could change one thing about {topic}, what would it be?",
            "What fictional scenario involving {topic} excites you most?",
            "How would you describe {topic} using only three words?",
        ],
    }

    KEYWORDS = [
        'life', 'work', 'hobby', 'interest', 'passion', 'dream', 'goal',
        'experience', 'memory', 'favorite', 'love', 'hate', 'fear', 'hope',
        'family', 'friend', 'career', 'education', 'travel', 'food', 'music',
        'art', 'science', 'technology', 'nature', 'sports', 'game', 'movie',
        'book', 'city', 'country', 'culture', 'history', 'future', 'past',
        'present', 'idea', 'opinion', 'belief', 'value', 'principle', 'skill'
    ]
    
    def __init__(self):
        self.conversation_history = deque(maxlen=20)
        self.used_questions = set()
        self.question_count = 0
    
    def extract_topic(self, context: List[str]) -> str:
        """Extract a topic from the conversation context."""
        combined = ' '.join(context[-5:]).lower()
        
        for keyword in self.KEYWORDS:
            if keyword in combined:
                return keyword
        
        proper_nouns = re.findall(r'\b[A-Z][a-z]+\b', ' '.join(context))
        if proper_nouns:
            return random.choice(proper_nouns)
        
        words = context[-1].split() if context else []
        for word in reversed(words):
            if len(word) > 3 and word.lower() not in ['what', 'that', 'this', 'then', 'than']:
                return word.rstrip('?.,!')
        
        return "this topic"
    
    def generate_question(self, user_question: str) -> str:
        """Generate a response question based on the user's question."""
        self.question_count += 1
        
        self.conversation_history.append(user_question)
        
        topic = self.extract_topic(list(self.conversation_history))
        
        categories = list(self.QUESTION_TEMPLATES.keys())
        weights = [0.3, 0.3, 0.2, 0.15, 0.05]
        
        if self.question_count % 3 == 0:
            weights = [0.2, 0.25, 0.25, 0.2, 0.1]
        
        selected_category = random.choices(categories, weights=weights)[0]
        templates = self.QUESTION_TEMPLATES[selected_category]
        
        available_templates = [
            t for t in templates 
            if t not in self.used_questions
        ]
        
        if not available_templates:
            available_templates = templates
        
        template = random.choice(available_templates)
        self.used_questions.add(template)
        
        question = template.format(topic=topic)
        
        if random.random() < 0.2:
            question = question.capitalize()
            if not question.endswith('?'):
                question += '?'
        
        return question
    
    def reset(self):
        """Reset the generator state."""
        self.conversation_history.clear()
        self.used_questions.clear()
        self.question_count = 0


class QuestionGameAI:
    """Main AI controller for the Question Only game."""
    
    MAX_TURNS = 20  # Maximum number of user questions before game ends
    
    def __init__(self):
        self.detector = QuestionDetector()
        self.generator = QuestionGenerator()
        self.game_state = GameState.WAITING_FOR_USER
        self.questions = []
        self.streak = 0
        self.ai_streak = 0
        self.error_count = 0
    
    def validate_user_question(self, question: str) -> Tuple[bool, str]:
        """
        Validate the user's question.
        Returns (is_valid, error_message)
        """
        is_valid, reason = self.detector.is_question(question)
        
        if not is_valid:
            return False, reason
        
        if len(self.questions) >= 2:
            recent_questions = [
                q.text.lower() for q in self.questions[-2:] if not q.is_ai
            ]
            if question.lower() in recent_questions:
                return False, "Repeated question"
        
        return True, ""
    
    def process_user_input(self, question: str) -> dict:
        """
        Process user's question and return the AI's response.
        Returns a dict with game state and messages.
        """
        result = {
            'valid': False,
            'message': '',
            'game_state': self.game_state.value,
            'ai_question': '',
            'streak': self.streak,
            'ai_streak': self.ai_streak,
            'error': None
        }
        
        is_valid, error_msg = self.validate_user_question(question)
        
        if not is_valid:
            result['valid'] = False
            result['error'] = error_msg
            result['message'] = f"Invalid question: {error_msg}"
            self.error_count += 1
            
            self.game_state = GameState.AI_WON
            result['game_state'] = self.game_state.value
            result['message'] = f"AI Wins! {error_msg}"
            
            return result
        
        user_q = Question(text=question, is_ai=False, timestamp=__import__('time').time())
        self.questions.append(user_q)
        self.streak += 1
        self.error_count = 0
        result['valid'] = True
        result['streak'] = self.streak
        
        # Check if max turns reached - user wins!
        user_question_count = len([q for q in self.questions if not q.is_ai])
        if user_question_count >= self.MAX_TURNS:
            self.game_state = GameState.USER_WON
            result['game_state'] = self.game_state.value
            result['message'] = f"Congratulations! You won! You completed {self.MAX_TURNS} questions!"
            return result
        
        if self.streak == 5:
            result['message'] = "Great! 5 questions in a row!"
        elif self.streak == 10:
            result['message'] = "Amazing! 10 questions without breaking!"
        
        ai_question = self.generator.generate_question(question)
        self.questions.append(
            Question(text=ai_question, is_ai=True, timestamp=__import__('time').time())
        )
        self.ai_streak += 1
        result['ai_question'] = ai_question
        result['ai_streak'] = self.ai_streak
        
        self.game_state = GameState.WAITING_FOR_USER
        
        return result
    
    def get_game_state(self) -> dict:
        """Get current game state."""
        return {
            'game_state': self.game_state.value,
            'streak': self.streak,
            'ai_streak': self.ai_streak,
            'question_count': len([q for q in self.questions if not q.is_ai]),
            'errors': self.error_count
        }
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.game_state = GameState.WAITING_FOR_USER
        self.questions.clear()
        self.streak = 0
        self.ai_streak = 0
        self.error_count = 0
        self.generator.reset()
    
    def get_rules(self) -> list:
        """Return the game rules as a list."""
        return [
            "Start: You ask a question to begin the game",
            "Response: AI must answer with another question",
            "Chain: You must respond to AI's question with a NEW question",
            "Keep Going: The chain continues until someone breaks the rules",
            "",
            "Ways to Lose:",
            "- Answering with a statement instead of a question",
            "- Not ending with a question mark (?)",
            "- Repeating a previous question",
            "- Taking too long to respond",
            "- Asking a question that's too short or too long",
            "",
            "Tips:",
            "- Listen carefully to the AI's question",
            "- Ask follow-up questions about the topic",
            "- Try to connect your questions to create a conversation",
            "- Have fun exploring different topics!"
        ]

game_ai = QuestionGameAI()