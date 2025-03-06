# catnap
1. graphs are generated daily - vanessa
2. sleep score 3-5 days after recieving data - vanessa 
3. use data base direct file from rasp pi (from vanessa) - vanessa


Develop Sleep Score using the Sleep Data (algorithm): - create a formula for the sleep score
Sleep Data: https://docs.google.com/document/d/1RjL8mFpSL2T81FSVjUJbbIZ4C64yyYo7T2cA6JJ5yQQ/edit?tab=t.826wam8uwjxe


Maybe use this: https://cloud.google.com/looker/docs/studio?visit_id=638764669736057988-1463686718&rd=2



# Sleep Score Algorithm

## Overview
This project implements a **sleep score algorithm** using data from a **motion sensor (binary output: 0 or 1), light sensor, and environmental temperature sensor**. The algorithm calculates a sleep score based on key sleep quality metrics.

## Sleep Score Components
The sleep score consists of six key metrics, each contributing a weighted percentage to the final score.

### 1. Sleep Latency (10%)
- **Definition:** Time taken to fall asleep after getting into bed.
- **Measurement:**
  - Detect when the user **lies still** (motion sensor mostly 0 for at least 5 mins).
  - Calculate time from **last movement** to **first long period of stillness**.
- **Scoring:**
  ```
  Sleep Latency Score = 10% × max(0, 1 - (Latency - 15) / 15)
  ```
  - **Best:** < 15 mins → Full 10%
  - **Good:** 15–25 mins → Scaled down
  - **Poor:** > 30 mins → 0%

### 2. Sleep Efficiency (30%)
- **Definition:** Percentage of time in bed spent sleeping.
- **Measurement:**
  - `Time in Bed (TIB)`: Period of low motion and darkness.
  - `Total Sleep Time (TST)`: Total period of motion inactivity.
  - Compute: `Sleep Efficiency = (TST / TIB) × 100`
- **Scoring:**
  ```
  Sleep Efficiency Score = 30% × max(0, 1 - (85 - SE) / 10)
  ```
  - **Best:** SE > 90% → Full 30%
  - **Good:** 85% - 90% → Scaled down
  - **Poor:** < 75% → 0%

### 3. Sleep Interruptions (10%)
- **Definition:** Number of wake events lasting longer than 5 minutes.
- **Measurement:**
  - Count instances where **motion = 1 for > 5 minutes**.
- **Scoring:**
  ```
  Sleep Interruptions Score = 10% - (1% × wake events (5–15 mins)) - (2% × wake events (>15 mins))
  ```
  - **Short wake-ups (< 2 mins) are ignored.**
  - **Capped at 0%.**

### 4. Sleep Duration (30%)
- **Definition:** Total sleep time relative to **8-hour ideal**.
- **Measurement:**
  - Count `Total Sleep Time (TST)` using motion inactivity.
- **Scoring:**
  ```
  Sleep Duration Score = 30% × max(0, 1 - |8 - TST| / 3)
  ```
  - **Best:** 7–9 hours → Full 30%
  - **Suboptimal:** 6–7 or 9–10 hours → Scaled down
  - **Poor:** < 5 or > 10 hours → 0%

### 5. Sleep Regularity Index (10%)
- **Definition:** Consistency of sleep schedule over past 3 days.
- **Measurement:**
  - Compare bedtimes within ±20 minutes of average bedtime.
- **Scoring:**
  ```
  Sleep Regularity Score = 10% × (# of consistent bedtimes (±20 mins) / 3)
  ```

### 6. Environmental Stability (10%)
- **Definition:** Penalizes temperature and light fluctuations.
- **Measurement:**
  - **Temperature Variance (σ_temp)** and **Light Variance (σ_light)**.
  - Penalize **>3°C changes** and **light spikes (>100 lux overnight)**.
- **Scoring:**
  ```
  Environmental Stability Score = 10% - (0.5% × σ_temp) - (0.5% × σ_light)
  ```
  - **Capped at 0%.**

## Final Sleep Score Calculation
``` 
Sleep Score = Sleep Latency Score + Sleep Efficiency Score + Sleep Interruptions Score 
            + Sleep Duration Score + Sleep Regularity Score + Environmental Stability Score 
```
- **Score Range:** 0 - 100%
- **Higher score = Better sleep quality**

## Next Steps
- **Test with real sensor data.**
- **Fine-tune thresholds based on feedback.**
- **Optimize environmental penalties.**
