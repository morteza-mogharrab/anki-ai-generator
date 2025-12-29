# Repository Setup Summary

## What Was Changed

### 🔒 Security & Best Practices
1. **Removed hardcoded API key** - Now uses environment variables
2. **Added `.env.example`** - Template for users to add their own keys
3. **Created `.gitignore`** - Prevents committing sensitive files

### 🎯 Generalization
1. **Removed specific category names** (Golden 2000, etc.)
2. **Created customizable categorization function** - Easy to modify for any use case
3. **Simplified to 2-column CSV** - Just "Front" and "Source" columns
4. **Renamed output** - Generic "generated_deck.apkg" instead of specific name

### 📚 Documentation
1. **Comprehensive README.md** - Full documentation with examples
2. **QUICKSTART.md** - 5-minute setup guide
3. **CONTRIBUTING.md** - Guidelines for contributors
4. **Added code comments** - Better inline documentation

### 🛠️ Improvements
1. **Better error handling** - More informative error messages
2. **Clearer logging** - Easier to track progress
3. **Environment variable loading** - Using python-dotenv
4. **Example CSV** - Template file for users

## Files Created

```
anki-ai-generator/
├── anki_generator.py          # Main script (cleaned & generalized)
├── README.md                  # Full documentation
├── QUICKSTART.md              # Quick setup guide
├── CONTRIBUTING.md            # Contribution guidelines
├── LICENSE                    # MIT License
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variable template
├── .gitignore                # Git ignore rules
└── vocabulary_example.csv    # Example input file
```

## Key Changes in Code

### 1. API Key Management
**Before:**
```python
client = OpenAI(api_key="sk-proj-...")
```

**After:**
```python
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
```

### 2. Categorization Logic
**Before:**
```python
if any(x in src for x in ['golden', 'template', 'common verbs', ...]):
    return DECK_ESSENTIALS, True
```

**After:**
```python
high_priority_keywords = ['essential', 'priority', 'important', 'core']
if any(keyword in src for keyword in high_priority_keywords):
    return DECK_ESSENTIALS, True
```

Users can now easily customize these keywords!

### 3. Deck Naming
**Before:**
```python
DECK_ESSENTIALS = genanki.Deck(2059400101, 'English::01_Essentials')
```

**After:**
```python
DECK_ESSENTIALS = genanki.Deck(2059400101, 'Flashcards::01_High_Priority')
```

Generic naming suitable for any subject.

## How to Use

### First Time Setup
1. Download all files to a folder
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`
4. Add your OpenAI API key to `.env`
5. Create or rename `vocabulary_example.csv` to `vocabulary.csv`
6. Customize categorization keywords if needed
7. Run: `python anki_generator.py`

### Customization Points

**1. Change category keywords** (in `anki_generator.py`):
```python
def get_deck_and_audio_rules(source_name):
    # Modify these lists to match your CSV's Source column values
    high_priority_keywords = ['your', 'keywords', 'here']
    low_priority_keywords = ['archive', 'old', 'reference']
```

**2. Modify AI prompt** (in `anki_generator.py`):
```python
SYSTEM_PROMPT = """
Role: You are an expert [YOUR DOMAIN] coach.
...
"""
```

**3. Change deck names** (in `anki_generator.py`):
```python
DECK_ESSENTIALS = genanki.Deck(2059400101, 'YourSubject::01_Priority1')
```

**4. Adjust styling** (in `anki_generator.py`):
```python
CSS_STYLE = """
.card { 
    font-family: arial;
    font-size: 24px;
    /* Add your custom CSS here */
}
"""
```

## Publishing to GitHub

### Quick Steps:
```bash
# Initialize git
cd anki-ai-generator
git init

# Add files
git add .
git commit -m "Initial commit: AI-powered Anki flashcard generator"

# Create repo on GitHub, then:
git remote add origin https://github.com/morteza-mogharrab/anki-ai-generator.git
git branch -M main
git push -u origin main
```

### Recommended Repository Settings:
- **Description**: "AI-powered Anki flashcard generator using GPT-4 and TTS"
- **Topics**: python, anki, openai, flashcards, language-learning, spaced-repetition
- **License**: MIT (already included)

## Next Steps

1. **Test locally first** - Make sure everything works
2. **Update README** - Add your GitHub username to links
3. **Push to GitHub** - Follow steps above
4. **Add badges** - Stars, issues, license badges
5. **Write blog post** - Share your project!

## Support

If you have questions about the changes or need help customizing:
- Check the code comments
- Review QUICKSTART.md
- Read the full README.md
- The code is well-documented for easy modification

Good luck with your project! 🚀
