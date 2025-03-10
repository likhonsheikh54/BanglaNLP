# Dataset Statistics

## Overview

BanglaNLP currently contains:

- **120,000+** sentence pairs
- **6** major news sources
- **15+** topic categories
- **92%** alignment accuracy

## Source Distribution
<div class="visualization-container">
    <canvas id="source-chart"></canvas>
</div>

## Dataset Growth
<div class="chart-container">
    <canvas id="dataset-growth"></canvas>
</div>

## Quality Metrics
<div class="quality-metrics-container">
    <div class="metric-card">
        <h3>Language Detection</h3>
        <div class="metric-value">99.2%</div>
        <div class="quality-bar" style="width: 99.2%"></div>
    </div>
    // ...more metrics...
</div>

## Dataset Format

```json
{
    "bn": "বাংলা বাক্য",
    "en": "English sentence",
    "source": "prothomalo",
    "url": "https://example.com/article",
    "date": "2023-09-20"
}
```
