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

## Future Work

- [ ] Collect larger labeled datasets under controlled speed conditions
- [ ] Test on industrial-grade motors
- [ ] Integrate additional sensors: current, acoustic, magnetometer
- [ ] Apply ML classifiers (Random Forest, SVM, Decision Tree) for automated fault classification
- [ ] Build real-time dashboard with cloud-based storage for remote monitoring
- [ ] Deploy embedded TinyML model on ESP32 for on-device inference

---




