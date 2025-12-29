"""
Anki Flashcard Generator with AI
Creates Anki decks with cloze deletions, definitions, and optional audio using OpenAI API.
"""

import pandas as pd
import genanki
import json
import os
import time
import logging
import re
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================
# SETUP & CONFIGURATION
# ============================================================

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

# Directory to temporarily store generated MP3s
AUDIO_DIR = Path("temp_anki_audio")
AUDIO_DIR.mkdir(exist_ok=True)

# Output Filename
OUTPUT_PKG_NAME = "generated_deck.apkg"

# Initialize OpenAI Client
# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set. Please set it before running.")

client = OpenAI(api_key=api_key)

# ============================================================
# DECK DEFINITIONS
# ============================================================

# Three priority-based decks organized hierarchically
DECK_ESSENTIALS = genanki.Deck(2059400101, 'Flashcards::01_High_Priority')
DECK_ENRICHMENT = genanki.Deck(2059400102, 'Flashcards::02_Medium_Priority')
DECK_ARCHIVE = genanki.Deck(2059400103, 'Flashcards::03_Low_Priority')

# ============================================================
# ANKI MODEL (CSS & Layout)
# ============================================================

MODEL_ID = 1607392319

CSS_STYLE = """
.card { 
    font-family: arial; 
    font-size: 24px; 
    text-align: center; 
    color: black; 
    background-color: white; 
}
.cloze { 
    font-weight: bold; 
    color: #007bff; 
}
.nightMode .cloze { 
    color: #5dade2; 
}
.extra { 
    font-size: 18px; 
    color: #555; 
    margin-top: 20px; 
}
.source-tag { 
    font-size: 12px; 
    color: #aaa; 
    margin-top: 40px; 
}
"""

my_cloze_model = genanki.Model(
    MODEL_ID,
    'AI Cloze Flashcard',
    fields=[
        {'name': 'Text'},
        {'name': 'Extra'},
        {'name': 'Audio'},
        {'name': 'Source'}
    ],
    templates=[{
        'name': 'Cloze Card',
        'qfmt': '{{cloze:Text}}',
        'afmt': '{{cloze:Text}}<br><div class="extra">{{Extra}}</div><br>{{Audio}}<div class="source-tag">{{Source}}</div>',
    }],
    css=CSS_STYLE,
    model_type=genanki.Model.CLOZE
)

# ============================================================
# CATEGORIZATION LOGIC
# ============================================================

def get_deck_and_audio_rules(source_name):
    """
    Determines the target deck and whether to generate audio based on source.
    
    Customize this function to match your categorization needs.
    
    Args:
        source_name (str): The value from the 'Source' column
        
    Returns:
        tuple: (Deck_Object, Generate_Audio_Boolean)
        
    Examples:
        - High priority items get audio and go to DECK_ESSENTIALS
        - Medium priority items get audio and go to DECK_ENRICHMENT
        - Low priority items skip audio (save costs) and go to DECK_ARCHIVE
    """
    src = str(source_name).lower().strip()
    
    # HIGH PRIORITY - Categories that need audio and are most important
    # Customize these keywords for your use case
    high_priority_keywords = ['essential', 'priority', 'important', 'core']
    if any(keyword in src for keyword in high_priority_keywords):
        return DECK_ESSENTIALS, True  # True = Generate Audio
    
    # LOW PRIORITY - Archive/reference material, skip audio to save costs
    # Customize these keywords for your use case
    low_priority_keywords = ['archive', 'reference', 'low', 'deprecated']
    if any(keyword in src for keyword in low_priority_keywords):
        return DECK_ARCHIVE, False  # False = Skip Audio
    
    # MEDIUM PRIORITY - Everything else gets audio
    return DECK_ENRICHMENT, True

# ============================================================
# AI PROMPT
# ============================================================

SYSTEM_PROMPT = """
Role: You are an expert language learning coach.

Task: I will give you a term/phrase and its source context.

Instructions:
1. ANALYZE the term based on its context
2. CREATE a natural, contextual cloze deletion sentence
3. PROVIDE a clear definition and usage context

Output Format (JSON Only):
{
  "anki_text": "Full sentence with {{c1::target term::hint}}.",
  "anki_extra": "<b>Meaning:</b> [Definition]<br><b>Context:</b> [Usage context]",
  "audio_script": "The full sentence written naturally for text-to-speech.",
  "tags": "tag1 tag2 tag3"
}

Guidelines:
- Make sentences natural and memorable
- Use appropriate difficulty level
- Include helpful hints in the cloze deletion
- Keep definitions concise but complete
"""

# ============================================================
# WORKER FUNCTION
# ============================================================

def process_row(args):
    """
    Processes a single vocabulary item: generates content and audio.
    Runs in a separate thread for parallel processing.
    
    Args:
        args: tuple of (index, word, source, should_generate_audio)
        
    Returns:
        dict: Processed flashcard data or None if error
    """
    idx, word, source, should_gen_audio = args
    
    # 1. Generate content using GPT
    try:
        user_content = f"Term: '{word}'. Context/Source: '{source}'"
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
    except Exception as e:
        logger.error(f"GPT Error on '{word}': {e}")
        return None
    
    # 2. Generate audio if enabled for this category
    audio_filename = ""
    audio_path = None
    
    if should_gen_audio:
        try:
            # Create safe filename
            safe_word = re.sub(r'[^a-zA-Z0-9]', '', word[:10])
            audio_filename = f"audio_{idx}_{safe_word}.mp3"
            audio_path = AUDIO_DIR / audio_filename
            
            # Generate TTS audio
            tts_response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=data['audio_script']
            )
            tts_response.stream_to_file(audio_path)
            
        except Exception as e:
            logger.error(f"TTS Error on '{word}': {e}")
            # Continue without audio rather than failing
            audio_filename = ""
    
    return {
        "text": data['anki_text'],
        "extra": data['anki_extra'],
        "tags": data['tags'].split(),
        "audio_file_name": audio_filename,
        "audio_path": str(audio_path) if audio_path else None,
        "source_original": source
    }

# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    """
    Main function that orchestrates the flashcard generation process.
    """
    input_file = "vocabulary.csv"
    
    # 1. Load and validate data
    try:
        df = pd.read_csv(input_file)
        
        # Ensure required columns exist
        if "Front" not in df.columns or "Source" not in df.columns:
            logger.error("CSV must have columns: 'Front' and 'Source'")
            logger.error("Found columns: " + ", ".join(df.columns))
            return
        
        # Filter valid rows (non-empty Front values)
        rows = []
        for idx, row in df.iterrows():
            word = str(row["Front"]).strip()
            source = str(row["Source"]).strip()
            
            if word.lower() != "nan" and word != "":
                rows.append((idx, word, source))
        
        logger.info(f"Loaded {len(rows)} items to process from {input_file}")
        
    except FileNotFoundError:
        logger.error(f"Could not find {input_file}. Please create a CSV with 'Front' and 'Source' columns.")
        return
    except Exception as e:
        logger.error(f"Error reading CSV: {e}")
        return
    
    # 2. Process items in parallel using threads
    futures_map = {}
    media_files = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        for r in rows:
            idx, word, source = r
            
            # Determine target deck and audio policy
            target_deck, gen_audio_flag = get_deck_and_audio_rules(source)
            
            # Submit processing task
            future = executor.submit(process_row, (idx, word, source, gen_audio_flag))
            
            # Track which deck each task belongs to
            futures_map[future] = target_deck
        
        # Collect results as they complete
        for i, future in enumerate(as_completed(futures_map)):
            result = future.result()
            target_deck = futures_map[future]
            
            if result:
                # Add audio file if generated
                if result['audio_path']:
                    media_files.append(result['audio_path'])
                
                # Format audio field for Anki
                audio_field = f"[sound:{result['audio_file_name']}]" if result['audio_file_name'] else ""
                
                # Create Anki note
                note = genanki.Note(
                    model=my_cloze_model,
                    fields=[
                        result['text'],
                        result['extra'],
                        audio_field,
                        result['source_original']
                    ],
                    tags=result['tags']
                )
                target_deck.add_note(note)
            
            # Progress logging
            if (i + 1) % 10 == 0:
                logger.info(f"Processed {i + 1}/{len(rows)} items...")
    
    # 3. Create final Anki package
    logger.info("Creating Anki package...")
    
    package = genanki.Package([DECK_ESSENTIALS, DECK_ENRICHMENT, DECK_ARCHIVE])
    package.media_files = media_files
    package.write_to_file(OUTPUT_PKG_NAME)
    
    logger.info(f"✅ SUCCESS! Generated {OUTPUT_PKG_NAME}")
    logger.info(f"   - Total cards: {len(rows)}")
    logger.info(f"   - Audio files: {len(media_files)}")
    logger.info(f"   - Import this file into Anki to see your 3 priority-based decks")

if __name__ == "__main__":
    main()
