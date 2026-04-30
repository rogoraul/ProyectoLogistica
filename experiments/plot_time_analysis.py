import csv
import os
from collections import defaultdict


CSV_DIR = "csv_final"
INPUT_CSV = os.path.join(CSV_DIR, "convergence_curves_large.csv")
OUTPUT_PNG = os.path.join(CSV_DIR, "convergence_curves_large.png")

COLORS = {
    "GRASP": "#0077BB",
    "GRASP+TS": "#EE7733",
}


def load_rows(path):
    grouped = defaultdict(list)
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["Instance"], row["Algorithm"])
            grouped[key].append((
                float(row["Elapsed_Time"]),
                float(row["Best_Objective"]),
            ))

    for values in grouped.values():
        values.sort(key=lambda item: item[0])

    return grouped


def main():
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        draw_with_pillow(load_rows(INPUT_CSV), OUTPUT_PNG)
        return

    grouped = load_rows(INPUT_CSV)
    instances = sorted({instance for instance, _algorithm in grouped})

    if not instances:
        raise SystemExit(f"No rows found in {INPUT_CSV}")

    fig, axes = plt.subplots(len(instances), 1, figsize=(10, 4 * len(instances)), sharex=True)
    if len(instances) == 1:
        axes = [axes]

    for ax, instance_name in zip(axes, instances):
        for algorithm in ["GRASP", "GRASP+TS"]:
            values = grouped.get((instance_name, algorithm), [])
            if not values:
                continue

            times = [item[0] for item in values]
            objectives = [item[1] for item in values]
            ax.step(
                times,
                objectives,
                where="post",
                linewidth=2.2,
                color=COLORS[algorithm],
                label=algorithm,
            )
            ax.scatter(times[-1], objectives[-1], color=COLORS[algorithm], s=28)

        ax.set_title(instance_name)
        ax.set_ylabel("Best objective")
        ax.grid(axis="y", alpha=0.25)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend()

    axes[-1].set_xlabel("Elapsed time (s)")
    fig.suptitle("GRASP+TS improves inside long Tabu Search phases", fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUTPUT_PNG, dpi=160)
    print(f"Plot written to: {OUTPUT_PNG}")


def hex_to_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def draw_step_line(draw, points, color, width=3):
    if len(points) == 1:
        x, y = points[0]
        draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=color)
        return

    path = [points[0]]
    for idx in range(1, len(points)):
        prev_x, prev_y = points[idx - 1]
        x, y = points[idx]
        path.append((x, prev_y))
        path.append((x, y))

    draw.line(path, fill=color, width=width)
    x, y = points[-1]
    draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=color)


def draw_with_pillow(grouped, output_path):
    from PIL import Image, ImageDraw, ImageFont

    instances = sorted({instance for instance, _algorithm in grouped})
    if not instances:
        raise SystemExit(f"No rows found in {INPUT_CSV}")

    width = 1200
    panel_height = 430
    margin_left = 90
    margin_right = 40
    margin_top = 55
    margin_bottom = 60
    height = panel_height * len(instances)

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    for panel_idx, instance_name in enumerate(instances):
        y_offset = panel_idx * panel_height
        plot_left = margin_left
        plot_right = width - margin_right
        plot_top = y_offset + margin_top
        plot_bottom = y_offset + panel_height - margin_bottom
        plot_width = plot_right - plot_left
        plot_height = plot_bottom - plot_top

        values_by_algorithm = {
            algorithm: grouped.get((instance_name, algorithm), [])
            for algorithm in ["GRASP", "GRASP+TS"]
        }
        all_values = [item for values in values_by_algorithm.values() for item in values]
        max_time = max(time_value for time_value, _objective in all_values)
        objectives = [objective for _time_value, objective in all_values]
        min_objective = min(objectives)
        max_objective = max(objectives)
        y_padding = max((max_objective - min_objective) * 0.08, 1.0)
        min_objective -= y_padding
        max_objective += y_padding

        draw.text((plot_left, y_offset + 18), f"{instance_name} - best objective over time", fill=(20, 20, 20), font=font)
        draw.line((plot_left, plot_top, plot_left, plot_bottom), fill=(80, 80, 80), width=1)
        draw.line((plot_left, plot_bottom, plot_right, plot_bottom), fill=(80, 80, 80), width=1)

        for grid_idx in range(5):
            ratio = grid_idx / 4
            y = plot_bottom - ratio * plot_height
            value = min_objective + ratio * (max_objective - min_objective)
            draw.line((plot_left, y, plot_right, y), fill=(225, 225, 225), width=1)
            draw.text((18, y - 6), f"{value:.0f}", fill=(90, 90, 90), font=font)

        for tick_idx in range(5):
            ratio = tick_idx / 4
            x = plot_left + ratio * plot_width
            value = ratio * max_time
            draw.line((x, plot_bottom, x, plot_bottom + 5), fill=(100, 100, 100), width=1)
            draw.text((x - 12, plot_bottom + 12), f"{value:.0f}", fill=(90, 90, 90), font=font)

        for legend_idx, algorithm in enumerate(["GRASP", "GRASP+TS"]):
            color = hex_to_rgb(COLORS[algorithm])
            legend_x = plot_right - 190 + legend_idx * 95
            legend_y = y_offset + 20
            draw.line((legend_x, legend_y + 6, legend_x + 26, legend_y + 6), fill=color, width=3)
            draw.text((legend_x + 32, legend_y), algorithm, fill=(40, 40, 40), font=font)

        for algorithm, values in values_by_algorithm.items():
            if not values:
                continue
            color = hex_to_rgb(COLORS[algorithm])
            points = []
            for time_value, objective in values:
                x = plot_left + (time_value / max_time) * plot_width if max_time else plot_left
                y = plot_bottom - ((objective - min_objective) / (max_objective - min_objective)) * plot_height
                points.append((x, y))
            draw_step_line(draw, points, color)

        draw.text((plot_left + plot_width / 2 - 45, y_offset + panel_height - 28), "Elapsed time (s)", fill=(40, 40, 40), font=font)

    image.save(output_path)
    print(f"Plot written to: {output_path}")


if __name__ == "__main__":
    main()
