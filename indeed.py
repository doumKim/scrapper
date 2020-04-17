import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit={LIMIT}"


def extract_indeed_pages():
    result = requests.get(URL)

    soup = BeautifulSoup(result.text, "html.parser")

    pagination = soup.find("div", {"class": "pagination"})

    links = pagination.find_all("a")

    pages = []

    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extarct_job(html):
    title = html.find('h2', {'class': 'title'}).find('a')["title"]
    company = html.find('span', {'class': 'company'})
    company_anchor = company.find("a")
    if company_anchor != None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)
    company = company.strip()
    location = str(html.find('div', {'class': 'recJobLoc'})["data-rc-loc"])
    job_id = html["data-jk"]
    return {
        'tilte':
        title,
        'company':
        company,
        'location':
        location,
        'link':
        f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk={job_id}"
    }


def extract_indeed_jobs(last_page):
    jobs = []
    # for page in range(last_page):
    result = requests.get(f"{URL}&start={0 * LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for result in results:
        job = extarct_job(result)
        jobs.append(job)
        print(jobs)
    return jobs