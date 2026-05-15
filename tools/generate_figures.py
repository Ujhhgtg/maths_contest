import matplotlib

matplotlib.use("Agg")
import os

import matplotlib.pyplot as plt
import numpy as np

# Configure Chinese font
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

fig_dir = "../figures"
os.makedirs(fig_dir, exist_ok=True)


# ============================================================
# Fig 1: Pagoda structural diagram
# ============================================================
def fig1_pagoda_structure():
    # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 8))
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 8))

    # Left: elevation with dimensions
    # Data for the pagoda outline
    diameters = [30.27, 26.88, 23.12, 19.50, 15.50]
    heights = [8.76, 8.40, 7.75, 7.30, 6.65]
    cum_heights = [sum(heights[: i + 1]) for i in range(5)]

    # Draw trapezoidal outline
    for i in range(5):
        y_bottom = cum_heights[i] - heights[i]
        y_top = cum_heights[i]
        r_bottom = diameters[i] / 2
        r_top = diameters[i + 1] / 2 if i < 4 else diameters[4] / 2 * 0.7
        x_left = [-r_bottom, -r_top, r_top, r_bottom]
        y_vals = [y_bottom, y_top, y_top, y_bottom]
        ax1.fill(x_left, y_vals, alpha=0.3, color=f"C{i}")
        ax1.plot(x_left + [x_left[0]], y_vals + [y_vals[0]], "k-", linewidth=1.5)

    # Add labels
    for i in range(5):
        y_mid = cum_heights[i] - heights[i] / 2
        ax1.text(
            0,
            y_mid,
            f"第{i + 1}层\nH={heights[i]}m",
            ha="center",
            va="center",
            fontsize=9,
            bbox=dict(facecolor="white", alpha=0.7),
        )

    # Dimensions
    ax1.annotate(
        "",
        xy=(0, 0),
        xytext=(0, cum_heights[-1]),
        arrowprops=dict(arrowstyle="<->", lw=1.5),
    )
    ax1.text(1.5, cum_heights[-1] / 2, f"H = {cum_heights[-1]:.1f} m", fontsize=10)

    ax1.set_xlim(-20, 20)
    ax1.set_ylim(0, 45)
    ax1.set_aspect("equal")
    ax1.set_xlabel("宽度 (m)")
    ax1.set_ylabel("高度 (m)")
    ax1.set_title("(a) 木塔立面示意（含尺寸）")
    ax1.grid(True, alpha=0.3)

    # Right: plan view (octagon)
    theta = np.linspace(0, 2 * np.pi, 9)[:-1]
    r_outer = 15.135
    x_outer = r_outer * np.cos(theta)
    y_outer = r_outer * np.sin(theta)

    # Outer circle
    ax2.plot(x_outer, y_outer, "b-", linewidth=2, label="外圈柱（24根）")
    ax2.scatter(x_outer, y_outer, color="blue", s=50, zorder=5)

    # Inner circle
    r_inner = 4.0
    x_inner = r_inner * np.cos(theta)
    y_inner = r_inner * np.sin(theta)
    ax2.plot(x_inner, y_inner, "r-", linewidth=2, label="内圈柱（8根）")
    ax2.scatter(x_inner, y_inner, color="red", s=50, zorder=5)

    # Octagon outline
    theta_full = np.linspace(0, 2 * np.pi, 9)
    x_poly = r_outer * np.cos(theta_full)
    y_poly = r_outer * np.sin(theta_full)
    ax2.plot(x_poly, y_poly, "k--", alpha=0.5, label="外接圆")

    ax2.set_aspect("equal")
    ax2.set_xlabel("x (m)")
    ax2.set_ylabel("y (m)")
    ax2.set_title("(b) 底层平面布置")
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(
        os.path.join(fig_dir, "fig1_pagoda_structure.png"), dpi=150, bbox_inches="tight"
    )
    plt.close()
    print("Fig 1 saved.")


# ============================================================
# Fig 2: Taper ratio analysis
# ============================================================
def fig2_taper_ratio():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    floors = [1, 2, 3, 4, 5]
    diameters = [30.27, 26.88, 23.12, 19.50, 15.50]

    # Left: diameter vs floor
    ax1.plot(floors, diameters, "bo-", linewidth=2, markersize=8)
    ax1.set_xlabel("层序")
    ax1.set_ylabel("外接圆直径 (m)")
    ax1.set_title("(a) 各层直径变化")
    ax1.set_xticks(floors)
    ax1.grid(True, alpha=0.3)

    # Fit exponential
    coeffs = np.polyfit(floors, np.log(diameters), 1)
    r_fit = np.exp(coeffs[0])
    fitted = diameters[0] * (r_fit ** (np.array(floors) - 1))
    ax1.plot(floors, fitted, "r--", label=f"指数拟合 r={r_fit:.3f}")
    ax1.legend()

    # Right: taper ratios between adjacent floors
    ratios = [diameters[i + 1] / diameters[i] for i in range(4)]
    ax2.bar([f"{i}→{i + 1}" for i in range(1, 5)], ratios, color="orange", alpha=0.7)
    ax2.axhline(y=0.85, color="r", linestyle="--", label="均值 0.85")
    ax2.set_ylabel("收分比 r = D_{i+1}/D_i")
    ax2.set_title("(b) 相邻层收分比")
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    plt.savefig(
        os.path.join(fig_dir, "fig2_taper_ratio.png"), dpi=150, bbox_inches="tight"
    )
    plt.close()
    print("Fig 2 saved.")


# ============================================================
# Fig 3: Vertical load transfer
# ============================================================
def fig3_vertical_load():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    floors = ["第5层", "第4层", "第3层", "第2层", "第1层"]
    N = [925, 2396, 4868, 8208, 13114]
    sigma_out = [0.114, 0.294, 0.597, 1.007, 1.61]
    sigma_in = [0.146, 0.378, 0.768, 1.295, 2.07]

    x = np.arange(len(floors))
    width = 0.35

    ax1.bar(
        x - width / 2,
        [v / 1000 for v in N],
        width,
        label="总荷载 N (×10³ kN)",
        color="steelblue",
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(floors)
    ax1.set_ylabel("荷载 (×10³ kN)")
    ax1.set_title("(a) 各层总竖向荷载")
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis="y")

    ax2.bar(x - width / 2, sigma_out, width, label="外圈柱应力", color="coral")
    ax2.bar(x + width / 2, sigma_in, width, label="内圈柱应力", color="goldenrod")
    ax2.set_xticks(x)
    ax2.set_xticklabels(floors)
    ax2.set_ylabel("压应力 (MPa)")
    ax2.set_title("(b) 各层柱平均压应力")
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    plt.savefig(
        os.path.join(fig_dir, "fig3_vertical_load.png"), dpi=150, bbox_inches="tight"
    )
    plt.close()
    print("Fig 3 saved.")


# ============================================================
# Fig 4: Seismic shear distribution
# ============================================================
def fig4_seismic():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    floors = ["第5层", "第4层", "第3层", "第2层", "第1层"]
    # H_i = [38.86, 32.21, 24.91, 17.16, 8.76]  # height from base
    F_i = [88.2, 116.3, 151.2, 140.7, 105.5]  # seismic force
    V_i = [88.2, 204.5, 355.7, 496.4, 602.0]  # inter-story shear

    # Left: seismic force distribution (horizontal bar)
    ax1.barh(floors, F_i, color="darkred", alpha=0.7)
    for i, v in enumerate(F_i):
        ax1.text(v + 2, i, f"{v:.1f} kN", va="center", fontsize=9)
    ax1.set_xlabel("水平地震作用 F_i (kN)")
    ax1.set_title("(a) 各层水平地震作用")
    ax1.grid(True, alpha=0.3, axis="x")

    # Right: inter-story shear
    ax2.barh(floors, V_i, color="darkblue", alpha=0.7)
    for i, v in enumerate(V_i):
        ax2.text(v + 2, i, f"{v:.1f} kN", va="center", fontsize=9)
    ax2.set_xlabel("层间剪力 V_i (kN)")
    ax2.set_title("(b) 各层层间剪力")
    ax2.grid(True, alpha=0.3, axis="x")

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "fig4_seismic.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("Fig 4 saved.")


# ============================================================
# Fig 5: Dougong isolation mechanism
# ============================================================
def fig5_dougong():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Left: Schematic of dougong friction
    # Draw dougong layers
    layers = 6
    for i in range(layers):
        y = i * 0.8
        width = 3 - i * 0.15
        ax1.fill(
            [-width / 2, width / 2, width / 2, -width / 2],
            [y, y, y + 0.5, y + 0.5],
            color="sandybrown",
            edgecolor="sienna",
            linewidth=1,
        )
        if i < layers - 1:
            # friction arrows
            ax1.annotate(
                "",
                xy=(-0.8, y + 0.25),
                xytext=(0.8, y + 0.25),
                arrowprops=dict(arrowstyle="<->", color="red", lw=1.5),
            )
    ax1.text(0, -0.5, "斗拱各层摩擦滑移", ha="center", fontsize=10)
    ax1.set_xlim(-3, 3)
    ax1.set_ylim(-1, 5)
    ax1.set_aspect("equal")
    ax1.set_title("(a) 斗拱摩擦滑移示意")
    ax1.axis("off")

    # Right: Damping ratio comparison
    categories = ["纯木结构\n(无斗拱)", "含斗拱\n(本文模型)", "含斗拱\n(强震非线性)"]
    damping = [0.02, 0.08, 0.12]
    colors_d = ["lightgray", "goldenrod", "coral"]
    bars = ax2.bar(categories, damping, color=colors_d, edgecolor="black", linewidth=1)
    for bar, val in zip(bars, damping):
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.003,
            f"{val * 100:.0f}%",
            ha="center",
            fontsize=11,
            fontweight="bold",
        )
    ax2.set_ylabel("等效阻尼比")
    ax2.set_title("(b) 斗拱对阻尼比的提升")
    ax2.set_ylim(0, 0.15)
    ax2.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "fig5_dougong.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("Fig 5 saved.")


# ============================================================
# Fig 6: Sensitivity analysis
# ============================================================
def fig6_sensitivity():
    # fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    _, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

    # (a) Friction coefficient vs isolation efficiency
    mu_vals = np.array([0.2, 0.3, 0.35, 0.4, 0.5])
    eta_mu = np.array([15, 22, 26, 30, 37])
    ax1.plot(mu_vals, eta_mu, "bo-", linewidth=2, markersize=8)
    ax1.axvline(x=0.35, color="r", linestyle="--", label="本文取值 μ=0.35")
    ax1.set_xlabel("摩擦系数 μ")
    ax1.set_ylabel("隔震效率 η (%)")
    ax1.set_title("(a) 摩擦系数对隔震效率的影响")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # (b) Elastic modulus vs lateral displacement
    E_vals = np.array([8000, 10000, 12000])
    delta_E = np.array([0.049, 0.039, 0.033]) * 1000  # convert to mm
    ax2.plot(E_vals, delta_E, "rs-", linewidth=2, markersize=8)
    ax2.axvline(x=10000, color="r", linestyle="--", label="本文取值 E=10000 MPa")
    ax2.set_xlabel("弹性模量 E (MPa)")
    ax2.set_ylabel("底层侧移 Δ₁ (mm)")
    ax2.set_title("(b) 弹性模量对侧移的影响")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # (c) Taper ratio comparison (R12: what-if)
    r_vals = [0.80, 0.85, 0.90]
    F_Ek = [532, 602, 685]
    Ko = [13.5, 11.8, 10.4]
    ax3.plot(r_vals, F_Ek, "go-", linewidth=2, markersize=8, label="底部剪力 F_Ek (kN)")
    ax3_twin = ax3.twinx()
    ax3_twin.plot(
        r_vals, Ko, "m^--", linewidth=2, markersize=8, label="抗倾覆安全系数 K_o"
    )
    ax3.axvline(x=0.85, color="gray", linestyle=":", alpha=0.7)
    ax3.set_xlabel("收分比 r")
    ax3.set_ylabel("底部剪力 (kN)", color="g")
    ax3_twin.set_ylabel("抗倾覆安全系数 K_o", color="m")
    ax3.set_title("(c) 不同收分比反事实对比")
    lines1, labels1 = ax3.get_legend_handles_labels()
    lines2, labels2 = ax3_twin.get_legend_handles_labels()
    ax3.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
    ax3.grid(True, alpha=0.3)

    # (d) Summary radar chart of what-if
    categories = ["竖向荷载", "地震作用", "稳定性", "重心高度", "使用空间"]
    r80 = [0.88, 0.88, 1.14, 0.92, 0.70]
    r85 = [1.00, 1.00, 1.00, 1.00, 1.00]
    r90 = [1.14, 1.14, 0.88, 1.07, 1.30]
    x_cat = np.arange(len(categories))
    width = 0.25
    ax4.bar(x_cat - width, r80, width, label="r=0.80", color="coral", alpha=0.7)
    ax4.bar(x_cat, r85, width, label="r=0.85 (本文)", color="goldenrod", alpha=0.7)
    ax4.bar(x_cat + width, r90, width, label="r=0.90", color="steelblue", alpha=0.7)
    ax4.set_xticks(x_cat)
    ax4.set_xticklabels(categories)
    ax4.set_ylabel("相对指标（以 r=0.85 为 1.0）")
    ax4.set_title("(d) 不同收分比综合对比")
    ax4.axhline(y=1.0, color="k", linestyle="--", alpha=0.5)
    ax4.legend(fontsize=8)
    ax4.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    plt.savefig(
        os.path.join(fig_dir, "fig6_sensitivity.png"), dpi=150, bbox_inches="tight"
    )
    plt.close()
    print("Fig 6 saved.")


# ============================================================
# Fig 7: Column stress distribution with control model
# ============================================================
def fig7_column_stress():
    # fig, ax = plt.subplots(figsize=(10, 6))
    _, ax = plt.subplots(figsize=(10, 6))

    floors = ["第5层", "第4层", "第3层", "第2层", "第1层"]
    N_vals = [925, 2396, 4868, 8208, 13114]
    sigma_out = [0.114, 0.294, 0.597, 1.007, 1.61]
    sigma_in = [0.146, 0.378, 0.768, 1.295, 2.07]

    x = np.arange(len(floors))
    width = 0.3

    ax.bar(
        x - width / 2,
        N_vals,
        width,
        label="总竖向荷载 N (kN)",
        color="steelblue",
        alpha=0.8,
    )
    ax_twin = ax.twinx()
    ax_twin.bar(
        x + width / 2,
        sigma_in,
        width,
        label="内圈柱应力 (MPa)",
        color="coral",
        alpha=0.8,
    )
    ax_twin.bar(
        x + 3 * width / 2,
        sigma_out,
        width,
        label="外圈柱应力 (MPa)",
        color="goldenrod",
        alpha=0.8,
    )

    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(floors)
    ax.set_xlabel("层序")
    ax.set_ylabel("总竖向荷载 (kN)")
    ax_twin.set_ylabel("柱压应力 (MPa)")
    ax.set_title("各层柱荷载与应力分布")
    ax.grid(True, alpha=0.3, axis="y")

    # Add safety factor annotation
    ax_twin.annotate(
        f"安全系数 = {15 / 2.07:.1f}",
        xy=(4, 2.07),
        xytext=(4, 2.07 + 0.3),
        ha="center",
        fontsize=11,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
        arrowprops=dict(arrowstyle="->", lw=1.5),
    )

    # Safety line
    ax_twin.axhline(
        y=15, color="red", linestyle="--", linewidth=1.5, label="抗压强度 f_c = 15 MPa"
    )
    ax_twin.text(0.5, 15.5, "木材顺纹抗压强度 f_c = 15 MPa", color="red", fontsize=9)

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax_twin.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=9)

    plt.tight_layout()
    plt.savefig(
        os.path.join(fig_dir, "fig7_column_stress.png"), dpi=150, bbox_inches="tight"
    )
    plt.close()
    print("Fig 7 saved.")


if __name__ == "__main__":
    fig1_pagoda_structure()
    fig2_taper_ratio()
    fig3_vertical_load()
    fig4_seismic()
    fig5_dougong()
    fig6_sensitivity()
    fig7_column_stress()
    print("All figures generated successfully.")
