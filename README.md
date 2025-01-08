PubMed Data Fetcher
Overview
This project allows you to search and fetch scientific papers from PubMed using the PubMed E-utilities API. The script is designed to search PubMed using custom queries, fetch metadata for matching papers, and classify authors as academic or non-academic based on their affiliation and email domain. The results are saved in a CSV format for further analysis.

Features
Search PubMed: Execute search queries on PubMed to retrieve paper metadata.
Author Classification: Classify authors into academic or non-academic based on their affiliation and email.
Save Results: Save the results, including paper details and author classifications, to a CSV file.
Debug Mode: Enable debug mode to get detailed logs for the operations.
Technologies Used
Python 3.x: Programming language for the script.
Requests: For HTTP requests to fetch data from PubMed API.
Click: For creating command-line interfaces.
CSV: For saving results into a CSV file.
XML: For parsing XML data from PubMed’s fetch response.
Setup Instructions
Prerequisites
Python 3.6 or higher.
pip (Python package installer).
Internet connection to fetch data from the PubMed API.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/pubmed-data-fetcher.git
cd pubmed-data-fetcher
Set up a virtual environment (optional but recommended):

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Configuration
No additional configuration is required for this project. However, if you're dealing with larger data sets or require specific query parameters, you can customize the search query directly in the script.

Running the Script
To run the script, use the following command in your terminal:

bash
Copy code
python pubmed_fetcher.py "your search query"
You can also specify options for debugging and saving the results to a file:

Debug mode: Add the -d or --debug flag to print debug information.
Save results to a file: Use the -f or --file option to specify a file name to save the results.
Example usage:

bash
Copy code
python pubmed_fetcher.py "cancer research" -d -f results.csv
This will fetch the results for "cancer research", enable debug mode, and save the results to results.csv.

Commands and Options
query (required): The search query string to search PubMed.
-d, --debug: Enable debug mode for detailed logs.
-f, --file: Specify a file name to save the results. If not provided, results are printed to the console.
File Structure
graphql
Copy code
pubmed-data-fetcher/
│
├── pubmed_fetcher.py          # Main script for fetching and processing PubMed data
├── requirements.txt           # List of dependencies for the project
├── README.md                  # Project documentation
└── results.csv                # Example output CSV file (optional)
Example Output
The output will include the following details for each paper:

PubmedID: Unique identifier for the paper.
Title: Title of the paper.
Publication Date: Year of publication.
Non-academic Author(s): Authors identified as non-academic (based on affiliation/email).
Company Affiliation(s): Authors identified with company affiliations.
Corresponding Author Email: Email of the corresponding author (if available).
An example of the CSV output:

PubmedID	Title	Publication Date	Non-academic Author(s)	Company Affiliation(s)	Corresponding Author Email
12345678	A study on cancer therapies	2020	John Doe	Jane Smith	jdoe@company.com
23456789	Advances in biotechnology	2019		Bob Johnson	bob.johnson@university.edu
Contribution Guidelines
Fork the repository.
Create a new feature branch (git checkout -b feature-branch).
Commit your changes (git commit -m 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a pull request.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
NCBI PubMed API for providing access to scientific data.
Click for creating command-line interfaces.
Requests for HTTP requests.
CSV module for saving results to CSV.
