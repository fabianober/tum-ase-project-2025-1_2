










import pandas as pd
import matplotlib.pyplot as plt
import ast
from matplotlib.widgets import Button

plt.style.use('seaborn-v0_8-colorblind')

CSV_PATH = r'.\data\yannis\output\generations.csv'

def load_data():
    df = pd.read_csv(
        CSV_PATH,
        converters={
            'panel thickness': ast.literal_eval,
            'stringer Parameters': ast.literal_eval
        }
    )
    if 'GenIndex' in df.columns:
        df = df.sort_values('GenIndex')
    return df

def plot_all():
    df = load_data()
    gen_idx = df['GenIndex']

    for ax in axes:
        ax.clear()

    # 1. Panel Thicknesses
    panel_thicknesses = df['panel thickness'].tolist()
    panel_thicknesses = list(map(list, zip(*panel_thicknesses)))  # transpose
    for i, thickness in enumerate(panel_thicknesses):
        axes[0].plot(gen_idx, thickness, marker='o', linewidth=2, markersize=6, label=f'panel{i+1}')
    axes[0].set_title('Panel Thicknesses', fontsize=16, fontweight='bold')
    axes[0].set_xlabel('GenIndex', fontsize=12)
    axes[0].set_ylabel('Thickness', fontsize=12)
    axes[0].legend(fontsize=10, loc='best', frameon=True)
    axes[0].grid(True, linestyle='--', alpha=0.7)

    # 2-6. Stringer Parameters (one plot per stringer, 4 dims each)
    stringer_params = df['stringer Parameters'].tolist()
    for s_idx in range(5):
        for d_idx in range(4):
            values = [gen[s_idx][d_idx] for gen in stringer_params]
            axes[1 + s_idx].plot(gen_idx, values, marker='o', linewidth=2, markersize=6, label=f'dim{d_idx+1}')
        axes[1 + s_idx].set_title(f'Stringer {s_idx+1} Dimensions', fontsize=16, fontweight='bold')
        axes[1 + s_idx].set_xlabel('GenIndex', fontsize=12)
        axes[1 + s_idx].set_ylabel('Value', fontsize=12)
        axes[1 + s_idx].legend(fontsize=10, loc='best', frameon=True)
        axes[1 + s_idx].grid(True, linestyle='--', alpha=0.7)

    # 7. Score
    axes[6].plot(gen_idx, df['score'], marker='o', color='#0072B2', linewidth=2, markersize=6)
    axes[6].set_title('Score', fontsize=16, fontweight='bold')
    axes[6].set_xlabel('GenIndex', fontsize=12)
    axes[6].set_ylabel('Score', fontsize=12)
    axes[6].grid(True, linestyle='--', alpha=0.7)

    # 8. Mass
    axes[7].plot(gen_idx, df['mass'], marker='o', color='#009E73', linewidth=2, markersize=6)
    axes[7].set_title('Mass', fontsize=16, fontweight='bold')
    axes[7].set_xlabel('GenIndex', fontsize=12)
    axes[7].set_ylabel('Mass', fontsize=12)
    axes[7].grid(True, linestyle='--', alpha=0.7)

    # 9. Min RF
    axes[8].plot(gen_idx, df['min RF'], marker='o', color='#D55E00', linewidth=2, markersize=6)
    axes[8].set_title('Min RF', fontsize=16, fontweight='bold')
    axes[8].set_xlabel('GenIndex', fontsize=12)
    axes[8].set_ylabel('Min RF', fontsize=12)
    axes[8].grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.4, wspace=0.3)
    fig.suptitle('Generation Results Overview', fontsize=20, fontweight='bold', y=1.03)
    plt.draw()

def on_reload(event):
    plot_all()

fig, axes = plt.subplots(3, 3, figsize=(18, 12))
axes = axes.flatten()

# Adjust layout to make space for button at the bottom
plt.subplots_adjust(hspace=0.4, wspace=0.3, bottom=0.12)

# Add reload button centered below the plots
button_width = 0.1
button_height = 0.04
button_left = 0.35 - button_width / 2
button_bottom = 0.02
button_ax = fig.add_axes([button_left, button_bottom, button_width, button_height])
reload_button = Button(button_ax, 'Reload Data', color='#cccccc', hovercolor='#aaaaaa')
reload_button.on_clicked(on_reload)

plot_all()
plt.show()