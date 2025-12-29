# Quick Start Guide

Get your Anki flashcard generator running in 5 minutes!

## Step 1: Install Python
Make sure Python 3.7+ is installed:
```bash
python --version
```

## Step 2: Clone & Install
```bash
git clone https://github.com/morteza-mogharrab/anki-ai-generator.git
cd anki-ai-generator
pip install -r requirements.txt
```

## Step 3: Set Up API Key
1. Get an OpenAI API key: https://platform.openai.com/api-keys
2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your key:
   ```
   OPENAI_API_KEY=sk-proj-your-actual-key-here
   ```

## Step 4: Prepare Your Vocabulary
Create `vocabulary.csv` (or rename `vocabulary_example.csv`):
```csv
Front,Source
serendipity,essential
ubiquitous,important
```

**Column meanings:**
- `Front`: Word or phrase to learn
- `Source`: Category (determines priority and audio)

## Step 5: Customize Categories (Optional)
Edit `anki_generator.py` function `get_deck_and_audio_rules()` to match your source categories.

Default categories:
- **High priority** (with audio): "essential", "priority", "important", "core"
- **Low priority** (no audio): "archive", "reference", "low", "deprecated"
- **Medium priority** (with audio): everything else

## Step 6: Run!
```bash
python anki_generator.py
```

## Step 7: Import to Anki
1. Open Anki Desktop
2. File → Import
3. Select `generated_deck.apkg`
4. Done! You'll see 3 sub-decks under "Flashcards"

## Troubleshooting

**"OPENAI_API_KEY not set"**
- Make sure `.env` file exists and contains your key
- Check there are no extra spaces around the key

**"CSV must have columns Front and Source"**
- Verify column headers are exactly: `Front,Source`
- No extra spaces in column names

**No audio in cards**
- Check if source category is set to generate audio
- Verify OpenAI TTS is enabled on your account
- Check error logs for specific issues

## What's Next?

- Read [README.md](README.md) for detailed configuration options
- Customize the system prompt for your learning style
- Adjust card styling in the CSS_STYLE variable
- Try different GPT models or TTS voices

## Cost Expectations

For 100 cards:
- GPT-4 generation: ~$0.30-0.50
- TTS audio: ~$0.15
- **Total**: ~$0.45-0.65

💡 Tip: Disable audio for low-priority cards to save costs!

## Need Help?

Check the full [README.md](README.md) or open an issue on GitHub.

Happy learning! 🎓
