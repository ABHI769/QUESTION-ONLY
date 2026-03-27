# Question Only Game

A conversational AI game where players must respond only with questions. The challenge is to keep the conversation going without breaking the rules!

## 🎮 How to Play

1. **Start**: Ask a question to begin the game
2. **Response**: The AI will respond with another question
3. **Chain**: You must respond to AI's question with a NEW question
4. **Keep Going**: The chain continues until someone breaks the rules

## 🚫 Ways to Lose

- Answering with a statement instead of a question
- Not ending with a question mark (?)
- Repeating a previous question
- Asking a question that's too short or too long

## 🛠️ Installation

1. Make sure you have Python 3.8+ installed

2. Install the required dependencies:
```bash
cd question_game
pip install -r requirements.txt
```

3. Run the game server:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## 📁 Project Structure

```
question_game/
├── app.py              # Flask application
├── ai_model.py         # AI question generator and validator
├── requirements.txt   # Python dependencies
├── README.md          # This file
├── templates/
│   └── index.html     # Game UI HTML
└── static/
    ├── style.css      # Game styling
    └── script.js      # Game interaction logic
```

## 🎯 Features

- **Smart Question Validation**: Detects invalid questions
- **Contextual Responses**: AI generates relevant follow-up questions
- **Streak Tracking**: Track your progress with streak counters
- **Responsive Design**: Works on desktop and mobile
- **Visual Feedback**: Clear error messages and streak celebrations
- **Game Rules**: Built-in rules reference

## 💡 Tips for Playing

- Listen carefully to the AI's question
- Ask follow-up questions about the topic
- Try to connect your questions to create a conversation
- Have fun exploring different topics!

## 🔧 Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI**: Custom NLP-based question generation
- **Design**: Modern dark theme with smooth animations

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.