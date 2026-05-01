import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path




# 1. LOAD AND PARSE CSV DATA

print("="*70)
print(" FFT ANALYSIS - MOTOR VIBRATION DATA ".center(70, "="))
print("="*70)

# Ask user for CSV filename
csv_file = input("\nEnter CSV filename (default: fault2_2.csv): ").strip()
if not csv_file:
    csv_file = "/Users/sejavarthana/Downloads/fault2_2.csv"

# Check if file exists
if not os.path.exists(csv_file):
    print(f"Error: File '{csv_file}' not found!")
    print(f"   Please make sure '{csv_file}' is in the same directory as this script.")
    exit(1)

print(f"\nLoading file: {csv_file}")

data = []
skipped_lines = 0
with open(csv_file, "r") as f:
    for i, line in enumerate(f):
        # Strip whitespace and quotes
        line = line.strip().strip('"')
        if not line:
            continue
        try:
            values = [float(x) for x in line.split(',')]
            if len(values) == 7:  # Only keep complete rows
                data.append(values)
            else:
                skipped_lines += 1
        except ValueError:
            skipped_lines += 1
            continue

# Convert to numpy array
data = np.array(data)
print(f"✓ Loaded {len(data)} rows with {data.shape[1]} columns")
if skipped_lines > 0:
    print(f"Skipped {skipped_lines} malformed rows")
print(f"✓ Data shape: {data.shape}")

# 2. EXTRACT COLUMNS
time_ms = data[:, 0]  # Time in milliseconds
ax = data[:, 1]       # Acceleration X
ay = data[:, 2]       # Acceleration Y
az = data[:, 3]       # Acceleration Z
gx = data[:, 4]       # Gyroscope X
gy = data[:, 5]       # Gyroscope Y
gz = data[:, 6]       # Gyroscope Z

# 3. CALCULATE SAMPLING RATE

duration_ms = (time_ms[-1] - time_ms[0])
duration_s = duration_ms / 1000.0
fs = len(data) / duration_s

print(f"\nSAMPLING INFORMATION:")
print(f"   Time range: {time_ms[0]:.0f} to {time_ms[-1]:.0f} ms")
print(f"   Duration: {duration_s:.3f} seconds")
print(f"   Sampling rate: {fs:.2f} Hz")
print(f"   Total samples: {len(data)}")

# 4. CREATE ACCELERATION MAGNITUDE SIGNAL
signal = np.sqrt(ax**2 + ay**2 + az**2)

# Remove DC offset (mean)
signal = signal - np.mean(signal)

print(f"\nSIGNAL STATISTICS:")
print(f"   Mean: {np.mean(signal):.6f}")
print(f"   Std Dev: {np.std(signal):.2f}")
print(f"   Min: {np.min(signal):.2f}")
print(f"   Max: {np.max(signal):.2f}")
print(f"   Peak-to-peak: {np.max(signal) - np.min(signal):.2f}")


# 5. PERFORM FFT
N = len(signal)
fft_values = np.fft.fft(signal)
fft_magnitude = np.abs(fft_values)[:N//2]
freqs = np.fft.fftfreq(N, d=1/fs)[:N//2]

print(f"\nFFT ANALYSIS:")
print(f"   FFT size: {N}")
print(f"   Frequency resolution: {freqs[1] - freqs[0]:.4f} Hz")
print(f"   Max frequency (Nyquist): {freqs[-1]:.2f} Hz")

# 6. IDENTIFY DOMINANT FREQUENCY COMPONENTS (Ignoring < 5 Hz)

peak_threshold = np.max(fft_magnitude) * 0.1
peak_indices = np.where(fft_magnitude > peak_threshold)[0]
peak_freqs = freqs[peak_indices]
peak_mags = fft_magnitude[peak_indices]

# Filter out frequencies less than 5 Hz
filtered_mask = peak_freqs >= 5.0
filtered_peak_freqs = peak_freqs[filtered_mask]
filtered_peak_mags = peak_mags[filtered_mask]

print(f"\n{'='*70}")
print(f"TOP 15 FREQUENCY COMPONENTS (>10% of max, ≥5 Hz)".center(70))
print(f"{'='*70}")

if len(filtered_peak_freqs) > 0:
    top_indices = np.argsort(filtered_peak_mags)[-15:][::-1]
    for i, idx in enumerate(top_indices, 1):
        freq = filtered_peak_freqs[idx]
        mag = filtered_peak_mags[idx]
        pct = (mag / np.max(fft_magnitude)) * 100
        print(f"{i:2d}. {freq:7.2f} Hz  │  Magnitude: {mag:10.1f}  │  {pct:5.1f}%")
else:
    print("No significant frequencies found above 5 Hz threshold.")

# ============================================================================
# 7. CALCULATE ENERGY DISTRIBUTION
# ============================================================================
band_0_5 = np.sum(fft_magnitude[(freqs >= 0) & (freqs < 5)])
band_5_10 = np.sum(fft_magnitude[(freqs >= 5) & (freqs < 10)])
band_10_50 = np.sum(fft_magnitude[(freqs >= 10) & (freqs < 50)])
band_50_100 = np.sum(fft_magnitude[(freqs >= 50) & (freqs < 100)])
band_100_plus = np.sum(fft_magnitude[(freqs >= 100)])
total_energy = np.sum(fft_magnitude)

energy_0_5_pct = 100*band_0_5/total_energy
energy_5_10_pct = 100*band_5_10/total_energy
energy_10_50_pct = 100*band_10_50/total_energy
energy_50_100_pct = 100*band_50_100/total_energy
energy_100_plus_pct = 100*band_100_plus/total_energy

# ============================================================================
# 8. GENERATE AND SAVE PLOTS
# ============================================================================
print(f"\n{'='*70}")
print(f"GENERATING PLOTS".center(70))
print(f"{'='*70}")

# Create output directory if needed
output_dir = "fft_plots"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"✓ Created directory: {output_dir}")

# ========== PLOT 1: Full FFT Spectrum ==========
plt.figure(figsize=(14, 7))
plt.plot(freqs, fft_magnitude, linewidth=1.2, color='steelblue', alpha=0.8)
plt.xlabel("Frequency (Hz)", fontsize=12, fontweight='bold')
plt.ylabel("Magnitude", fontsize=12, fontweight='bold')
plt.title("FFT Spectrum - Motor Vibration (Full Range)", fontsize=14, fontweight='bold', pad=20)
plt.xlim(0, fs/2)
plt.axvline(x=5, color='red', linestyle='--', linewidth=2, label='5 Hz Threshold', alpha=0.7)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()

plot1_path = os.path.join(output_dir, "01_FFT_Full_Spectrum.png")
plt.savefig(plot1_path, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {plot1_path}")
plt.close()





# ============================================================================
# 9. SUMMARY AND ANALYSIS
# ============================================================================
print(f"\n{'='*70}")
print(f"📋 ANALYSIS SUMMARY".center(70))
print(f"{'='*70}")

# Find dominant frequency (excluding < 5 Hz)
freqs_above_5hz = freqs[freqs >= 5.0]
mags_above_5hz = fft_magnitude[freqs >= 5.0]

if len(mags_above_5hz) > 0:
    dominant_idx_filtered = np.argmax(mags_above_5hz)
    dominant_freq = freqs_above_5hz[dominant_idx_filtered]
    dominant_mag = mags_above_5hz[dominant_idx_filtered]
    print(f"\n✓ Dominant frequency (≥5 Hz): {dominant_freq:.2f} Hz")
    print(f"✓ Dominant magnitude: {dominant_mag:.1f}")
else:
    print(f"\n✓ Dominant frequency (≥5 Hz): None found")

print(f"✓ Number of peaks (>10% max, ≥5 Hz): {len(filtered_peak_freqs)}")

print(f"\nEnergy Distribution:")
print(f"   0-5 Hz:    {band_0_5:10.1f}  ({energy_0_5_pct:5.1f}%)  [IGNORED - Sensor Drift]")
print(f"   5-10 Hz:   {band_5_10:10.1f}  ({energy_5_10_pct:5.1f}%)")
print(f"   10-50 Hz:  {band_10_50:10.1f}  ({energy_10_50_pct:5.1f}%)")
print(f"   50-100 Hz: {band_50_100:10.1f}  ({energy_50_100_pct:5.1f}%)")
print(f"   >100 Hz:   {band_100_plus:10.1f}  ({energy_100_plus_pct:5.1f}%)")
print(f"   {'─'*60}")
print(f"   Total:     {total_energy:10.1f}  (100.0%)")

# Energy above 5 Hz
energy_above_5hz = total_energy - band_0_5
energy_above_5hz_pct = 100 * energy_above_5hz / total_energy
print(f"\nSignificant Energy (≥5 Hz):")
print(f"   Energy: {energy_above_5hz:10.1f}  ({energy_above_5hz_pct:5.1f}%)")

# ========== SAVE SUMMARY REPORT ==========
report_path = os.path.join(output_dir, "Analysis_Report.txt")
with open(report_path, 'w') as f:
    f.write("="*70 + "\n")
    f.write("FFT ANALYSIS REPORT - MOTOR VIBRATION DATA\n")
    f.write("="*70 + "\n\n")
    
    f.write("SAMPLING INFORMATION:\n")
    f.write(f"  CSV File: {csv_file}\n")
    f.write(f"  Time range: {time_ms[0]:.0f} to {time_ms[-1]:.0f} ms\n")
    f.write(f"  Duration: {duration_s:.3f} seconds\n")
    f.write(f"  Sampling rate: {fs:.2f} Hz\n")
    f.write(f"  Total samples: {len(data)}\n\n")
    
    f.write("SIGNAL STATISTICS:\n")
    f.write(f"  Mean: {np.mean(signal):.6f}\n")
    f.write(f"  Std Dev: {np.std(signal):.2f}\n")
    f.write(f"  Min: {np.min(signal):.2f}\n")
    f.write(f"  Max: {np.max(signal):.2f}\n")
    f.write(f"  Peak-to-peak: {np.max(signal) - np.min(signal):.2f}\n\n")
    
    f.write("FFT ANALYSIS (Frequencies ≥ 5 Hz):\n")
    f.write(f"  FFT size: {N}\n")
    f.write(f"  Frequency resolution: {freqs[1] - freqs[0]:.4f} Hz\n")
    if len(mags_above_5hz) > 0:
        f.write(f"  Dominant frequency: {dominant_freq:.2f} Hz\n")
        f.write(f"  Dominant magnitude: {dominant_mag:.1f}\n")
    f.write(f"  Number of peaks (>10% max): {len(filtered_peak_freqs)}\n\n")
    
    f.write("TOP 15 FREQUENCY COMPONENTS (≥5 Hz):\n")
    f.write(f"{'─'*70}\n")
    if len(filtered_peak_freqs) > 0:
        top_indices = np.argsort(filtered_peak_mags)[-15:][::-1]
        for i, idx in enumerate(top_indices, 1):
            freq = filtered_peak_freqs[idx]
            mag = filtered_peak_mags[idx]
            pct = (mag / np.max(fft_magnitude)) * 100
            f.write(f"{i:2d}. {freq:7.2f} Hz  │  Magnitude: {mag:10.1f}  │  {pct:5.1f}%\n")
    f.write(f"{'─'*70}\n\n")
    
    f.write("ENERGY DISTRIBUTION:\n")
    f.write(f"  0-5 Hz (IGNORED):  {energy_0_5_pct:5.1f}%\n")
    f.write(f"  5-10 Hz:           {energy_5_10_pct:5.1f}%\n")
    f.write(f"  10-50 Hz:          {energy_10_50_pct:5.1f}%\n")
    f.write(f"  50-100 Hz:         {energy_50_100_pct:5.1f}%\n")
    f.write(f"  >100 Hz:           {energy_100_plus_pct:5.1f}%\n")
    f.write(f"  Significant (≥5 Hz): {energy_above_5hz_pct:5.1f}%\n\n")
    
    f.write("INTERPRETATION:\n")
    f.write(f"  • Energy below 5 Hz is ignored (sensor drift, measurement bias)\n")
    f.write(f"  • {energy_above_5hz_pct:.1f}% of energy is from real motor vibrations (≥5 Hz)\n")
    f.write(f"  • Primary vibration is centered around {dominant_freq:.2f} Hz\n")
    f.write(f"  • Most energy is in the 10-50 Hz band ({energy_10_50_pct:.1f}%)\n")

print(f"✓ Saved: {report_path}")

# ============================================================================
# 10. FINISH
# ============================================================================
print(f"\n{'='*70}")
print(f"✓ ANALYSIS COMPLETE!".center(70))
print(f"{'='*70}")
print(f"\nAll files saved in directory: {os.path.abspath(output_dir)}")
print(f"\nGenerated plots:")
print(f"   1. 01_FFT_Full_Spectrum.png")
print(f"   2. Analysis_Report.txt")
print(f"\n")
