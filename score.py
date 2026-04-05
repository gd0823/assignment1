import struct
from pathlib import Path
import os
import sys
import math


def read_doubles(path):
    with open(path, 'rb') as f:
        data = f.read()
    if len(data) % 8 != 0:
        raise ValueError(f"File size not multiple of 8: {path}")
    count = len(data) // 8
    return list(struct.unpack('<' + 'd' * count, data))


def get_accuracy(gt, pred, tol=1e-6):
    if len(gt) != len(pred):
        print(f"  Warning: Array length mismatch: {len(gt)} vs {len(pred)}")
        return 0.0
    if len(gt) == 0:
        return 1.0

    correct = 0
    for g, p in zip(gt, pred):
        if math.isnan(g) and math.isnan(p):
            correct += 1
        elif not math.isnan(g) and not math.isnan(p) and abs(g - p) <= tol:
            correct += 1
    return correct / len(gt)

def main():
    base_path = Path(__file__).parent
    output_path = base_path / "output"
    ground_truth_path = base_path / "ground_truth"

    weights = {
        "output_1": 0,
        "output_2": 0,
        "output_3": 2,
        "output_4": 3,
        "output_5": 1,
        "output_6": 1,
        "output_7": 1,
        "output_8": 2,
        "output_9": 3,
        "output_10": 3,
        "output_11": 3,
        "output_12": 3,
        "output_13": 3,
        "output_14": 3,
        "output_15": 3,
        "output_16": 3,
        "output_17": 3
    }

    if not ground_truth_path.exists():
        raise FileNotFoundError(f"Ground truth directory not found: {ground_truth_path}")

    total_weighted_accuracy = 0.0
    total_weight = sum(weights.values())

    source_accuracies = {}

    print(f"{'Source':<40} | {'Weight':<6} | {'Accuracy':<10} | {'Files':<6}")
    print("-" * 70)

    for source, weight in weights.items():
        gt_source_dir = ground_truth_path / source
        out_source_dir = output_path / source

        if not gt_source_dir.exists():
            print(f"{source:<40} | {weight:<6} | {'N/A':<10} | {'0':<6} (GT not found)")
            source_accuracies[source] = 0.0
            continue

        if not out_source_dir.exists():
            print(f"{source:<40} | {weight:<6} | {'N/A':<10} | {'0':<6} (Output not found)")
            source_accuracies[source] = 0.0
            continue

        accuracies = []
        file_count = 0

        for gt_date_dir in sorted(gt_source_dir.iterdir()):
            if not gt_date_dir.is_dir():
                continue

            date_name = gt_date_dir.name
            out_date_dir = out_source_dir / date_name

            if not out_date_dir.exists():
                print(f"  Warning: Output date directory {date_name} not found for {source}")
                continue

            # Compare files for this date
            for gt_bin_file in sorted(gt_date_dir.glob("*.bin")):
                symbol = gt_bin_file.stem
                out_bin_file = out_date_dir / f"{symbol}.bin"

                if not out_bin_file.exists():
                    print(f"  Error: Output file {source}/{date_name}/{symbol}.bin not found")
                    raise FileNotFoundError(f"Output file {source}/{date_name}/{symbol}.bin not found")

                try:
                    gt_data = read_doubles(gt_bin_file)
                    out_data = read_doubles(out_bin_file)

                    if len(gt_data) == 0:
                        continue

                    acc = get_accuracy(gt_data, out_data, tol=1e-6)
                    accuracies.append(acc)
                    file_count += 1

                    # if acc < 1.0:
                    #     print(f"  {source}/{date_name}/{symbol}.bin: {acc:.6f}")
                except Exception as e:
                    print(f"  Warning: Error reading {source}/{date_name}/{symbol}.bin: {e}, treating as 0.0 accuracy")
                    acc = 0.0
                    accuracies.append(acc)
                    file_count += 1

        if accuracies:
            avg_acc = sum(accuracies) / len(accuracies)
        else:
            avg_acc = 0.0

        source_accuracies[source] = avg_acc
        total_weighted_accuracy += avg_acc * weight
        print(f"{source:<40} | {weight:<6} | {avg_acc:.6f} | {file_count:<6}")

    print("-" * 70)
    final_score = total_weighted_accuracy / total_weight if total_weight > 0 else 0.0
    print(f"Final Weighted Score: {final_score:.6f}")

    print("\nSummary:")
    for source, acc in source_accuracies.items():
        print(f"  {source}: {acc:.6f}")

if __name__ == "__main__":
    main()
