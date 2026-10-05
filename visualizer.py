"""
CodeAlpha Data Analytics Internship - Task 3: Data Visualization

This script generates publication-quality data visualizations from 'books_scraped.csv':
1. 01_price_distribution.png         - Histogram & KDE of book prices with mean/median markers.
2. 02_rating_distribution.png        - Bar chart of star ratings with counts and percentages.
3. 03_top_categories_volume.png      - Top 15 categories by catalog volume.
4. 04_price_by_rating_boxplot.png    - Price distributions across star ratings.
5. 05_category_price_comparison.png  - Top 10 highest vs lowest average priced categories.
6. 06_executive_dashboard.png        - 4-panel consolidated overview dashboard.

All plots are rendered and saved to the 'figures/' directory.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


class BooksVisualizer:
    def __init__(self, data_path: str, figures_dir: str):
        self.data_path = data_path
        self.figures_dir = figures_dir
        self.df = None

        # Configure global plotting aesthetics
        sns.set_theme(style="whitegrid", palette="deep")
        plt.rcParams.update({
            "font.family": "sans-serif",
            "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial"],
            "axes.edgecolor": "#cccccc",
            "axes.linewidth": 0.8,
            "grid.color": "#ebebeb",
            "grid.linestyle": "--",
            "grid.alpha": 0.7,
            "figure.autolayout": False
        })
        os.makedirs(self.figures_dir, exist_ok=True)

    def load_data(self) -> bool:
        """Load and prepare data for plotting."""
        if not os.path.exists(self.data_path):
            print(f"[ERROR] Data file not found at: {self.data_path}")
            return False

        self.df = pd.read_csv(self.data_path)
        self.df["price_gbp"] = pd.to_numeric(self.df["price_gbp"], errors="coerce")
        self.df["star_rating"] = pd.to_numeric(self.df["star_rating"], errors="coerce")
        self.df["category"] = self.df["category"].astype(str).str.strip()
        print(f"[INFO] Loaded {len(self.df)} records for visualization.")
        return True

    def plot_price_distribution(self):
        """1. Price Distribution Histogram + KDE."""
        fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
        prices = self.df["price_gbp"].dropna()
        mean_p = prices.mean()
        median_p = prices.median()

        sns.histplot(prices, kde=True, bins=25, color="#2b5c8f", edgecolor="white", alpha=0.75, ax=ax)
        ax.axvline(mean_p, color="#d9534f", linestyle="--", linewidth=2, label=f"Mean: £{mean_p:.2f}")
        ax.axvline(median_p, color="#5cb85c", linestyle="-.", linewidth=2, label=f"Median: £{median_p:.2f}")

        ax.set_title("Distribution of Book Prices (GBP)", fontsize=15, fontweight="bold", pad=15)
        ax.set_xlabel("Price (£ GBP)", fontsize=12, labelpad=10)
        ax.set_ylabel("Book Count", fontsize=12, labelpad=10)
        ax.legend(frameon=True, facecolor="white", edgecolor="#cccccc", fontsize=11)

        out_path = os.path.join(self.figures_dir, "01_price_distribution.png")
        plt.tight_layout()
        plt.savefig(out_path, dpi=300)
        plt.close(fig)
        print(f"[SAVED] {out_path}")

    def plot_rating_distribution(self):
        """2. Star Rating Frequency & Percentage."""
        fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
        counts = self.df["star_rating"].value_counts().sort_index()
        total = len(self.df)

        colors = ["#e76f51", "#f4a261", "#e9c46a", "#2a9d8f", "#264653"]
        bars = ax.bar([f"{int(r)} Star{'s' if r>1 else ''}" for r in counts.index], counts.values, color=colors, width=0.6, edgecolor="#333333", linewidth=0.6)

        # Annotate counts and percentages
        for bar in bars:
            height = bar.get_height()
            pct = (height / total) * 100
            ax.annotate(f"{height}\n({pct:.1f}%)",
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 4), textcoords="offset points",
                        ha="center", va="bottom", fontsize=11, fontweight="bold", color="#222222")

        ax.set_title("Book Rating Distribution", fontsize=15, fontweight="bold", pad=15)
        ax.set_xlabel("Star Rating", fontsize=12, labelpad=10)
        ax.set_ylabel("Count of Books", fontsize=12, labelpad=10)
        ax.set_ylim(0, max(counts.values) * 1.15)

        out_path = os.path.join(self.figures_dir, "02_rating_distribution.png")
        plt.tight_layout()
        plt.savefig(out_path, dpi=300)
        plt.close(fig)
        print(f"[SAVED] {out_path}")

    def plot_top_categories(self):
        """3. Top 15 Categories by Book Count."""
        top_cats = self.df["category"].value_counts().head(15)

        fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
        palette = sns.color_palette("mako", len(top_cats))
        bars = ax.barh(top_cats.index[::-1], top_cats.values[::-1], color=palette[::-1], edgecolor="none", height=0.65)

        for bar in bars:
            width = bar.get_width()
            ax.annotate(f" {width}",
                        xy=(width, bar.get_y() + bar.get_height() / 2),
                        xytext=(4, 0), textcoords="offset points",
                        ha="left", va="center", fontsize=10, fontweight="bold", color="#333333")

        ax.set_title("Top 15 Book Categories by Catalog Volume", fontsize=15, fontweight="bold", pad=15)
        ax.set_xlabel("Number of Books", fontsize=12, labelpad=10)
        ax.set_ylabel("Category", fontsize=12, labelpad=10)
        ax.set_xlim(0, max(top_cats.values) * 1.12)

        out_path = os.path.join(self.figures_dir, "03_top_categories_volume.png")
        plt.tight_layout()
        plt.savefig(out_path, dpi=300)
        plt.close(fig)
        print(f"[SAVED] {out_path}")

    def plot_price_by_rating_boxplot(self):
        """4. Price Distribution by Star Rating."""
        fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
        palette = sns.color_palette("Set2")

        sns.boxplot(x="star_rating", y="price_gbp", hue="star_rating", data=self.df,
                    palette=palette[:5], ax=ax, width=0.5, legend=False,
                    boxprops=dict(alpha=0.85), flierprops=dict(marker="o", markersize=4, alpha=0.5))
        sns.pointplot(x="star_rating", y="price_gbp", data=self.df, color="#222222", markers="D",
                      linestyles="None", errorbar=None, ax=ax, markersize=7)

        # Legend explanation
        ax.plot([], [], marker="D", color="#222222", linestyle="None", label="Category Mean")
        ax.legend(loc="upper right", frameon=True, facecolor="white")

        ax.set_title("Book Price Distribution Across Star Ratings", fontsize=15, fontweight="bold", pad=15)
        ax.set_xlabel("Star Rating", fontsize=12, labelpad=10)
        ax.set_ylabel("Price (£ GBP)", fontsize=12, labelpad=10)

        out_path = os.path.join(self.figures_dir, "04_price_by_rating_boxplot.png")
        plt.tight_layout()
        plt.savefig(out_path, dpi=300)
        plt.close(fig)
        print(f"[SAVED] {out_path}")

    def plot_category_price_comparison(self):
        """5. Top 10 Most Expensive vs Top 10 Most Affordable Categories."""
        cat_stats = self.df.groupby("category").agg(
            avg_price=("price_gbp", "mean"),
            count=("title", "count")
        ).reset_index()

        # Minimum 4 books for fair statistical comparison
        valid_cats = cat_stats[cat_stats["count"] >= 4]
        if len(valid_cats) < 10:
            valid_cats = cat_stats

        top10_exp = valid_cats.sort_values(by="avg_price", ascending=False).head(8)
        top10_aff = valid_cats.sort_values(by="avg_price", ascending=True).head(8)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=300)

        # Most expensive
        ax1.barh(top10_exp["category"][::-1], top10_exp["avg_price"][::-1], color="#e76f51", height=0.6)
        for i, val in enumerate(top10_exp["avg_price"][::-1]):
            ax1.annotate(f" £{val:.2f}", xy=(val, i), va="center", fontsize=10, fontweight="bold")
        ax1.set_title("Highest Average Price Categories", fontsize=13, fontweight="bold", pad=10)
        ax1.set_xlabel("Average Price (£)", fontsize=11)
        ax1.set_xlim(0, max(top10_exp["avg_price"]) * 1.15)

        # Most affordable
        ax2.barh(top10_aff["category"][::-1], top10_aff["avg_price"][::-1], color="#2a9d8f", height=0.6)
        for i, val in enumerate(top10_aff["avg_price"][::-1]):
            ax2.annotate(f" £{val:.2f}", xy=(val, i), va="center", fontsize=10, fontweight="bold")
        ax2.set_title("Most Affordable Categories", fontsize=13, fontweight="bold", pad=10)
        ax2.set_xlabel("Average Price (£)", fontsize=11)
        ax2.set_xlim(0, max(top10_aff["avg_price"]) * 1.25)

        plt.suptitle("Category Price Comparison (Min 4 Books)", fontsize=16, fontweight="bold", y=0.98)
        out_path = os.path.join(self.figures_dir, "05_category_price_comparison.png")
        plt.tight_layout(rect=[0, 0, 1, 0.94])
        plt.savefig(out_path, dpi=300)
        plt.close(fig)
        print(f"[SAVED] {out_path}")

    def plot_executive_dashboard(self):
        """6. Consolidated 4-Panel Executive Dashboard."""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12), dpi=300)
        fig.suptitle("CodeAlpha Data Analytics - Executive Summary Dashboard", fontsize=18, fontweight="bold", y=0.98)

        # 1. Price Dist
        prices = self.df["price_gbp"].dropna()
        sns.histplot(prices, kde=True, color="#1d3557", ax=axes[0, 0], alpha=0.7)
        axes[0, 0].axvline(prices.mean(), color="#e63946", linestyle="--", label=f"Mean: £{prices.mean():.2f}")
        axes[0, 0].set_title("A. Price Distribution", fontsize=13, fontweight="bold")
        axes[0, 0].set_xlabel("Price (£)")
        axes[0, 0].legend()

        # 2. Rating Breakdown
        r_counts = self.df["star_rating"].value_counts().sort_index()
        colors = ["#e76f51", "#f4a261", "#e9c46a", "#2a9d8f", "#264653"]
        axes[0, 1].bar([f"{int(r)} Star{'s' if r > 1 else ''}" for r in r_counts.index], r_counts.values, color=colors, width=0.55)
        axes[0, 1].set_title("B. Star Rating Frequency", fontsize=13, fontweight="bold")
        axes[0, 1].set_ylabel("Count")

        # 3. Top 8 Categories
        top8 = self.df["category"].value_counts().head(8)
        palette = sns.color_palette("crest", len(top8))
        axes[1, 0].barh(top8.index[::-1], top8.values[::-1], color=palette[::-1], height=0.6)
        axes[1, 0].set_title("C. Top 8 Categories by Volume", fontsize=13, fontweight="bold")
        axes[1, 0].set_xlabel("Book Count")

        # 4. Price by Rating Boxplot
        pastel = sns.color_palette("Pastel1", 5)
        sns.boxplot(x="star_rating", y="price_gbp", hue="star_rating", data=self.df, palette=pastel, ax=axes[1, 1], width=0.5, legend=False)
        axes[1, 1].set_title("D. Price Distribution by Rating", fontsize=13, fontweight="bold")
        axes[1, 1].set_xlabel("Star Rating")
        axes[1, 1].set_ylabel("Price (£)")

        out_path = os.path.join(self.figures_dir, "06_executive_dashboard.png")
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(out_path, dpi=300)
        plt.close(fig)
        print(f"[SAVED] {out_path}")

    def generate_all_visualizations(self):
        """Execute all plotting routines."""
        if not self.load_data():
            return
        print("[INFO] Generating publication-quality charts...")
        self.plot_price_distribution()
        self.plot_rating_distribution()
        self.plot_top_categories()
        self.plot_price_by_rating_boxplot()
        self.plot_category_price_comparison()
        self.plot_executive_dashboard()
        print(f"[SUCCESS] All visualizations generated in: {self.figures_dir}")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Check current directory first (for standalone repo), then parent task1 folder
    possible_paths = [
        os.path.join(script_dir, "books_scraped.csv"),
        os.path.join(project_root, "task1_web_scraping", "books_scraped.csv"),
        os.path.join(os.getcwd(), "books_scraped.csv"),
        os.path.join(os.getcwd(), "task1_web_scraping", "books_scraped.csv"),
    ]
    
    data_file = next((p for p in possible_paths if os.path.exists(p)), possible_paths[0])
    figures_dir = os.path.join(script_dir, "figures")

    visualizer = BooksVisualizer(data_path=data_file, figures_dir=figures_dir)
    visualizer.generate_all_visualizations()


if __name__ == "__main__":
    main()
