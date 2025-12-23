import streamlit as st
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# --- Page Configuration ---
st.set_page_config(
    page_title="P-Value Explorer",
    page_icon="📊",
    layout="wide"
)

# --- Custom Styling ---
st.markdown("""
<style>
    .metric-container {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .sig-result {
        color: #2e7d32;
        font-weight: bold;
        font-size: 24px;
    }
    .nonsig-result {
        color: #c62828;
        font-weight: bold;
        font-size: 24px;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Controls ---
st.sidebar.header("🧪 Experiment Parameters")

st.sidebar.markdown("Adjust these to see how they impact the P-value.")

n_samples = st.sidebar.slider(
    "Sample Size (per group)",
    min_value=5,
    max_value=200,
    value=30,
    step=1,
    help="Number of observations in each group (N)."
)

effect_size = st.sidebar.slider(
    "Magnitude of Effect (Mean Difference)",
    min_value=0.0,
    max_value=2.0,
    value=0.5,
    step=0.05,
    help="The difference between the Control and Treatment means."
)

std_dev = st.sidebar.slider(
    "Standard Deviation (Noise)",
    min_value=0.5,
    max_value=3.0,
    value=1.0,
    step=0.1,
    help="How spread out the data is. Higher noise makes effects harder to detect."
)

alpha = 0.05

# --- Main Content ---
st.title("📊 P-Value Visualizer")
st.markdown("""
This educational tool demonstrates the relationship between **Sample Size**, **Effect Size**, and the resulting **P-value**.
Adjust the sliders on the left to simulate an experiment comparing two groups (Control vs. Treatment).
""")

st.divider()

# --- Calculations ---
# 1. Generate Theoretical Data (for visualization)
x = np.linspace(-4, 6, 1000)
# Group A (Control): Mean = 0
y_control = stats.norm.pdf(x, 0, std_dev)
# Group B (Treatment): Mean = Effect Size
y_treatment = stats.norm.pdf(x, effect_size, std_dev)

# 2. Simulate Actual T-Test
# We simulate random sampling based on the user's parameters to get a real p-value
np.random.seed(42) # Fixed seed for stability while sliding, remove for pure random
group_control = np.random.normal(0, std_dev, n_samples)
group_treatment = np.random.normal(effect_size, std_dev, n_samples)

t_stat, p_val = stats.ttest_ind(group_control, group_treatment)

# --- Visualization ---

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("1. Visualizing the Populations")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot curves
    ax.plot(x, y_control, label='Control Group (Mean=0)', color='blue', linewidth=2)
    ax.fill_between(x, y_control, alpha=0.1, color='blue')
    
    ax.plot(x, y_treatment, label=f'Treatment Group (Mean={effect_size})', color='orange', linewidth=2)
    ax.fill_between(x, y_treatment, alpha=0.1, color='orange')
    
    # Plot means
    ax.axvline(0, color='blue', linestyle='--', alpha=0.5)
    ax.axvline(effect_size, color='orange', linestyle='--', alpha=0.5)
    
    # Annotations
    ax.set_title(f"Population Distributions (SD={std_dev})", fontsize=14)
    ax.set_xlabel("Value")
    ax.set_ylabel("Density")
    ax.legend()
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    st.pyplot(fig)

with col2:
    st.subheader("2. Statistical Result")
    
    # Determine result style
    is_sig = p_val < alpha
    result_text = "SIGNIFICANT" if is_sig else "NOT SIGNIFICANT"
    result_class = "sig-result" if is_sig else "nonsig-result"
    
    st.markdown(f"""
    <div class="metric-container">
        <p style="font-size: 16px; margin-bottom: 0;">Calculated P-Value:</p>
        <p style="font-size: 40px; font-weight: bold; margin: 10px 0;">{p_val:.4f}</p>
        <p class="{result_class}">{result_text}</p>
        <p style="font-size: 14px; color: gray;">(Threshold: p < 0.05)</p>
    </div>
    """, unsafe_allow_html=True)

    st.info(f"""
    **Current Stats:**
    * **N:** {n_samples}
    * **T-Statistic:** {t_stat:.2f}
    """)

# --- Educational Explanation ---
st.divider()
st.subheader("📝 Interpretation")

st.markdown(f"""
To detect a significant result ($p < 0.05$), you need to separate the signal from the noise.

1.  **Effect Size (The Signal):** You currently have a mean difference of **{effect_size}**. 
    * *Try increasing this:* As the peaks move further apart, the groups become distinct, and the p-value drops.
2.  **Sample Size (The Confidence):** You are using **{n_samples}** samples per group.
    * *Try increasing this:* Even if the effect size is small, a larger sample size makes the statistical test more "confident" that the difference is real, lowering the p-value.
3.  **Standard Deviation (The Noise):** You have a spread of **{std_dev}**.
    * *Try decreasing this:* Less overlap between the curves makes it easier to detect a difference.
""")

# Optional: Power visualization hint
if p_val > 0.05 and effect_size > 0:
    st.warning("⚠️ **Hint:** Your result is not significant yet. Try **increasing the sample size** or **increasing the effect magnitude** to drop the p-value below 0.05.")
elif p_val < 0.05:
    st.success("✅ **Success:** You have successfully detected a statistically significant difference!")
