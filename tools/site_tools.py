from langchain.tools import tool
from query_search.amiami_search import get_search_results as amiami_search
from query_search.solaris_search import get_search_results as solaris_search
from query_search.ninningame_search import get_search_results as ninningame_search
from query_search.animota_search import get_search_results as animota_search
from query_search.goodsmileeurope_search import get_search_results as gsce_search
from query_search.japan_figure_search import get_search_results as jf_search

def format_results(results):
    """Return a newline-separated list of URLs."""
    if not results:
        return "No results found."
    return "\\n".join([r["url"] for r in results[:3]])

@tool
def search_amiami(query: str) -> str:
    """Search AmiAmi for a product. Returns top 3 result URLs."""
    return format_results(amiami_search(query))

@tool
def search_solaris(query: str) -> str:
    """Search Solaris Japan for a product. Returns top 3 result URLs."""
    return format_results(solaris_search(query))

@tool
def search_ninningame(query: str) -> str:
    """Search Nin-Nin Game for a product. Returns top 3 result URLs."""
    return format_results(ninningame_search(query))

@tool
def search_animota(query: str) -> str:
    """Search Animota for a product. Returns top 3 result URLs."""
    return format_results(animota_search(query))

@tool
def search_gsce(query: str) -> str:
    """Search Good Smile Europe for a product. Returns top 3 result URLs."""
    return format_results(gsce_search(query))

@tool
def search_japanfigure(query: str) -> str:
    """Search Japan Figure for a product. Returns top 3 result URLs."""
    return format_results(jf_search(query))
