import requests
from bs4 import BeautifulSoup
from semantic_kernel.functions.kernel_function_decorator import kernel_function


class PubMedPlugin:

    PUBMED_API_KEY = "ffcfa5c634e8e7378ee0824f5fd261bf4308"
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def _esearch_ids(self, term: str, retmax: int) -> list:
        """Internal method to perform esearch and return PMIDs."""
        if not term:
            return []
        url = f"{self.BASE_URL}/esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": term,
            "retmax": retmax,
            "retmode": "json",
            "sort": "relevance",
            "api_key": self.PUBMED_API_KEY
        }
        try:
            response = requests.get(url, params=params).json()
            return response.get("esearchresult", {}).get("idlist", [])
        except Exception as e:
            return []

    @kernel_function(name="esearch", description="Search for PubMed articles by term")
    def esearch(self, term: str, retmax: int = 5) -> str:
        if not term:
            return "❌ Error: Search term is required."
        ids = self._esearch_ids(term, retmax)
        if not ids:
            return "❌ No results found."
        urls = [f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" for pmid in ids]
        return "\n".join([f"📄 PMID: {pmid} 🔗 {url}" for pmid, url in zip(ids, urls)])

    @kernel_function(name="efetch", description="Fetch article details using term or PMIDs")
    def efetch(self, term_or_pmid: str, retmax: int = 1) -> str:
        if not term_or_pmid:
            return "❌ Error: Parameter 'term_or_pmid' is required."

        if "," in term_or_pmid:
            pmids = [pmid.strip() for pmid in term_or_pmid.split(",") if pmid.strip().isdigit()]
        elif term_or_pmid.isdigit():
            pmids = [term_or_pmid]
        else:
            pmids = self._esearch_ids(term_or_pmid, retmax)

        if not pmids:
            return "❌ No PMIDs found."

        results = []
        for pmid in pmids:
            url = f"{self.BASE_URL}/efetch.fcgi"
            params = {
                "db": "pubmed",
                "id": pmid,
                "retmode": "xml",
                "api_key": self.PUBMED_API_KEY
            }
            try:
                response = requests.get(url, params=params)
                soup = BeautifulSoup(response.text, "lxml-xml")
                title = soup.find("ArticleTitle")
                abstract = soup.find("AbstractText")
                pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                results.append(
                    f"📄 PMID: {pmid}\n🔗 URL: {pubmed_url}\n📝 Title: {title.text if title else 'N/A'}\n📘 Abstract: {abstract.text if abstract else 'N/A'}"
                )
            except Exception as e:
                results.append(f"❌ Error fetching article with PMID {pmid}: {str(e)}")

        return "\n\n".join(results)

    @kernel_function(name="esummary", description="Get summary metadata using term or PMIDs")
    def esummary(self, term_or_pmid: str, retmax: int = 1) -> str:
        if not term_or_pmid:
            return "❌ Error: Parameter 'term_or_pmid' is required."

        pmids = self._esearch_ids(term_or_pmid, retmax) if not term_or_pmid.isdigit() else [term_or_pmid]
        if not pmids:
            return "❌ No PMIDs found."

        results = []
        for pmid in pmids:
            url = f"{self.BASE_URL}/esummary.fcgi"
            params = {
                "db": "pubmed",
                "id": pmid,
                "retmode": "json",
                "api_key": self.PUBMED_API_KEY
            }
            try:
                response = requests.get(url, params=params).json()
                summary = response.get("result", {}).get(pmid, {})
                title = summary.get("title", "N/A")
                authors = summary.get("authors", [])
                authors_list = ", ".join([a.get("name", "") for a in authors])
                pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                results.append(
                    f"📄 PMID: {pmid}\n🔗 URL: {pubmed_url}\n📝 Title: {title}\n👥 Authors: {authors_list}"
                )
            except Exception as e:
                results.append(f"❌ Error fetching summary for PMID {pmid}: {str(e)}")
        return "\n\n".join(results)

    @kernel_function(name="elink", description="Get related articles using term or PMIDs")
    def elink(self, term_or_pmid: str, retmax: int = 5) -> str:
        if not term_or_pmid:
            return "❌ Error: Parameter 'term_or_pmid' is required."

        pmids = self._esearch_ids(term_or_pmid, 1) if not term_or_pmid.isdigit() else [term_or_pmid]
        pmid = pmids[0] if pmids else None
        if not pmid:
            return "❌ No PMIDs found."

        url = f"{self.BASE_URL}/elink.fcgi"
        params = {
            "dbfrom": "pubmed",
            "id": pmid,
            "retmode": "json",
            "api_key": self.PUBMED_API_KEY
        }
        try:
            response = requests.get(url, params=params).json()
            linksets = response.get("linksets", [])
            links = linksets[0].get("linksetdbs", [])[0].get("links", []) if linksets else []
            related = links[:retmax]
            result_lines = [
                f"📄 Related Article:\n📄 PMID: {r}\n🔗 URL: https://pubmed.ncbi.nlm.nih.gov/{r}/"
                for r in related
            ]
            return f"🔍 Based on article PMID {pmid}\n\n" + "\n\n".join(result_lines) if result_lines else "ℹ️ No related articles found."
        except Exception as e:
            return f"❌ Error fetching related articles: {str(e)}"
