# Results — 2023 Bahrain Grand Prix

Analysis of 956 laps from the 2023 Bahrain Grand Prix using real F1 telemetry 
data extracted via FastF1, processed through the pipeline, and queried from PostgreSQL.

---

## Finding 1 — Zhou Set the Fastest Lap, Not Verstappen

| Driver | Fastest Lap (s) |
|--------|----------------|
| ZHO | 93.996 |
| GAS | 95.068 |
| NOR | 95.257 |
| SAR | 96.037 |
| ALO | 96.156 |
| VER | 96.236 |
| PER | 96.344 |
| MAG | 96.471 |
| STR | 96.546 |
| HAM | 96.546 |

**What this shows:** Zhou Guanyu (Alfa Romeo) set the fastest individual lap 
of the race at 93.996 seconds — over 2 seconds faster than Verstappen's best. 
This is explained by tyre strategy: drivers on fresh soft tyres late in the 
race set purple sectors without the pressure of racing for position. 
Fastest lap in isolation does not reflect race pace — it reflects tyre state 
and track position at a specific moment.

**Engineering insight:** This is why F1 data engineers never use single-lap 
fastest time as a performance metric in isolation. Stint average and tyre-age 
normalised pace are far more meaningful for comparing true car performance.

---

## Finding 2 — Hard Tyres Were Faster Than Softs on Average

| Compound | Avg Lap Time (s) | Laps |
|----------|-----------------|------|
| MEDIUM | 98.245 | 9 |
| HARD | 98.388 | 533 |
| SOFT | 99.142 | 414 |

**What this shows:** Counter-intuitively, the Hard compound produced faster 
average lap times than the Soft compound across the race. Softs averaged 
99.142 seconds versus Hards at 98.388 seconds — a 0.754 second difference 
per lap in favour of the harder compound.

**Why this happens:** The Bahrain circuit is highly abrasive. Soft tyres 
degrade rapidly in these conditions, meaning the average soft lap includes 
many laps on badly worn rubber. Hard tyres maintain their performance window 
for much longer, producing more consistently fast laps across a full stint. 
The Medium sample is too small (9 laps) to draw conclusions.

**Engineering insight:** Raw compound averages are misleading without 
controlling for tyre age. A soft tyre on lap 3 is incomparable to a soft 
tyre on lap 18. This is why tyre-age normalised analysis is standard practice 
in F1 performance engineering.

---

## Finding 3 — Tyre Degradation Is Non-Linear

| Tyre Age | Avg Lap Time (s) |
|----------|-----------------|
| 1 | 100.230 |
| 2 | 98.350 |
| 3 | 98.452 |
| 5 | 98.526 |
| 10 | 98.911 |
| 15 | 99.036 |
| 20 | 98.711 |
| 25 | 98.779 |
| 29 | 99.161 |

**What this shows:** Lap 1 on any tyre is significantly slower — 100.230 
seconds on average — as drivers manage temperatures and tyre pressures 
coming out of the pit lane. From lap 2 onwards pace stabilises, then 
gradually degrades after lap 10 as rubber wears. However degradation 
is not a smooth linear decline — track evolution, fuel load reduction, 
and driver management create significant variation lap to lap.

**Engineering insight:** This is why F1 engineers use rolling averages and 
regression models rather than raw lap times when predicting tyre degradation 
for strategy calls. A single slow lap tells you very little — the trend 
across a stint tells you everything.

---

## Finding 4 — Verstappen's Third Stint on Hards Was His Fastest

**VER stint comparison — best lap per stint:**

| Stint | Compound | Best Lap (s) | Notes |
|-------|----------|-------------|-------|
| 1 | SOFT | 97.974 | Opening stint |
| 2 | SOFT | 97.372 | Fresh soft — fastest soft laps |
| 3 | HARD | 96.236 | Fastest lap of his race |

**What this shows:** Verstappen's fastest lap of the entire race came in 
Stint 3 on Hard tyres at 96.236 seconds — faster than anything he produced 
on Softs. His second stint on Softs was faster than his first (97.372 vs 
97.974), consistent with the track gaining grip as rubber was laid down 
throughout the race.

**Why Stint 3 was fastest:** By the third stint fuel load was at its 
lightest — roughly 40kg less than the start of the race. A lighter car 
generates less tyre stress and corners faster. Combined with a fully 
evolved track surface and Verstappen managing the gap to the field, 
the Hard tyre in clean air on a light fuel load produced his quickest pace.

**Engineering insight:** Isolating the fuel load effect from tyre 
performance is one of the core challenges in F1 data analysis. Engineers 
use lap time corrections based on fuel burn rate (typically around 0.03 
seconds per kilogram of fuel) to normalise pace across a stint.

---

## Summary

| Finding | Key Number | Insight |
|---------|-----------|---------|
| Fastest lap misleads | ZHO: 93.996s | Strategy artifact, not car pace |
| Hard beats Soft on average | 0.754s faster | Degradation dominates on abrasive circuits |
| Lap 1 penalty | +1.88s vs lap 2 | Tyre prep cost is consistent and significant |
| Fuel load effect | VER Stint 3 fastest | Lightest car + track evolution = best pace |

---

*Data source: 2023 Bahrain Grand Prix — FastF1 v3.x*  
*Pipeline: FastF1 → Pandas → PostgreSQL → REST API*  
*956 laps analysed after outlier and null filtering*