# MUHAMMAD ALIF ARYAGUNA (24/536649/TK/59540) MODELING AND SIMULATION PROJECT!
import streamlit as st
import numpy as np
import pandas as pd
import time

st.set_page_config(page_title="Password Security Simulator", layout="wide")

st.title("Password Brute-Force & Vulnerability Countdown")
st.write("An interactive simulation that analyzes the predictability of human behavior and how it could impact cybersecurity.")
st.write("Made by Muhammad Alif Aryaguna (24/536649/TK/59540) of Information Engineering")

# SIDEBAR CONFIGURATION
st.sidebar.header("Attacker Settings")

attack_speed = st.sidebar.select_slider(
    "Hacker Guessing Speed (R) [Guesses/sec]",
    options=[1, 10, 100, 1000, 10000],
    value=10000,
    help="Number of variations an attacker's hardware can process every second."
)

st.sidebar.markdown("---")
st.sidebar.subheader("Character Pool Specifications")
st.sidebar.write("Using the full standard ASCII keyboard spectrum ($C = 94$):")
st.sidebar.markdown("""
* **Numbers:** 10
* **Lowercase letters:** 26
* **Uppercase letters:** 26
* **Special Characters:** 32 
  `!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~`
""")

st.header("Case Study: Human Predictability vs. True Randomness")
st.write("Select a password profile below to analyze how a 'Dictionary List' attack compares against a blind mathematical search.")

# EMPIRICAL MODELING: Updated with exact historical global rankings from major breach databases
common_passwords = {
    "123456": {
        "len": 6, 
        "is_random": False, 
        "leak_rank": 1,  
        "desc": "The #1 most common password globally for over a decade. Simple sequential numeric progression"
    },
    "admin": {
        "len": 5, 
        "is_random": False, 
        "leak_rank": 2, 
        "desc": "The ultimate universal default hardware credential, widely left unchanged by users and IT teams"
    },
    "qwerty": {
        "len": 6, 
        "is_random": False, 
        "leak_rank": 14,  
        "desc": "A basic left-to-right keyboard row pattern swipe across physical keys"
    },
    "Pass@123": {
        "len": 8, 
        "is_random": False, 
        "leak_rank": 9, 
        "desc": "A common 'augmented' strategy attempting to pass basic system requirements (Capital + Symbol)"
    },
    "xK9!vM2@pZ4#qR": {
        "len": 14, 
        "is_random": True, 
        "leak_rank": None, 
        "desc": "Google-Generated Suggestion. High-entropy, pure mathematical randomness with no human patterns"
    }
}

selected_pw = st.selectbox("Choose a password to attack:", list(common_passwords.keys()))
pw_details = common_passwords[selected_pw]

st.info(f"**Analysis:** '{selected_pw}' is {pw_details['len']} characters long. Pattern profile: {pw_details['desc']}.")

# --- MATH CALCULATIONS ---
C = 94
L = pw_details["len"]
search_space = C ** L
avg_attempts = search_space / 2
theoretical_time_seconds = avg_attempts / attack_speed

# Helper function to format giant seconds values neatly into readable strings
def format_time(seconds):
    if seconds < 0.001:
        return f"{seconds * 1000:.3f} Milliseconds"
    elif seconds < 60:
        return f"{seconds:.4f} Seconds"
    elif seconds < 3600:
        return f"{seconds/60:.2f} Minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} Hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.2f} Days"
    else:
        return f"{seconds/31536000:.2e} Years"

theo_time_str = format_time(theoretical_time_seconds)

# --- DYNAMIC ACTUAL TIME CALCULATION ENGINE ---
if pw_details["is_random"]:
    actual_time_seconds = theoretical_time_seconds
    actual_time_str = theo_time_str
    actual_delta = "0% optimization (No short-cuts available)"
    delta_col = "normal"
else:
    # EMPIRICAL LOOKUP: Actual time is calculated dynamically as: (Leak Rank Position) / (Attacker Speed)
    actual_time_seconds = pw_details["leak_rank"] / attack_speed
    actual_time_str = format_time(actual_time_seconds)
    
    # Calculates the order-of-magnitude acceleration factor over blind math
    time_saved_factor = theoretical_time_seconds / actual_time_seconds
    actual_delta = f"Accelerated by {time_saved_factor:.1e}x via Wordlist Indexing"
    delta_col = "inverse"

# Display Metrics
col1, col2 = st.columns(2)
with col1:
    st.subheader("Pure Brute-Force Math (Theoretical)")
    st.metric("Total Search Space ($C^L$)", f"{search_space:.2e} combinations")
    st.metric("Theoretical Time to Crack", theo_time_str)

with col2:
    st.subheader("Real-World Attack (Actual)")
    if pw_details["is_random"]:
        st.metric("Dictionary Database Rank", "Not Found (Unique)")
    else:
        st.metric("Dictionary Database Rank", f"Global Rank #{pw_details['leak_rank']} inside Wordlist")
        
    st.metric("Actual Time to Crack", actual_time_str, delta=actual_delta, delta_color=delta_col)

st.markdown("---")

# --- SIMULATION ENGINE ---
st.header("Interactive Attack Timeline")
st.write("Run the simulator below to view how the attack engine handles this password type.")

if st.button("Execute Simulated Attack Profile"):
    if not pw_details["is_random"]:
        with st.spinner("Running Optimized Wordlist Database Stream Lookup..."):
            time.sleep(0.6)
        st.success(f"Target Breached! The password '{selected_pw}' was matched at row index position #{pw_details['leak_rank']} of the database file.")
        st.balloons()
    else:
        with st.spinner("Running Optimized Wordlist Database Stream Lookup..."):
            time.sleep(0.8)
        st.error("Dictionary Attack Failed! Password is not indexed in any leaked registries. Falling back to mathematical brute-force...")
        
    st.markdown("### How your system data looks under a blind random fallback search:")
    
    progress_bar = st.progress(0.0)
    status_text = st.empty()
    chart_placeholder = st.empty()
    
    attempts_history = []
    time_steps = []
    current_attempts = 0
    start_time = time.time()
    
    # Visualizing a slice of the search timeline
    for step in range(1, 41):
        time.sleep(0.04)
        current_attempts += (attack_speed * 0.04) * np.random.uniform(0.85, 1.15)
        
        attempts_history.append(current_attempts)
        time_steps.append(time.time() - start_time)
        
        progress_percentage = step / 40
        progress_bar.progress(progress_percentage)
        
        if pw_details["is_random"]:
            status_text.text(f"Brute-Forcing: Checked {int(current_attempts):,} combinations. Total progress: {current_attempts/search_space:.2e}%")
        else:
            status_text.text(f"Blind Search Mode Fallback: Checked {int(current_attempts):,} out of {search_space:.1e} combinations...")
        
        df_chart = pd.DataFrame({"Elapsed Time (s)": time_steps, "Combinations Evaluated": attempts_history})
        chart_placeholder.line_chart(df_chart.set_index("Elapsed Time (s)"))
        
    if pw_details["is_random"]:
        st.success(f"Security Verified! At your current hardware speed, this Google-generated password will remain uncracked for the next {theo_time_str}.")
    else:
        st.warning("Notice the difference: Blindly traversing the math space would take an eternity, but because humans choose predictable words, attackers compromise the account immediately using dictionary lookups.")
