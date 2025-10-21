import streamlit as st
import json
import pandas as pd
from pathlib import Path

# Add custom CSS for larger fonts and better styling
st.markdown("""
    <style>
        /* Main title styling */
        .main-title {
            font-size: 42px !important;
            font-weight: bold;
            padding-bottom: 20px;
        }
        
        /* Subtitle styling */
        .subtitle {
            font-size: 40px !important;
            color: #666;
            padding-bottom: 30px;
        }
        
        /* Metric card styling */
        div[data-testid="stMetricValue"] {
            font-size: 36px !important;
            font-weight: bold !important;
        }
        
        div[data-testid="stMetricLabel"] {
            font-size: 50px !important;
            font-weight: 600 !important;
            color: #0066cc !important;
        }
        
        /* Add background and shadow to metric containers */
        [data-testid="stMetricValue"] > div {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
        
        /* Section headers */
        .section-header {
            font-size: 32px !important;
            font-weight: bold;
            padding: 20px 0;
        }
        
        /* DataFrame styling */
        .dataframe {
            font-size: 16px !important;
            font-weight: bold !important;
        }
        
        /* Style the table header */
        .dataframe thead th {
            font-size: 18px !important;
            font-weight: 800 !important;
            background-color: #0066cc !important;
            color: white !important;
            padding: 12px 5px !important;
        }
        
        /* Style table cells */
        .dataframe tbody td {
            font-size: 16px !important;
            font-weight: bold !important;
            padding: 8px !important;
            background-color: #f8f9fa !important;
        }
        
        /* Alternate row colors */
        .dataframe tbody tr:nth-child(odd) td {
            background-color: #ffffff !important;
        }
        
        /* Hover effect on rows */
        .dataframe tbody tr:hover td {
            background-color: #e6f3ff !important;
        }
        
        /* Download button */
        .stDownloadButton button {
            font-size: 18px !important;
            padding: 10px 20px;
        }
    </style>
""", unsafe_allow_html=True)

def load_results():
    # Get the absolute path to results.json in parent directory
    current_dir = Path(__file__).parent
    results_path = current_dir.parent / "results.json"
    
    try:
        if not results_path.exists():
            st.error(f"Results file not found at: {results_path}")
            st.info("Expected location: ../results.json")
            return None
            
        with open(results_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Could not find results.json in {results_path}")
        return None
    except json.JSONDecodeError:
        st.error("Invalid JSON format in results.json")
        return None

def analyze_costs(data):
    if not data:
        return None
    
    models = []
    costs = []
    latencies = []
    
    for prompt in data["results"]["prompts"]:
        models.append(prompt["provider"])
        costs.append(prompt["metrics"]["cost"])
        latencies.append(prompt["metrics"]["totalLatencyMs"])
    
    # Create initial DataFrame
    df = pd.DataFrame({
        "Model": models,
        "Cost per Request": costs,
        "Latency (ms)": latencies,
        "Monthly Cost (100K requests)": [c * 100000 for c in costs],
        "Yearly Cost (1.2M requests)": [c * 1200000 for c in costs]
    })
    
    # Calculate Cost Efficiency using new formula: Final Cost (×100K) / Latency
    df["Cost Efficiency"] = (df["Cost per Request"] * 100000) / df["Latency (ms)"]
    
    # Add Cost Efficiency Rank (lower is better)
    df["Efficiency Rank"] = df["Cost Efficiency"].rank()
    
    return df

def main():
    # Configure page to use wide layout
    st.set_page_config(layout="wide", page_title="AI Model Cost Analysis")
    
    st.title("🤖 AI Model Cost Analysis")
    st.write("Compare costs across different AI models")
    
    data = load_results()
    if data:
        df = analyze_costs(data)
        
        # Display metrics in 4 columns for better space usage
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Models", len(df))
        with col2:
            st.metric("Most Expensive Model", 
                     df.iloc[df["Cost per Request"].argmax()]["Model"])
        with col3:
            avg_cost = df["Monthly Cost (100K requests)"].mean()
            st.metric("Avg Monthly Cost", f"${avg_cost:,.2f}")

        with col4:
            total_yearly = df["Yearly Cost (1.2M requests)"].sum()
            st.metric("Total Yearly Cost", f"${total_yearly:,.2f}")
        
        # Cost comparison chart
        st.subheader("💰 Cost Comparison")
        chart_data = df.set_index("Model")
        st.bar_chart(chart_data["Monthly Cost (100K requests)"])
        
        # Detailed table with adjusted column width
        st.subheader("📊 Detailed Cost Analysis")
        st.dataframe(
            df.style
            .format({
                "Cost per Request": "${:,.4f}",
                "Latency (ms)": "{:,.0f}",
                "Monthly Cost (100K requests)": "${:,.2f}",
                "Yearly Cost (1.2M requests)": "${:,.2f}",
                "Cost Efficiency": "{:,.4f}",  # More decimal places for efficiency
                "Efficiency Rank": "{:.0f}"
            })
            .set_properties(**{
                'font-weight': 'bold',
                'text-align': 'right'
            })
            .set_table_styles([
                {'selector': 'th', 'props': [('font-weight', 'bold')]},
                {'selector': 'td', 'props': [('font-weight', 'bold')]}
            ]),
            use_container_width=True,
            height=300
        )
        
        # Download option
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Cost Analysis (CSV)",
            data=csv,
            file_name="ai_cost_analysis.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()