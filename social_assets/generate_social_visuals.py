import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Styling for social / publication graphics
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'figure.dpi': 300,
    'savefig.dpi': 300
})

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir, "data", "laipi_developing_panel_2000_2023.csv")
out_dir = os.path.join(base_dir, "social_assets")

df = pd.read_csv(data_path)

# 1. CHART 1: The AI Adaptation Capacity Paradox Visualizer
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5.2), gridspec_kw={'width_ratios': [1, 1]})

terciles = ['Low Human Capital\n(Bottom 33%)', 'Middle Human Capital\n(Middle 33%)', 'High Human Capital\n(Top 33%)']
potentials = [0.7714, 0.5633, 0.2451]
readiness = [0.142, 0.308, 0.525]
realized = [0.1093, 0.1736, 0.1287]

x = np.arange(len(terciles))
width = 0.35

# Panel A: Potential Return vs Baseline Readiness
ax1.bar(x - width/2, potentials, width, label='Marginal Potential (β)', color='#e63946', alpha=0.9)
ax1.bar(x + width/2, readiness, width, label='Baseline Readiness (Mean AIPI)', color='#457b9d', alpha=0.9)
ax1.set_ylabel('Index / Coefficient Value')
ax1.set_title('(A) The Potential vs. Readiness Divergence', fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(terciles, fontsize=9.5)
ax1.legend(frameon=True, facecolor='#f8f9fa')
ax1.grid(axis='y', linestyle=':', alpha=0.6)

# Panel B: Realized Protection
bars = ax2.bar(terciles, realized, color=['#e63946', '#2a9d8f', '#1d3557'], width=0.5, alpha=0.85)
ax2.set_ylabel('Realized Protection (β × Baseline Readiness)')
ax2.set_title('(B) Realized Resilience Capacity', fontweight='bold')
ax2.grid(axis='y', linestyle=':', alpha=0.6)

# Add value labels
for bar in bars:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.005, f'+{yval:.4f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.suptitle('The AI Adaptation Capacity Paradox (Ubabukoh, 2026)', fontsize=14, fontweight='bold', y=0.98)
plt.tight_layout()
p1_path = os.path.join(out_dir, "capacity_paradox_visualizer.png")
fig.savefig(p1_path, bbox_inches='tight', dpi=300)
plt.close(fig)
print(f"Generated: {p1_path}")

# 2. CHART 2: Exemplar 2000-2023 Trajectories
fig, ax = plt.subplots(figsize=(10, 5.8))
exemplars = {
    'China': ('#d62828', '-'),
    'India': ('#f77f00', '-'),
    'Vietnam': ('#fcbf49', '--'),
    'Brazil': ('#2a9d8f', '-'),
    'South Africa': ('#264653', '-.'),
    'Kenya': ('#0077b6', '-'),
    'Nigeria': ('#023e8a', ':'),
    'Ethiopia': ('#6c757d', ':')
}

for country, (col, lstyle) in exemplars.items():
    c_df = df[df['country_name'] == country].sort_values('year')
    if not c_df.empty:
        ax.plot(c_df['year'], c_df['laipi_composite'], label=country, color=col, linestyle=lstyle, lw=2.2)

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Longitudinal AI Preparedness Index (L-AIPI)', fontsize=12)
ax.set_title('AI Preparedness Expansion across Key Developing Economies (2000–2023)', fontsize=13, fontweight='bold')
ax.set_ylim(0, 0.75)
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper left', ncol=2, frameon=True, facecolor='#f8f9fa', fontsize=10)

plt.tight_layout()
p2_path = os.path.join(out_dir, "country_trajectories_2000_2023.png")
fig.savefig(p2_path, bbox_inches='tight', dpi=300)
plt.close(fig)
print(f"Generated: {p2_path}")
