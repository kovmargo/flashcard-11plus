import streamlit as st
import random
import json

# Page configuration
st.set_page_config(
    page_title="English Flashcards - 11+",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for better iPad experience
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        margin: 5px 0;
    }
    .card-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 60px;
        text-align: center;
        color: white;
        min-height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'current_deck' not in st.session_state:
    st.session_state.current_deck = None
if 'current_card' not in st.session_state:
    st.session_state.current_card = 0
if 'is_flipped' not in st.session_state:
    st.session_state.is_flipped = False
if 'score' not in st.session_state:
    st.session_state.score = {'correct': 0, 'incorrect': 0}
if 'study_mode' not in st.session_state:
    st.session_state.study_mode = 'flip'
if 'shuffled_cards' not in st.session_state:
    st.session_state.shuffled_cards = []

# Initialize custom decks in session state
if 'custom_decks' not in st.session_state:
    st.session_state.custom_decks = {}

# Default flashcard decks
DEFAULT_DECKS = {
    "Advanced Vocabulary": {
        "category": "Vocabulary",
        "color": "blue",
        "cards": [
            {"word": "Eloquent", "definition": "Fluent and persuasive in speaking or writing", 
             "example": "Her eloquent speech moved the audience to tears."},
            {"word": "Meticulous", "definition": "Showing great attention to detail; very careful", 
             "example": "The scientist was meticulous in recording every observation."},
            {"word": "Ubiquitous", "definition": "Present, appearing, or found everywhere", 
             "example": "Mobile phones have become ubiquitous in modern society."},
            {"word": "Ephemeral", "definition": "Lasting for a very short time", 
             "example": "The beauty of cherry blossoms is ephemeral, lasting only weeks."},
            {"word": "Ambiguous", "definition": "Open to more than one interpretation; unclear", 
             "example": "The politician's ambiguous statement confused voters."}
        ]
    },
    "Literary Devices": {
        "category": "English Literature",
        "color": "purple",
        "cards": [
            {"word": "Metaphor", "definition": "A figure of speech comparing two unlike things without using 'like' or 'as'", 
             "example": "Time is a thief (time isn't literally a thief)."},
            {"word": "Alliteration", "definition": "Repetition of the same sound at the start of words", 
             "example": "Peter Piper picked a peck of pickled peppers."},
            {"word": "Personification", "definition": "Giving human qualities to non-human things", 
             "example": "The wind whispered through the trees."},
            {"word": "Hyperbole", "definition": "Exaggerated statements not meant to be taken literally", 
             "example": "I've told you a million times!"},
            {"word": "Simile", "definition": "A comparison using 'like' or 'as'", 
             "example": "She was as brave as a lion."}
        ]
    },
    "Grammar Terms": {
        "category": "Grammar",
        "color": "green",
        "cards": [
            {"word": "Subordinate Clause", "definition": "A clause that cannot stand alone as a complete sentence", 
             "example": "Although it was raining (subordinate), we went outside (main)."},
            {"word": "Active Voice", "definition": "When the subject performs the action", 
             "example": "The cat chased the mouse (the cat does the action)."},
            {"word": "Passive Voice", "definition": "When the subject receives the action", 
             "example": "The mouse was chased by the cat (mouse receives action)."},
            {"word": "Conjunction", "definition": "A word used to connect clauses or sentences", 
             "example": "I wanted to go, but it was too late (but is the conjunction)."},
            {"word": "Adverb", "definition": "A word that modifies a verb, adjective, or other adverb", 
             "example": "She ran quickly (quickly modifies the verb ran)."}
        ]
    }
}

# Get all decks (default + custom)
def get_all_decks():
    return {**DEFAULT_DECKS, **st.session_state.custom_decks}

# Helper functions
def start_study(deck_name, mode):
    all_decks = get_all_decks()
    st.session_state.current_deck = deck_name
    st.session_state.study_mode = mode
    st.session_state.current_card = 0
    st.session_state.is_flipped = False
    st.session_state.score = {'correct': 0, 'incorrect': 0}
    
    cards = all_decks[deck_name]['cards'].copy()
    if mode == 'shuffle':
        random.shuffle(cards)
    st.session_state.shuffled_cards = cards
    st.session_state.view = 'study'

def flip_card():
    st.session_state.is_flipped = not st.session_state.is_flipped

def next_card(correct=None):
    if correct is not None:
        if correct:
            st.session_state.score['correct'] += 1
        else:
            st.session_state.score['incorrect'] += 1
    
    if st.session_state.current_card < len(st.session_state.shuffled_cards) - 1:
        st.session_state.current_card += 1
        st.session_state.is_flipped = False
    else:
        st.session_state.view = 'results'

def prev_card():
    if st.session_state.current_card > 0:
        st.session_state.current_card -= 1
        st.session_state.is_flipped = False

def go_home():
    st.session_state.view = 'home'
    st.session_state.current_deck = None

def restart():
    deck_name = st.session_state.current_deck
    mode = st.session_state.study_mode
    start_study(deck_name, mode)

def add_custom_deck(deck_name, category, color, cards):
    st.session_state.custom_decks[deck_name] = {
        "category": category,
        "color": color,
        "cards": cards
    }

def delete_custom_deck(deck_name):
    if deck_name in st.session_state.custom_decks:
        del st.session_state.custom_decks[deck_name]

# Main app
st.title("📚 English Flashcards - 11+ Learning")

# Sidebar for managing decks
with st.sidebar:
    st.header("⚙️ Manage Decks")
    
    menu = st.radio("Menu", ["🏠 Study Decks", "➕ Add New Deck", "✏️ Edit Cards"])
    
    if menu == "➕ Add New Deck":
        st.subheader("Create New Deck")
        
        new_deck_name = st.text_input("Deck Name", placeholder="My Custom Deck")
        new_category = st.text_input("Category", placeholder="e.g., Vocabulary, Science")
        new_color = st.selectbox("Color Theme", ["blue", "purple", "green", "red", "orange", "pink"])
        
        st.markdown("---")
        st.markdown("**Add Cards to Your Deck:**")
        
        num_cards = st.number_input("How many cards?", min_value=1, max_value=20, value=3)
        
        cards_list = []
        for i in range(num_cards):
            st.markdown(f"**Card {i+1}:**")
            word = st.text_input(f"Word/Term {i+1}", key=f"word_{i}")
            definition = st.text_area(f"Definition {i+1}", key=f"def_{i}")
            example = st.text_area(f"Example {i+1}", key=f"ex_{i}")
            
            if word and definition:
                cards_list.append({
                    "word": word,
                    "definition": definition,
                    "example": example if example else "No example provided."
                })
            st.markdown("---")
        
        if st.button("💾 Save New Deck", use_container_width=True):
            if new_deck_name and cards_list:
                add_custom_deck(new_deck_name, new_category, new_color, cards_list)
                st.success(f"✅ Deck '{new_deck_name}' created with {len(cards_list)} cards!")
                st.balloons()
            else:
                st.error("Please provide a deck name and at least one complete card.")
    
    elif menu == "✏️ Edit Cards":
        st.subheader("Edit Existing Decks")
        
        all_decks = get_all_decks()
        
        if st.session_state.custom_decks:
            deck_to_edit = st.selectbox("Select Deck to Edit/Delete", 
                                       list(st.session_state.custom_decks.keys()))
            
            if deck_to_edit:
                deck_data = st.session_state.custom_decks[deck_to_edit]
                
                st.markdown(f"**{deck_to_edit}**")
                st.markdown(f"Category: {deck_data['category']}")
                st.markdown(f"Cards: {len(deck_data['cards'])}")
                
                if st.button("🗑️ Delete This Deck", use_container_width=True):
                    delete_custom_deck(deck_to_edit)
                    st.success(f"Deleted '{deck_to_edit}'")
                    st.rerun()
                
                st.markdown("---")
                st.markdown("**Cards in this deck:**")
                for idx, card in enumerate(deck_data['cards']):
                    with st.expander(f"Card {idx+1}: {card['word']}"):
                        st.write(f"**Definition:** {card['definition']}")
                        st.write(f"**Example:** {card['example']}")
        else:
            st.info("No custom decks yet. Create one in 'Add New Deck'!")

# Home View
if st.session_state.view == 'home':
    st.markdown("### Choose Your Deck")
    
    all_decks = get_all_decks()
    
    # Create columns dynamically based on number of decks
    num_decks = len(all_decks)
    cols = st.columns(min(3, num_decks))
    
    for idx, (deck_name, deck_data) in enumerate(all_decks.items()):
        with cols[idx % 3]:
            # Show custom badge for custom decks
            if deck_name in st.session_state.custom_decks:
                st.markdown("🌟 **CUSTOM DECK**")
            
            st.markdown(f"#### {deck_name}")
            st.markdown(f"**Category:** {deck_data['category']}")
            st.markdown(f"**Cards:** {len(deck_data['cards'])}")
            
            if st.button(f"📖 Study Mode", key=f"study_{deck_name}"):
                start_study(deck_name, 'flip')
                st.rerun()
            
            if st.button(f"✅ Quiz Mode", key=f"quiz_{deck_name}"):
                start_study(deck_name, 'quiz')
                st.rerun()
            
            if st.button(f"🔀 Shuffle Mode", key=f"shuffle_{deck_name}"):
                start_study(deck_name, 'shuffle')
                st.rerun()
            
            st.markdown("---")

# Study View
elif st.session_state.view == 'study':
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Back to Decks"):
            go_home()
            st.rerun()
    
    with col2:
        st.markdown(f"### {st.session_state.current_deck}")
    
    with col3:
        total_cards = len(st.session_state.shuffled_cards)
        current = st.session_state.current_card + 1
        st.markdown(f"**Card {current} / {total_cards}**")
    
    if st.session_state.study_mode == 'quiz':
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"✓ Correct: {st.session_state.score['correct']}")
        with col2:
            st.error(f"✗ Incorrect: {st.session_state.score['incorrect']}")
    
    st.markdown("---")
    
    # Card display
    card = st.session_state.shuffled_cards[st.session_state.current_card]
    
    if not st.session_state.is_flipped:
        st.markdown(f"""
        <div class="card-container">
            <h4 style='opacity: 0.8; font-size: 14px; text-transform: uppercase;'>WORD</h4>
            <h1 style='font-size: 48px; margin: 30px 0;'>{card['word']}</h1>
            <p style='font-size: 18px; opacity: 0.9;'>👆 Tap 'Flip Card' to reveal definition</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="card-container">
            <h4 style='opacity: 0.8; font-size: 14px; text-transform: uppercase;'>DEFINITION</h4>
            <h2 style='font-size: 28px; margin: 20px 0;'>{card['definition']}</h2>
            <div style='background: rgba(255,255,255,0.2); padding: 20px; border-radius: 10px; margin-top: 30px;'>
                <h4 style='opacity: 0.8; font-size: 14px; text-transform: uppercase;'>EXAMPLE</h4>
                <p style='font-size: 18px; font-style: italic;'>{card['example']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("⬅️ Previous", disabled=(st.session_state.current_card == 0)):
            prev_card()
            st.rerun()
    
    with col2:
        if st.button("🔄 Flip Card"):
            flip_card()
            st.rerun()
    
    if st.session_state.study_mode == 'quiz' and st.session_state.is_flipped:
        with col3:
            if st.button("❌ Incorrect"):
                next_card(correct=False)
                st.rerun()
        with col4:
            if st.button("✅ Correct"):
                next_card(correct=True)
                st.rerun()
    else:
        with col3:
            pass
        with col4:
            is_last = st.session_state.current_card == len(st.session_state.shuffled_cards) - 1
            if st.button("Finish ✓" if is_last else "Next ➡️"):
                next_card()
                st.rerun()

# Results View
elif st.session_state.view == 'results':
    st.markdown("## 🏆 Deck Complete!")
    
    if st.session_state.study_mode == 'quiz':
        total = st.session_state.score['correct'] + st.session_state.score['incorrect']
        percentage = (st.session_state.score['correct'] / total * 100) if total > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h2 style='font-size: 48px; margin: 0;'>{st.session_state.score['correct']}</h2>
                <p>Correct</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h2 style='font-size: 48px; margin: 0;'>{st.session_state.score['incorrect']}</h2>
                <p>Incorrect</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h2 style='font-size: 48px; margin: 0;'>{percentage:.0f}%</h2>
                <p>Score</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Study Again", use_container_width=True):
            restart()
            st.rerun()
    
    with col2:
        if st.button("🏠 Back to Decks", use_container_width=True):
            go_home()
            st.rerun()
