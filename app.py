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

# Added the 5th secure random password profile to your collection
common_passwords = {
    "password123456": {"len": 14, "is_random": False, "desc": "Numbers following a simple password"},
    "admin123": {"len": 8, "is_random": False, "desc": "Standard router default"},
    "qwerty123": {"len": 9, "is_random": False, "desc": "Keyboard swipe mixed with simple counting"},
    "Pass@123": {"len": 8, "is_random": False, "desc": "Also has a capital letter and a special character, but it is still quite simple"},
    "xK9!vM2@pZ4#qR": {"len": 14, "is_random": True, "desc": "Google-Generated Suggestion. A super random password"}
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

# Format Theoretical Time
if theoretical_time_seconds < 60:
    theo_time_str = f"{theoretical_time_seconds:.2f} Seconds"
elif theoretical_time_seconds < 3600:
    theo_time_str = f"{theoretical_time_seconds/60:.2f} Minutes"
elif theoretical_time_seconds < 86400:
    theo_time_str = f"{theoretical_time_seconds/86400:.2f} Hours"
elif theoretical_time_seconds < 31536000:
    theo_time_str = f"{theoretical_time_seconds/86400:.2f} Days"
else:
    theo_time_str = f"{theoretical_time_seconds/31536000:.2e} Years"

# Logic processing actual times dynamically based on security traits
if pw_details["is_random"]:
    actual_time_str = theo_time_str
    actual_delta = "0% optimization (No short-cuts)"
    delta_col = "normal"
else:
    actual_time_str = "< 0.001 Seconds"
    actual_delta = "-100% immediate compromise"
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
        st.metric("Dictionary Database Rank", "Top 50 Most Leaked")
    st.metric("Actual Time to Crack", actual_time_str, delta=actual_delta, delta_color=delta_col)

st.markdown("---")

# --- SIMULATION ENGINE ---
st.header("Interactive Attack Timeline")
st.write("Run the simulator below to view how the attack engine handles this password type.")

if st.button("Execute Simulated Attack Profile"):
    if not pw_details["is_random"]:
        # Scenario A: Common vulnerable passwords
        with st.spinner("Running Dictionary Database Lookup..."):
            time.sleep(0.5)
        st.success(f"Target Breached! The password '{selected_pw}' was found instantly on step #1 of the Wordlist Dictionary check.")
        st.balloons()
    else:
        # Scenario B: Secure random password
        with st.spinner("Running Dictionary Database Lookup..."):
            time.sleep(0.8)
        st.error("Dictionary Attack Failed! Password is not in any leaked registries. Falling back to mathematical brute-force...")
        
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
