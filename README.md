# 🇩🇪 Ausbildung(vocational training) Insights — NLP & Data Analysis

An end-to-end data analysis project exploring student opinions about Ausbildung programs and companies in Germany using **web scraping, Natural Language Processing (NLP), sentiment analysis, topic modeling, and interactive data visualization**.

The project collects reviews from [Ausbildung.de](https://www.ausbildung.de/), processes unstructured German text, analyzes student sentiment, extracts recurring topics, and presents the results through an interactive web dashboard.

The main objective is to transform raw student reviews into meaningful insights about vocational training programs (*Berufe*), training companies, salaries, study conditions, and geographic distribution.

## 🎯 Project Objectives

- Collect student opinions about different Ausbildung programs and companies.
- Clean and structure unstructured review data.
- Separate opinions about vocational professions from opinions about companies.
- Analyze sentiment using a pretrained German sentiment model and a fine-tuned version.
- Identify recurring themes in student reviews using topic modeling.
- Explore salary evolution across the three years of vocational training.
- Visualize student experiences and opinions through an interactive dashboard.

## 🔄 Project Workflow

The project follows an end-to-end data pipeline, transforming raw student reviews into structured data, NLP results, and interactive visualizations.

```text
┌─────────────────────────────────┐
│  1. Web Scraping                 │
│  BeautifulSoup                   │
│  Collect reviews for 17 Berufe   │
└────────────────┬────────────────┘
                 ▼
┌─────────────────────────────────┐
│  2. Data Storage                 │
│  17 CSV files                    │
│  Raw student reviews             │
└────────────────┬────────────────┘
                 ▼
┌─────────────────────────────────┐
│  3. Data Cleaning & Preparation  │
│  Salary extraction               │
│  Separate Beruf and Firma        │
│  Opinions                        │
└────────────────┬────────────────┘
                 ▼
┌─────────────────────────────────┐
│  4. Sentiment Analysis           │
│  German Sentiment BERT           │
│  Baseline predictions            │
│  Fine-tuning on collected data   │
└────────────────┬────────────────┘
                 ▼
┌─────────────────────────────────┐
│  5. Topic Modeling               │
│  Sentence Transformers           │
│  UMAP + HDBSCAN + K-Means        │
│  Identify recurring topics       │
└────────────────┬────────────────┘
                 ▼
┌─────────────────────────────────┐
│  6. Processed Data               │
│  analys_result.csv               │
│  top_beruf_topics.csv            │
│  top_firma_topics.csv            │
└────────────────┬────────────────┘
                 ▼
┌─────────────────────────────────┐
│  7. Interactive Dashboard        │
│  Flask + HTML + CSS + JavaScript │
│  Charts, salary analysis,        │
│  sentiment, topics and map       │
└─────────────────────────────────┘
```

### Workflow Summary

1. **Web Scraping:** Extract student reviews from Ausbildung.de for 17 vocational training programs.
2. **Data Storage:** Save the collected reviews in separate CSV files organized by Beruf.
3. **Data Cleaning:** Extract salary information for the three training years and separate opinions about the profession from opinions about the company.
4. **Sentiment Analysis:** Apply a pretrained German sentiment model, fine-tune it using the collected data, and compare the resulting predictions.
5. **Topic Modeling:** Generate multilingual sentence embeddings and use dimensionality reduction and clustering techniques to discover recurring themes.
6. **Processed Data:** Store the cleaned reviews, sentiment results, and extracted topics in CSV files for further analysis.
7. **Dashboard Development:** Build a web interface to explore sentiment, salary trends, topics, geographic distributions, and study conditions.

**Final result:** A data analysis application that combines web scraping, NLP, and interactive visualization to explore student experiences with Ausbildung programs and training companies in Germany.


## 🕷️ 1. Web Scraping and Data Collection

The first stage uses **BeautifulSoup** to extract student reviews from Ausbildung.de for 17 different vocational training programs and related study paths.

Each scraped dataset contains up to eight fields describing the review and its context:

| Column             | Description                                                      |
| ------------------ | ---------------------------------------------------------------- |
| `suggestion`       | Positive or negative recommendation indicator                    |
| `opinion`          | Student's written review                                         |
| `company`          | Company providing the training                                   |
| `ausbildung_place` | City where the training takes place                              |
| `ausbildung_begin` | Beginning date or year of the training                           |
| `salary`           | Salary information extracted from the review                     |
| `study_condition`  | Whether the student completed, is pursuing, or quit the training |
| `beruf`            | Vocational training program or profession                        |

The collected reviews are stored in 17 separate CSV files, organized by Beruf. Some datasets contain more than 150 rows, while others contain fewer than five.

### Collected vocational training programs

The collection covers areas such as IT, software development, cybersecurity, electronics, engineering, and business informatics.

Examples include:

- Duales Studium IT-Security
- Duales Studium Wirtschaftsinformatik
- Fachinformatiker
- Fachinformatiker für Anwendungsentwicklung
- Fachinformatiker für Daten- und Prozessanalyse
- Fachinformatiker für Digitale Vernetzung
- Fachinformatiker für Systemintegration
- Elektroniker für Automatisierungstechnik
- Elektroniker für Betriebstechnik
- Elektroniker für Maschinen und Antriebstechnik
- Elektroniker für Geräte und Systeme
- Informationselektroniker
- IT-Systemelektroniker
- Kaufmann/-frau für Digitalisierungsmanagement
- Kaufmann/-frau für IT-System-Management
- Mathematisch-technische Softwareentwicklung
- Technischer Assistent für Informatik

The original CSV filenames are retained according to the naming conventions used in the project.

## 🧹 2. Data Cleaning and Preparation

Raw web data often contains inconsistent formatting and multiple types of information stored in a single field. The cleaning stage prepares the data for analysis.

### Salary extraction

The original `salary` column contains text that may include salary amounts for different training years.

The column is transformed into three separate fields:

- `first_year_salary`
- `second_year_salary`
- `third_year_salary`

This makes it possible to compare salaries across the three years of Ausbildung.

Missing salary values are an important consideration because not every student mentions their salary, and some reviews provide only partial information.

### Separating opinions

Each review can contain two distinct types of feedback:

- **Opinion about the Beruf:** The student's experience with the vocational training program itself.
- **Opinion about the Firma:** The student's experience with the company providing the training.

These opinions are separated so that the sentiment and topic analyses can distinguish between the training profession and the employer.

### Clean dataset

The resulting cleaned and analyzed dataset is stored in:

`analys_result.csv`

This file serves as a central data source for the subsequent analysis and dashboard.

## 🧠 3. Sentiment Analysis and Model Fine-Tuning

Sentiment analysis is used to identify the emotional polarity expressed in student reviews.

The project uses the pretrained German sentiment model:

[`oliverguhr/german-sentiment-bert`](https://huggingface.co/oliverguhr/german-sentiment-bert)

### Baseline model

The pretrained model is applied to the collected opinions to establish an initial sentiment classification.

This provides a baseline against which the fine-tuned model can be compared.

### Fine-tuned model

The pretrained model is then fine-tuned using the available project data, which contains approximately **1,127 rows**.

The objective is to adapt the model to the collected reviews and explore whether fine-tuning improves sentiment classification for this dataset.

The processed results include a fine-tuned sentiment column, which can be compared with the baseline predictions.

**Important:** The dataset size alone does not establish model quality. Reliable evaluation requires appropriate training and test splits, suitable labels, and metrics such as precision, recall, and F1-score.

## 🗂️ 4. Topic Modeling

Sentiment analysis indicates whether an opinion is positive or negative, but it does not explain the specific issues students discuss.

To explore the content of the reviews, the project uses sentence embeddings and clustering to identify recurring topics.

### Technologies used

| Technology                                                    | Purpose                                                                   |
| ------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | Convert review text into numerical embeddings                             |
| UMAP                                                          | Reduce embedding dimensionality                                           |
| HDBSCAN                                                       | Discover clusters of reviews without requiring a fixed number of clusters |
| K-Means                                                       | Group reviews into a predefined number of clusters                        |

The pipeline combines semantic text representations with clustering techniques to explore similarities between student opinions.

### Topic outputs

The topic modeling stage produces two CSV files:

- `top_beruf_topics.csv` — Topics associated with opinions about vocational training programs.
- `top_firma_topics.csv` — Topics associated with opinions about training companies.

These files support the dashboard's exploration of recurring themes in both types of feedback.

The topics should be interpreted in the context of the underlying reviews. Clustering does not automatically guarantee that every group represents a clear or meaningful topic.

## 📊 5. Interactive Dashboard

The processed data is presented through a web application built with **Flask, HTML, CSS, JavaScript, and Python**.

The dashboard combines summary statistics and five visualizations to explore the collected reviews from different perspectives.

### Dataset overview

The dashboard begins with an overview of the dataset, including:

- Total number of opinions.
- Number of vocational training programs analyzed.
- Time range between the earliest and latest recorded opinions.

These indicators help users understand the scope and temporal coverage of the collected data.

### Visualization 1 — Sentiment by Beruf

Compares sentiment results across vocational training programs using the baseline model and the fine-tuned model.

**Analytical purpose:** Explore how the two models classify student opinions across different professions and identify differences in their predictions.

### Visualization 2 — Mean Salary Across Training Years

Shows salary trends across the first, second, and third years of Ausbildung, with comparisons between vocational training programs.

**Analytical purpose:** Examine salary progression during vocational training and compare average salaries between different professions.

Because salary information can be incomplete, the number of available salary observations should be considered when interpreting these averages.

### Visualization 3 — Top Topics by Beruf and Firma

Displays the two leading topics associated with vocational training opinions and the three leading topics associated with company opinions.

**Analytical purpose:** Identify recurring themes in student feedback about training programs and employers.

This visualization complements sentiment analysis by exploring the subjects behind the opinions.

### Visualization 4 — Opinions by City

Uses a map of Germany with geographic markers representing the number of student opinions associated with each city.

The project uses **Folium** and a separate `city_coordinates.csv` file to associate cities with latitude and longitude coordinates.

**Analytical purpose:** Explore the geographic distribution of the collected reviews and identify cities with more recorded opinions.

The map represents the distribution of collected reviews, not necessarily the actual distribution of all Ausbildung students or job opportunities in Germany.

### Visualization 5 — Study Conditions by Company

Uses a bar chart to compare student training outcomes and experiences across companies.

The analysis considers study conditions such as completed training, ongoing training, and discontinued training.

**Analytical purpose:** Explore which companies have more reviews associated with successful completion or negative training outcomes.

These counts reflect the collected reviews and should not be interpreted directly as company-wide success or failure rates without accounting for the number of reviews and the characteristics of the sample.

## 🛠️ Technologies and Libraries

| Technology                | Role in the project                                   |
| ------------------------- | ----------------------------------------------------- |
| Python                    | Main programming language                             |
| BeautifulSoup             | Web scraping                                          |
| Pandas                    | Data cleaning and manipulation                        |
| NumPy                     | Numerical operations                                  |
| Hugging Face Transformers | Loading and fine-tuning the sentiment model           |
| Sentence Transformers     | Generating text embeddings                            |
| UMAP                      | Dimensionality reduction                              |
| HDBSCAN                   | Density-based clustering                              |
| K-Means                   | Clustering reviews into a predefined number of groups |
| Flask                     | Backend for the web application                       |
| HTML, CSS, JavaScript     | Frontend and interactive interface                    |
| Folium                    | Geographic visualization                              |
| `city_coordinates.csv`    | City-to-coordinate mapping                            |

## 📁 Project Structure

The following is an illustrative structure based on the described workflow. Adapt it to match the actual filenames and folders in your repository.

```text
ausbildung analysis/
│
├── app.py
├── index.html
├── city_coordinates.csv
│
├── scraping/
│   ├── scraping_files/
|       ├── scraper1.py
│       ├── scraper2.py
│       └── ... (17 py files in total)
│   └── scraped_data/
│       ├── fachinformatiker.csv
│       ├── info_systemintegration.csv
│       └── ... (17 CSV files in total)
│
├── data/
│   ├── analys_result.csv
│   ├── top_beruf_topics.csv
│   └── top_firma_topics.csv
│
├── notebooks/
│   └── Data_preprocessing + Sentiment_Analysis.ipynb
|   └── Get Cities Coordinates.ipynb
|   └── Topic Modeling.ipynb
├── ignored_files/
│   ├── adjusted_reviews.csv
│   ├── (these files won't be needed in any step)...
│
├── requirements.txt
└── README.md
```

## 🚀 How to Run the Project

The exact commands depend on how the scraping, NLP, and dashboard scripts are organized.

### 1. Clone the repository

```bash
git clone https://github.com/mediMor710/Ausbildung-Analysis.git
cd Ausbildung-Analysis 
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 3. Install the dependencies

If the repository contains a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Otherwise, create one containing the external libraries actually used by the project. For example:

```text
beautifulsoup4
pandas
numpy
flask
folium
transformers
sentence-transformers
umap-learn
hdbscan
scikit-learn
```

Depending on the training setup, you may also need a deep learning framework such as PyTorch. Verify the compatible versions and installation requirements for your environment.

### 4. Prepare the data

Use the existing CSV files generated by the scraping and processing stages, or execute the corresponding scripts in the correct order if those scripts are included.

The dashboard requires the processed data files and city coordinates used by its visualizations.

### 5. Launch the dashboard

If `app.py` contains the Flask application and its startup entry point, run:

```bash
python app.py
```

Open the local address printed by the application in your browser.

The exact startup procedure may differ depending on how the Flask application is configured.

## ⚠️ Limitations and Considerations

- The dataset contains reviews collected from a specific website and may not represent all Ausbildung students or companies.
- The number of reviews varies considerably across vocational training programs.
- Salary information may be incomplete, inconsistently formatted, or missing.
- Fine-tuning on a relatively small dataset may lead to overfitting, particularly if the training labels are limited or noisy.
- Topic modeling results depend on the embedding model, clustering parameters, and quality of the source text.
- City-level visualizations depend on the accuracy of the geographic mapping.
- Sentiment predictions and study-condition counts should be interpreted as analytical indicators rather than definitive assessments of companies or professions.

Web scraping should also respect the source website's terms of use, applicable data protection requirements, and any relevant access restrictions.

## 🔮 Future Improvements

Potential improvements include:

- Evaluate the baseline and fine-tuned models using precision, recall, F1-score, and a confusion matrix.
- Improve the quality and consistency of training labels.
- Explore topic labeling and representative reviews for each cluster.
- Add filters by profession, company, city, and training year.
- Display sample sizes alongside salary averages and company-level counts.
- Add data quality checks for missing values, duplicate reviews, and inconsistent salary formats.
- Automate the pipeline from scraping to data processing and dashboard generation.
- Improve the dashboard's interactive filtering and visual design.

## 👨‍💻 Author

**ELMEHDI MORTAJA**

- GitHub: (https://github.com/mediMor710)

## 📄 License

No license has been specified yet. Add an appropriate license if you intend to allow others to use, modify, or distribute this project.
