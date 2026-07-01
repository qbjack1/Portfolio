# Marketing and Advertising Analysis Python

A Python notebook analyzing three months of multichannel marketing performance for a direct-to-consumer fitness supplements brand. The project focuses on cleaning campaign data, validating performance metrics, comparing channel and regional performance, and developing recommendations for spend allocation.

## Files

```text
.
|-- marketing_data.xlsx
`-- notebook.ipynb
```

## Business Context

The analysis is framed around a brand spending across Facebook, Google, and TikTok while trying to improve ROAS, reduce underperforming spend, and grow revenue. The dataset includes campaign, platform, region, spend, impressions, clicks, purchases, revenue, product category, audience, creative type, customer LTV, and competitive event flags.

## Analysis Flow

- Data quality assessment and missing-value review
- Metric validation for CTR, CPC, CVR, and ROAS
- Data wrangling and removal of impossible or incomplete records
- Channel, region, creative, product, and audience performance analysis
- Statistical testing with Shapiro, Kruskal-Wallis, and Dunn's post-hoc tests
- Strategic recommendations for spend allocation
- Optional regression modeling with Lasso regression for ROAS prediction

## Tools Used

- Python
- pandas
- NumPy
- openpyxl
- SciPy
- scikit-posthocs
- scikit-learn
- Matplotlib
- Seaborn
- Jupyter Notebook

## How to Run

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install the main dependencies:

```powershell
python -m pip install pandas numpy openpyxl scipy scikit-posthocs scikit-learn matplotlib seaborn jupyter
```

Launch the notebook:

```powershell
jupyter notebook notebook.ipynb
```

## Notes

The notebook includes both business-facing commentary and code outputs. Some recommendations depend on the assumptions documented during the data cleaning and metric validation steps.
