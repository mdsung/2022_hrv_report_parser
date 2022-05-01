# HRV Parser from LabChart

- Author: MinDong Sung
- Date: 2022-04-30

---

## Objective

- extract labchart hrv report to csv

<img width="647" alt="image" src="https://user-images.githubusercontent.com/52244362/166127741-bb1c8b69-f193-49d3-a5b6-bc940ff88fcd.png">

## Process
1. Labchart reports are saved in html file.
2. Extract numbers from labchart reports. 
  - class `Parser` makes each dataclass includes `General`, `TimdDomain`, `FrequencyDomain`, `Nonlinear`
4. Aggregates filename metadata and created dataclass contents to create one table.
