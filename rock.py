import streamlit as st
import random

# Sidebar with rules
with st.sidebar:
    st.header("🎮 How to Play")
    st.write("""
    **Game Rules:**
    - ✊ Rock beats ✌️ Scissors  
    - ✋ Paper beats ✊ Rock  
    - ✌️ Scissors beats ✋ Paper

    **First to win 2 rounds!**
    """)
    st.markdown("---")
    st.write("Built with Streamlit")

# Function to reset game state
def reset_game_state():
    st.session_state.game = {
        'player_score': 0,
        'computer_score': 0,
        'round': 1,
        'history': [],
        'last_round': None,
        'game_over': False
    }

# Initialize game state
if 'game' not in st.session_state:
    reset_game_state()

# Main game area
st.title("✊ ✋ ✌️ Rock-Paper-Scissors")

# Scoreboard
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #6e48aa 0%, #9d50bb 100%);
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    margin: 20px 0;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
">
    <h2 style="color: white; margin: 0;">SCOREBOARD</h2>
    <div style="display: flex; justify-content: center; gap: 50px;">
        <div>
            <h3 style="color: white; margin: 0;">YOU</h3>
            <h1 style="color: white; margin: 0; font-size: 3em;">{st.session_state.game['player_score']}</h1>
        </div>
        <div>
            <h3 style="color: white; margin: 0;">COMPUTER</h3>
            <h1 style="color: white; margin: 0; font-size: 3em;">{st.session_state.game['computer_score']}</h1>
        </div>
    </div>
    <p style="color: white; margin: 5px 0 0 0;">Round {st.session_state.game['round']}</p>
</div>
""", unsafe_allow_html=True)

# Define choices
choices = ["Rock", "Paper", "Scissors"]
emojis = {"Rock": "✊", "Paper": "✋", "Scissors": "✌️"}

# Game logic
def determine_winner(player, computer):
    if player == computer:
        return "Draw"
    elif (player == "Rock" and computer == "Scissors") or \
         (player == "Paper" and computer == "Rock") or \
         (player == "Scissors" and computer == "Paper"):
        return "Player"
    else:
        return "Computer"

# User input buttons
if not st.session_state.game['game_over']:
    st.subheader("Make your choice:")
    cols = st.columns(3)
    for idx, choice in enumerate(choices):
        if cols[idx].button(f"{emojis[choice]} {choice}"):
            computer_choice = random.choice(choices)
            result = determine_winner(choice, computer_choice)

            round_result = {
                'round': st.session_state.game['round'],
                'player': choice,
                'computer': computer_choice,
                'result': result
            }

            st.session_state.game['history'].append(round_result)
            st.session_state.game['last_round'] = round_result
            st.session_state.game['round'] += 1

            if result == "Player":
                st.session_state.game['player_score'] += 1
            elif result == "Computer":
                st.session_state.game['computer_score'] += 1

            # End game if someone reaches 2 wins
            if st.session_state.game['player_score'] == 2 or st.session_state.game['computer_score'] == 2:
                st.session_state.game['game_over'] = True

            st.rerun()  # ✅ NEW VERSION

# Show last round result
if st.session_state.game['last_round']:
    last = st.session_state.game['last_round']
    st.info(f"Round {last['round']} result: You chose {emojis[last['player']]} {last['player']}, "
            f"Computer chose {emojis[last['computer']]} {last['computer']} → "
            f"**{last['result']}** wins the round.")

# Game over message
if st.session_state.game['game_over']:
    winner = "You" if st.session_state.game['player_score'] > st.session_state.game['computer_score'] else "Computer"
    st.success(f"🎉 Game Over! **{winner} win the game!**")
    if st.button("Play Again"):
        reset_game_state()
        st.rerun()  # ✅ NEW VERSION

# Optional: show full history
with st.expander("📜 Game History"):
    for entry in st.session_state.game['history']:
        st.write(f"Round {entry['round']}: You - {entry['player']} | Computer - {entry['computer']} → {entry['result']} wins")
