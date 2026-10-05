# CodeAlpha Data Analytics - Task 3: Data Visualization

## 📖 Overview
Generates publication-quality charts and an executive dashboard visualizing book prices, star ratings, and category trends from `books_scraped.csv`.

## 📁 Files
- `visualizer.py`: Visualization pipeline built using `matplotlib` and `seaborn`.
- `books_scraped.csv`: Input dataset.
- `figures/`: Output folder containing generated high-resolution charts:
  - `01_price_distribution.png`
  - `02_rating_distribution.png`
  - `03_top_categories_volume.png`
  - `04_price_by_rating_boxplot.png`
  - `05_category_price_comparison.png`
  - `06_executive_dashboard.png`
- `requirements.txt`: Dependencies for visualization.

## 🛠️ Installation
```bash
pip install -r requirements.txt
```

## ▶️ How to Run
```bash
python visualizer.py
```
This renders and saves all visual charts directly into the `figures/` directory.
