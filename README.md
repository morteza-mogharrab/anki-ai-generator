# AI-Powered Anki Flashcard Generator

Generate high-quality Anki flashcards automatically using OpenAI's GPT-4 and TTS. This tool creates cloze deletion cards with contextual examples, definitions, and optional audio pronunciation.

## Features

- 🤖 **AI-Generated Content**: Uses GPT-4 to create natural, contextual example sentences
- 🎯 **Cloze Deletions**: Automatically generates cloze deletion cards with hints
- 🔊 **Text-to-Speech**: Optional audio generation for pronunciation practice
- 📊 **Priority-Based Organization**: Automatically categorizes cards into 3 priority decks
- ⚡ **Parallel Processing**: Fast generation using multi-threading
- 💰 **Cost Optimization**: Skip audio for low-priority cards to save on API costs

## Priority Deck System

The generator creates three hierarchical decks:

1. **High Priority** (`01_High_Priority`): Essential items with audio
2. **Medium Priority** (`02_Medium_Priority`): Standard items with audio
3. **Low Priority** (`03_Low_Priority`): Archive/reference items without audio

## Prerequisites

- Python 3.7 or higher
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- Anki desktop application ([download here](https://apps.ankiweb.net/))

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/morteza-mogharrab/anki-ai-generator.git
   cd anki-ai-generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**:
   
   Create a `.env` file in the project directory:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

   Alternatively, set it as an environment variable:
   ```bash
   export OPENAI_API_KEY=your-api-key-here
   ```

## Usage

### 1. Prepare Your Vocabulary CSV

Create a CSV file named `vocabulary.csv` with two columns:

| Front | Source |
|-------|--------|
| serendipity | essential |
| ubiquitous | priority |
| ephemeral | reference |

**Column descriptions**:
- `Front`: The word or phrase to learn
- `Source`: Category/source that determines priority and audio generation

### 2. Customize Categorization (Optional)

Edit the `get_deck_and_audio_rules()` function in `anki_generator.py` to match your categories:

```python
def get_deck_and_audio_rules(source_name):
    src = str(source_name).lower().strip()
    
    # High priority - customize these keywords
    if any(keyword in src for keyword in ['essential', 'important', 'core']):
        return DECK_ESSENTIALS, True  # Generate audio
    
    # Low priority - customize these keywords
    if any(keyword in src for keyword in ['archive', 'reference', 'low']):
        return DECK_ARCHIVE, False  # Skip audio (save costs)
    
    # Medium priority - everything else
    return DECK_ENRICHMENT, True
```

### 3. Run the Generator

```bash
python anki_generator.py
```

The script will:
1. Load vocabulary from `vocabulary.csv`
2. Generate flashcards using GPT-4
3. Create audio files (if enabled for that category)
4. Package everything into `generated_deck.apkg`

### 4. Import to Anki

1. Open Anki
2. Click **File** → **Import**
3. Select `generated_deck.apkg`
4. Your cards will appear in three sub-decks under "Flashcards"

## Example Output

For the word "serendipity", the generator creates:

**Front of card**:
> Finding that café was pure {{c1::serendipity::happy accident}}

**Back of card**:
> Finding that café was pure **serendipity**
> 
> **Meaning**: The occurrence of fortunate events by chance
> 
> **Context**: Used in both formal and casual contexts to describe pleasant surprises
> 
> 🔊 [Audio pronunciation]

## Cost Estimation

Approximate costs per 100 cards (as of 2024):
- **GPT-4 content generation**: ~$0.30-0.50
- **TTS audio generation**: ~$0.15
- **Total per 100 cards**: ~$0.45-0.65

💡 **Tip**: Set low-priority categories to skip audio generation to reduce costs.

## Configuration Options

### Change Output Filename

In `anki_generator.py`:
```python
OUTPUT_PKG_NAME = "my_custom_deck.apkg"
```

### Change Input Filename

In `anki_generator.py` (inside `main()` function):
```python
input_file = "my_vocabulary.csv"
```

### Adjust GPT Model

In `anki_generator.py` (inside `process_row()` function):
```python
model="gpt-4o",  # or "gpt-4", "gpt-3.5-turbo"
```

### Change TTS Voice

In `anki_generator.py` (inside `process_row()` function):
```python
voice="alloy",  # Options: alloy, echo, fable, onyx, nova, shimmer
```

### Modify Card Styling

Edit the `CSS_STYLE` variable in `anki_generator.py` to customize appearance.

### Adjust System Prompt

Modify `SYSTEM_PROMPT` to change how GPT generates content:
- Add specific formatting requirements
- Change difficulty level
- Specify domain expertise (medical, business, etc.)

## Troubleshooting

### "OPENAI_API_KEY environment variable not set"
- Make sure you've created a `.env` file with your API key
- Or set the environment variable: `export OPENAI_API_KEY=your-key`

### "CSV must have columns: 'Front' and 'Source'"
- Verify your CSV has exactly these column headers
- Check for typos in column names

### Audio files not generating
- Verify your OpenAI account has TTS enabled
- Check API usage limits
- Review logs for specific error messages

### Cards not importing to Anki
- Make sure you're using Anki Desktop (not AnkiWeb browser)
- Check that the `.apkg` file isn't corrupted
- Try importing with a fresh Anki profile

## Project Structure

```
anki-ai-generator/
├── anki_generator.py      # Main script
├── vocabulary.csv         # Your input file (not in repo)
├── requirements.txt       # Python dependencies
├── .env.example          # Template for environment variables
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── temp_anki_audio/      # Generated audio files (temporary)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this for personal or commercial projects.

## Acknowledgments

- Built with [genanki](https://github.com/kerrickstaley/genanki) for Anki package generation
- Powered by [OpenAI API](https://platform.openai.com/)

## Support

If you encounter issues or have questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review existing [GitHub Issues](https://github.com/morteza-mogharrab/anki-ai-generator/issues)
3. Open a new issue with details about your problem

---

**Note**: This tool uses paid OpenAI API services. Monitor your usage to avoid unexpected costs.
