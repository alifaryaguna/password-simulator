# MUHAMMAD ALIF ARYAGUNA (24/536649/TK/59540) MODELING AND SIMULATION PROJECT!
import streamlit as st
import numpy as np
import pandas as pd
import time

st.set_page_config(page_title="Password Security Simulator", layout="wide")

st.title("Password Brute-Force & Vulnerability Countdown")
st.write("An interactive simulation that analyzes the predictability of human behavior and how it could impact cybersecurity.")

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

st.header("Case Study: The use of common passwords")
st.write("Select a notoriously weak, common password to analyze. Watch how a 'Dictionary List' attack bypasses standard combinatorial math completely.")

common_passwords = {
    "password123456": {"len": 14, "desc": "Numbers following a simple password"},
    "admin123": {"len": 8, "desc": "Standard router default"},
    "qwerty123": {"len": 9, "desc": "Keyboard swipe mixed with simple counting"},
    "Pass@123": {"len": 8, "desc": "Also has a capital letter and a special charactr, but it is still quite simple"}
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
    theo_time_str = f"{theoretical_time_seconds/3600:.2f} Hours"
elif theoretical_time_seconds < 31536000:
    theo_time_str = f"{theoretical_time_seconds/86400:.2f} Days"
else:
    theo_time_str = f"{theoretical_time_seconds/31536000:.2f} Years"

# Display Metrics
col1, col2 = st.columns(2)
with col1:
    st.subheader("Pure Brute-Force Math (If completely random)")
    st.metric("Total Search Space ($C^L$)", f"{search_space:.2e} combinations")
    st.metric("Theoretical Time to Crack", theo_time_str)

with col2:
    st.subheader("Real-World Dictionary Attack (Actual Speed)")
    st.metric("Dictionary Database Rank", "Top 50 Most Leaked")
    st.metric("Actual Time to Crack", "< 0.001 Seconds", delta="-100% immediate compromise", delta_color="inverse")

st.markdown("---")

# --- SIMULATION ENGINE ---
st.header("Interactive Attack Timeline")
st.write("Run the simulator below to contrast the live calculation stream vs. an immediate dictionary lookup match.")

if st.button("Execute Simulated Attack Profile"):
    # Simulated quick execution due to dictionary check
    with st.spinner("Initializing Wordlist Database Optimization..."):
        time.sleep(0.6)
        
    st.success(f"Target Breached! The password '{selected_pw}' was found on step #1 of the Wordlist Dictionary check.")
    st.balloons()
    
    st.markdown("### How your system data looks under a blind random fallback search:")
    
    # Run a comparative random search visualization to show what blind mathematical traversal looks like
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
        # Stochastic growth step
        current_attempts += (attack_speed * 0.04) * np.random.uniform(0.85, 1.15)
        
        attempts_history.append(current_attempts)
        time_steps.append(time.time() - start_time)
        
        progress_percentage = step / 40
        progress_bar.progress(progress_percentage)
        
        status_text.text(f"Blind Search Mode: Checked {int(current_attempts):,} out of {search_space:.1e} combinations...")
        
        df_chart = pd.DataFrame({"Elapsed Time (s)": time_steps, "Combinations Evaluated": attempts_history})
        chart_placeholder.line_chart(df_chart.set_index("Elapsed Time (s)"))
        
    st.warning("Notice the difference: Blindly traversing the math space would take an eternity, but because humans choose predictable words, attackers compromise the account immediately using dictionary lookups.")
