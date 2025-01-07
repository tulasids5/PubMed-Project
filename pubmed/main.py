import click
import requests
import csv
from typing import Optional, List, Dict
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus


# Utility functions
def build_search_url(query: str) -> str:
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    # Encode the query to ensure it is passed correctly to PubMed
    encoded_query = quote_plus(query)
    params = f"?db=pubmed&term={encoded_query}&retmode=json&retmax=10"
    return base_url + params


def build_fetch_url(pmids: List[str]) -> str:
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    pmid_list = ",".join(pmids)
    params = f"?db=pubmed&id={pmid_list}&retmode=xml"
    return base_url + params


def parse_papers(data: dict) -> List[str]:
    return data.get("esearchresult", {}).get("idlist", [])


def is_non_academic(affiliation: str, email: str) -> bool:
    # Heuristic to determine if the author is non-academic based on affiliation or email.
    non_academic_keywords = ["pharma", "biotech", "company", "corporation", "industry", "startup"]
    academic_keywords = ["university", "research", "institute", "lab", "college"]

    # Check affiliation and email for non-academic keywords
    if any(keyword.lower() in affiliation.lower() for keyword in non_academic_keywords):
        return True
    if any(keyword.lower() in affiliation.lower() for keyword in academic_keywords):
        return False
    if "@" in email:  # If email is present, check the domain
        domain = email.split("@")[-1]
        if any(domain.endswith(kw) for kw in ["company.com", "pharma.com", "startup.com"]):
            return True
    return False


def extract_paper_details(xml_data: str) -> List[Dict[str, str]]:
    root = ET.fromstring(xml_data)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        paper = {
            "PubmedID": article.findtext(".//PMID", default="N/A"),
            "Title": article.findtext(".//ArticleTitle", default="N/A"),
            "Publication Date": article.findtext(".//PubDate/Year", default="N/A"),
            "Non-academic Author(s)": [],
            "Company Affiliation(s)": [],
            "Corresponding Author Email": "N/A",
        }

        # Iterate over authors and check for non-academic authors
        for author in article.findall(".//Author"):
            affiliation = author.findtext(".//AffiliationInfo/Affiliation", default="")
            email = author.findtext(".//Email", default="")  # Extract email if available
            last_name = author.findtext("LastName", default="N/A")
            first_name = author.findtext("ForeName", default="N/A")
            
            if is_non_academic(affiliation, email):
                paper["Non-academic Author(s)"].append(f"{first_name} {last_name}")
            else:
                paper["Company Affiliation(s)"].append(f"{first_name} {last_name}")

        paper["Non-academic Author(s)"] = ", ".join(paper["Non-academic Author(s)"])
        paper["Company Affiliation(s)"] = ", ".join(paper["Company Affiliation(s)"])
        papers.append(paper)

    return papers


def fetch_papers(query: str, debug: bool = False) -> List[Dict[str, str]]:
    search_url = build_search_url(query)
    if debug:
        print(f"Fetching search results from: {search_url}")
    search_response = requests.get(search_url)
    if search_response.status_code != 200:
        if debug:
            print(f"Search API failed with status code: {search_response.status_code}")
        return []

    search_data = search_response.json()
    pmids = parse_papers(search_data)
    if not pmids:
        if debug:
            print("No PMIDs found.")
        return []

    fetch_url = build_fetch_url(pmids)
    if debug:
        print(f"Fetching paper details from: {fetch_url}")
    fetch_response = requests.get(fetch_url)
    if fetch_response.status_code != 200:
        if debug:
            print(f"Fetch API failed with status code: {fetch_response.status_code}")
        return []

    return extract_paper_details(fetch_response.text)


def save_to_csv(papers: List[Dict[str, str]], filename: str) -> None:
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = [
            "PubmedID",
            "Title",
            "Publication Date",
            "Non-academic Author(s)",
            "Company Affiliation(s)",
            "Corresponding Author Email",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(papers)


@click.command()
@click.argument('query', type=str)
@click.option('-d', '--debug', is_flag=True, help="Enable debug mode.")
@click.option('-f', '--file', type=str, default=None, help="File to save results.")
def main(query: str, debug: bool, file: Optional[str]):
    if debug:
        print(f"Starting fetch for query: {query}")

    papers = fetch_papers(query, debug)
    if not papers:
        print("No results found for the query.")
        return

    if file:
        save_to_csv(papers, file)
        print(f"Results saved to {file}")
    else:
        print("Results:")
        for paper in papers:
            print(paper)


if __name__ == '__main__':
    main()
