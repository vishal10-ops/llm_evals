import json
import pandas as pd

# Load JSON data from file
with open("results.json", "r") as f:
    data = json.load(f)

# Extract relevant info
models = []
costs = []
latencies = []  

for prompt in data["results"]["prompts"]:
    model_name = prompt["provider"]
    cost = prompt["metrics"]["cost"]
    latency = prompt["metrics"]["totalLatencyMs"]  # Optional, if latency is recorded
    models.append(model_name)
    costs.append(cost)
    latencies.append(latency)  

# Create DataFrame
df = pd.DataFrame({
    "Model Name": models,
    "Cost": costs,
    "Latency(ms)": latencies
})

# Compute Final Cost (× 100K)
df["Final Cost (×100K)"] = df["Cost"] * 100000

# Compute Cost Efficiency = Final Cost / Quality Score
df["Cost Efficiency"] = df["Final Cost (×100K)"] / df["Latency(ms)"]

# Print results
print(df.to_string(index=False, float_format="%.3f"))

# Optionally, save to CSV
df.to_csv("model_cost_summary.csv", index=False, float_format="%.4f")

print("\n Summary with Cost Efficiency saved as model_cost_summary.csv")
