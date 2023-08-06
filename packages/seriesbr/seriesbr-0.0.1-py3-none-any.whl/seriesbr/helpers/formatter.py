from pandas import DataFrame
from .metadata import bcb_metadata_list


def format_search_bcb(response, kwargs):
    json = response.json()
    count = json["result"]["count"]
    search_results = json["result"]["results"]
    assert (
        search_results
    ), "Nothing was found or start result is greater than total results."
    default_metadata = ["codigo_sgs", "title", "periodicidade"]
    selected_metadata = default_metadata + [
        bcb_metadata_list[arg]
        for arg in kwargs.keys()
        if kwargs and bcb_metadata_list[arg] not in default_metadata
    ]
    D = {
        metadata: []
        for metadata in search_results[0].keys()
        if metadata in selected_metadata
    }
    for result in search_results:
        for metadata in selected_metadata:
            D[metadata].append(result[metadata])
    df = DataFrame(D)
    return count, df


def format_search_ipea(response):
    search_results = response.json()["value"]
    assert len(search_results) > 0, "Nothing was found."
    D = {metadata: [] for metadata in search_results[0].keys()}
    for result in search_results:
        for metadata in result.keys():
            D[metadata].append(result[metadata])
    df = DataFrame(D)
    return df
