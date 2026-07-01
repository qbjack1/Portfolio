# National Park Biodiversity Python

A Python data analysis project exploring species information, park observations, and conservation status across national parks. The project combines exploratory analysis, visualization, and chi-squared hypothesis testing.

## Files

```text
.
|-- national_park_biodiversity.py
|-- observations.csv
`-- species_info.csv
```

## Data

`species_info.csv` includes species category, scientific name, common names, and conservation status.

`observations.csv` includes scientific name, park name, and observation count.

## Analysis Flow

- Load and inspect the species and observations datasets
- Summarize species categories and conservation statuses
- Review total observations and park coverage
- Visualize conservation status by species category
- Create protected-species indicators
- Compare protection rates across categories
- Run chi-squared tests for selected category comparisons

## Tools Used

- Python
- pandas
- NumPy
- SciPy
- Matplotlib
- Seaborn

## How to Run

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install dependencies:

```powershell
python -m pip install pandas numpy scipy matplotlib seaborn
```

Run the script from this folder:

```powershell
python national_park_biodiversity.py
```

## Notes

The script prints exploratory summaries to the terminal and displays charts with Matplotlib. It expects `species_info.csv` and `observations.csv` to remain in the same folder as the script.
