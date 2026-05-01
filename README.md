# Predictive Maintenance of Grinder Motors Using Vibration Analysis

> A vibration-based condition monitoring system for grinder motors using MEMS sensors, FFT analysis, and ESP32.

## Problem Statement

Grinder motors operate continuously under heavy industrial loads, making them prone to mechanical faults like:

- Bearing wear
- Shaft misalignment
- Rotor imbalance
- Structural looseness

Traditional maintenance strategies (reactive or time-based preventive) are either too late or wasteful. This project implements a **predictive maintenance system** that detects faults *before* failure occurs.

---

## Abstract

This system uses an **MPU-9250 MEMS sensor** (3-axis accelerometer + 3-axis gyroscope) mounted on a grinder motor to collect vibration data. The data is processed by an **ESP32 microcontroller** using **Fast Fourier Transform (FFT)** to convert time-domain signals into the frequency domain. Abnormal frequency patterns are detected and used to predict potential motor faults early.

---

## System Architecture

```
RPM Data ──────────────────────────── Current Data
              │                              │
              ▼                              ▼
          Data Collection
                │
          Data Transmission
                │
          Data Preprocessing
         ┌─────┼──────┬──────────┐
    Noise │   Data │  Normali- │  Feature
 Filtering│ Handling│  zation   │ Engineering
         └─────┴──────┴──────────┘
                │
          Data Splitting
      ┌─────────┼──────────┐
  Training  Validation  Testing
                │
       ML Model Development
   ┌────────────┼────────────┐
Random Forest  SVM    Decision Tree
                │
         Model Selection
                │
       Real-Time Inference
      ┌──────────┴──────────┐
Predict Failure Prob.    Latency
                │
         Data Visualization
                │
          Feedback Loop
   ┌────────────┼────────────┐
Store Pred.  Retrain     Update Model
                │
          Updated Model
```

---

## Methodology

### 1. Sensor Installation
The **MPU-9250** sensor is mounted on the grinder motor to capture vibration signals along multiple axes (X, Y, Z).

### 2. Casing & Mounting Design
- Aluminum 6061 base plate (3–5 mm, flat machined)
- Epoxy bond layer (rigid) for firm attachment
- Mounted near the **bearing housing region** for maximum fault sensitivity
- Rigid mounting minimizes damping losses and improves FFT reliability

### 3. Data Acquisition
Vibration data is collected in real time by the **ESP32 microcontroller** via I2C from the MPU-9250.

### 4. Signal Processing
Raw time-domain signals are:
- Mean-centered
- Windowed (to reduce spectral leakage)
- Transformed using **FFT** into the frequency domain

### 5. Frequency Analysis
FFT spectrum is analyzed to identify dominant frequencies and amplitudes — each fault type produces a **characteristic frequency signature**.

### 6. Fault Detection
Motor's normal vibration spectrum is compared against observed patterns. Significant deviations indicate:
- Imbalance
- Bearing defects
- Misalignment

### 7. Predictive Maintenance Decision
When abnormal vibration levels are detected, maintenance is **scheduled proactively** — before motor failure.

---

## Results

### Performance Metrics

| Parameter | Baseline (Normal) | Fault 1 | Fault 2 |
|-----------|:-----------------:|:-------:|:-------:|
| Std Dev | 1752.12 | 6062.15 | 2606.93 |
| Dominant Freq (Hz) | 25.92 | 18.46 | 13.02 |
| Dominant Magnitude | 190,983.1 | 3,754,685.4 | 405,711.8 |
| Num Significant Peaks | 857 | 227 | 507 |

### Critical Thresholds

| Parameter | Normal | Warning | Alert | Critical |
|-----------|--------|---------|-------|----------|
| Std Dev | < 2,000 | 2,000–3,000 | 3,000–5,000 | > 6,000 |
| Dominant Freq (Hz) | > 20 | 16–20 | 13–16 | < 13 |
| Dominant Magnitude | < 200,000 | 200K–400K | 400K–1M | > 1M |
| Num Peaks | > 700 | 500–700 | 300–500 | < 300 |

**Key Findings:**
- **Fault 1** was the most severe — std dev jumped to 6062 and dominant magnitude spiked to 3.75M, with energy concentrated in a narrow lower-frequency band (~18 Hz)
- **Fault 2** showed moderate deviation — dominant frequency dropped to 13 Hz, indicating a different fault mode
- FFT successfully differentiated all three motor states

---

## Hardware Used

| Component | Purpose |
|-----------|---------|
| MPU-9250 | 3-axis accelerometer + gyroscope (vibration sensing) |
| ESP32 | Main processing unit, data acquisition, FFT computation |
| Hall Effect Sensor | Motor shaft RPM measurement |
| Temperature Sensor | Surface temperature monitoring |

---

## Literature Survey Highlights

| Author | Contribution |
|--------|-------------|
| Patil & Gaikwad (2018) | FFT-based vibration analysis for rotating machines |
| Kolok et al. (2020) | Low-cost IoT predictive maintenance with MEMS + ESP32 |
| Khalil et al. (2021) | ML-based fault diagnosis using FFT features |
| Kumar et al. (2023) | IoT + Random Forest for industrial motor fault prediction |
| Gupta et al. (2022) | Embedded TinyML on ESP32 for real-time vibration monitoring |

---
## Output
<img width="4168" height="2068" alt="01_FFT_Full_Spectrum" src="https://github.com/user-attachments/assets/6a35702c-bf80-4521-b944-e097e408beb2" />
<img width="5367" height="1852" alt="FFT_Comparison_3Files" src="https://github.com/user-attachments/assets/ac781855-b1bd-45e5-874d-40089d998a6a" />
======================================================================
FFT ANALYSIS REPORT - MOTOR VIBRATION DATA
======================================================================

SAMPLING INFORMATION:
  CSV File: /Users/sejavarthana/Downloads/fault2_2.csv
  Time range: 26466 to 46667 ms
  Duration: 20.201 seconds
  Sampling rate: 142.57 Hz
  Total samples: 2880

SIGNAL STATISTICS:
  Mean: -0.000000
  Std Dev: 2606.93
  Min: -12245.71
  Max: 15445.44
  Peak-to-peak: 27691.15

FFT ANALYSIS (Frequencies ≥ 5 Hz):
  FFT size: 2880
  Frequency resolution: 0.0495 Hz
  Dominant frequency: 13.02 Hz
  Dominant magnitude: 405711.8
  Number of peaks (>10% max): 507

TOP 15 FREQUENCY COMPONENTS (≥5 Hz):
──────────────────────────────────────────────────────────────────────
 1.   13.02 Hz  │  Magnitude:   405711.8  │   31.9%
 2.   10.74 Hz  │  Magnitude:   358163.6  │   28.2%
 3.   13.12 Hz  │  Magnitude:   347953.7  │   27.4%
 4.   16.04 Hz  │  Magnitude:   334732.6  │   26.3%
 5.   12.67 Hz  │  Magnitude:   321575.3  │   25.3%
 6.   14.60 Hz  │  Magnitude:   313356.5  │   24.7%
 7.   11.58 Hz  │  Magnitude:   312706.0  │   24.6%
 8.   15.20 Hz  │  Magnitude:   312251.3  │   24.6%
 9.   19.31 Hz  │  Magnitude:   309021.9  │   24.3%
10.   57.18 Hz  │  Magnitude:   308694.1  │   24.3%
11.   19.60 Hz  │  Magnitude:   303174.5  │   23.9%
12.   64.80 Hz  │  Magnitude:   301230.3  │   23.7%
13.   15.69 Hz  │  Magnitude:   297237.9  │   23.4%
14.   20.20 Hz  │  Magnitude:   293327.7  │   23.1%
15.   11.53 Hz  │  Magnitude:   292200.1  │   23.0%
──────────────────────────────────────────────────────────────────────

ENERGY DISTRIBUTION:
  0-5 Hz (IGNORED):    8.4%
  5-10 Hz:             8.2%
  10-50 Hz:           57.2%
  50-100 Hz:          26.2%
  >100 Hz:             0.0%
  Significant (≥5 Hz):  91.6%

INTERPRETATION:
  • Energy below 5 Hz is ignored (sensor drift, measurement bias)
  • 91.6% of energy is from real motor vibrations (≥5 Hz)
  • Primary vibration is centered around 13.02 Hz
  • Most energy is in the 10-50 Hz band (57.2%)

================================================================================
FFT ANALYSIS COMPARISON REPORT - 3 MOTOR DATASETS
================================================================================

PARAMETER           NORMAL              FAULT 2             FAULT 1             
================================================================================
Dominant Freq (Hz)  25.92               13.02               18.46               
Dominant Magnitude  190983              405712              3754685             
Std Dev             1752.12             2606.93             6062.15             
Peak-to-Peak        10677.52            27691.15            21437.93            
Duration (sec)      13.89               20.20               29.04               
================================================================================

DETAILED ANALYSIS:
================================================================================


1. NORMAL
────────────────────────────────────────────────────────────────────────────────
  File: /Users/sejavarthana/Downloads/normal_2.csv
  Sampling Rate: 142.79 Hz
  Duration: 13.888 seconds
  Total Samples: 1983
  Std Dev: 1752.12
  Peak-to-Peak: 10677.52
  Dominant Frequency (≥5 Hz): 25.92 Hz
  Dominant Magnitude: 190983.1


2. FAULT 2
────────────────────────────────────────────────────────────────────────────────
  File: /Users/sejavarthana/Downloads/fault2_2.csv
  Sampling Rate: 142.57 Hz
  Duration: 20.201 seconds
  Total Samples: 2880
  Std Dev: 2606.93
  Peak-to-Peak: 27691.15
  Dominant Frequency (≥5 Hz): 13.02 Hz
  Dominant Magnitude: 405711.8


3. FAULT 1
────────────────────────────────────────────────────────────────────────────────
  File: /Users/sejavarthana/Downloads/fault1_4.csv
  Sampling Rate: 142.66 Hz
  Duration: 29.041 seconds
  Total Samples: 4143
  Std Dev: 6062.15
  Peak-to-Peak: 21437.93
  Dominant Frequency (≥5 Hz): 18.46 Hz
  Dominant Magnitude: 3754685.4



## Future Work

- [ ] Collect larger labeled datasets under controlled speed conditions
- [ ] Test on industrial-grade motors
- [ ] Integrate additional sensors: current, acoustic, magnetometer
- [ ] Apply ML classifiers (Random Forest, SVM, Decision Tree) for automated fault classification
- [ ] Build real-time dashboard with cloud-based storage for remote monitoring
- [ ] Deploy embedded TinyML model on ESP32 for on-device inference

---




