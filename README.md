# Big Data Platform for Parliamentary Transparency (In Progress)

## Description

This project aims to provide a big data platform for parliamentary transparency.  
The platform will contain data from the [Moroccan Chamber of Deputies](https://www.chambredesrepresentants.ma/fr/). We are concerned about written questions, oral questions and government engagements.  
We mainly have 3 main tasks to accomplish:

1. Collecting data from the Moroccan Chamber of Deputies website.
2. Implementing a big data infrastucture for data storage and preprocessing.
3. Building a web application or dashboard to visualize data.

## Setup (Linux Ubuntu)

create a virtual environment and install the requirements:

```python -m venv .venv```

```source .venv/bin/activate```

```pip install -r requirements.txt```

## Acknowledgements

The following are resources that have been useful for learning about data engineering and big data, and helped in the development of this project:

- [Scrapy tutorials](https://docs.scrapy.org/en/latest/intro/tutorial.html) are great for learning about how to use Scrapy.
- [Scrapfly articles](https://scrapfly.io/blog/how-to-scrape-without-getting-blocked-tutorial/) explain best practices to follow when scraping, in order to avoid getting blocked, respect the website's terms of use, and be a good citizen of the web.
- [Big Data Engineering course](https://www.youtube.com/watch?v=Tyg1FVNq40g) provides clear explanation for the Hadoop ecosystem.
