#!/usr/bin/env python3

"""
This module handles all interaction with NCBI.

The main functionality is provided through the `CDSearch` function, which will take the
initial query, go through the entire search process and return the results. For example,
we can launch a new search:

>>> from synthaser import ncbi
>>> results = ncbi.CDSearch(query_file='queries.fasta')
INFO:synthaser.ncbi:Launching new CDSearch run with: queries.fasta
INFO:synthaser.ncbi:Run ID: QM3-qcdsearch-B4BAD4B59BC5B80-3E7CFCD3F93E21D0
INFO:synthaser.ncbi:Polling NCBI for results...

The query sequences are first sent to the CD-Search API to start a new search. The
parameters for this search are specified by the values in `SEARCH_PARAMS`:

>>> ncbi.SEARCH_PARAMS
{
  'db': 'cdd',
  'smode': 'auto',
  'useid1': 'true',
  'compbasedadj': '1',
  'filter': 'true',
  'evalue': '3.0',
  'maxhit': '500',
  'dmode': 'full',
  'tdata': 'hits'
}

which can be freely edited. Check here_ for a full description of valid values.

.. _here: https://www.ncbi.nlm.nih.gov/Structure/cdd/cdd_help.shtml#BatchRPSBWebAPI_parameters

The API is polled until the search has completed, at which point the results are retrieved.
The function returns the `requests.models.Response` object which is returned by the
`requests` package. Thus, the search results are stored in the `text` attribute:

>>> print(results.text)
#Batch CD-search tool	NIH/NLM/NCBI
#cdsid	QM3-qcdsearch-B4BAD4B59BC5B80-3E7CFCD3F93E21D0
#datatype	hitsFull Results
#status	0
#Start time	2019-09-03T04:21:23	Run time	0:00:04:23
#status	success
...

Searches are saved in the `SEARCH_HISTORY` dictionary, which can be nicely summarised by
calling the `history` function:

>>> ncbi.history()
1.      Run ID: QM3-qcdsearch-B4BAD4B59BC5B80-3E7CFCD3F93E21D0
    Parameters:
                db: cdd
             smode: auto
            useid1: true
      compbasedadj: 1
            filter: true
            evalue: 3.0
            maxhit: 500
             dmode: full
             tdata: hits

Finally, this module provides `efetch_sequences`, a function for fetching sequences from
NCBI from a collection of accessions. For example:

>>> ncbi.efetch_sequences(['CBF71467.1', 'XP_681681.1'])
{'CBF71467.1': 'MQSAGMHRATA...', 'XP_681681.1': 'MQDLIAIVGSA...'}

The accessions are sent to the NCBI's Entrez API, which returns the sequences in FASTA
format. They are parsed using `fasta.parse`, and the resulting dictionary is returned.
"""

import time
import logging
import re

import requests

from synthaser import fasta

LOG = logging.getLogger(__name__)


CDSEARCH_URL = "https://www.ncbi.nlm.nih.gov/Structure/bwrpsb/bwrpsb.cgi?"

SEARCH_PARAMS = {
    "db": "cdd",
    "smode": "auto",
    "useid1": "true",
    "compbasedadj": "1",
    "filter": "true",
    "evalue": "3.0",
    "maxhit": "500",
    "dmode": "full",
    "tdata": "hits",
}

SEARCH_HISTORY = []


def _search_query_file(handle):
    """Launch a new CD-Search job from a query file.

    Checks that file contains less than 4000 sequences, as per NCBI limit.

    Parameters
    ----------
    handle : open file handle
        An open file handle belonging to a query FASTA file.

    Raises
    ------
    ValueError
        If there are more than 4000 sequences in the handle.
    """
    if fasta.count(handle) > 4000:
        raise ValueError("Too many sequences in file (NCBI limit = 4000).")
    return requests.post(CDSEARCH_URL, files={"queries": handle}, data=SEARCH_PARAMS)


def _search_query_ids(ids):
    """Launch a new CD-Search job from a collection of query IDs.

    Parameters
    ----------
    ids : list, tuple
        Collection of valid NCBI sequence identifiers to be searched.

    Raises
    ------
    TypeError
        If `query_ids` is not a list or tuple.
    TypeError
        If values in `query_ids` are not of type `int` or `str`.
    ValueError
        If neither `query_ids` or `query_file` are specified.
    """
    if not isinstance(ids, (list, tuple)):
        raise TypeError("Query IDs must be given in a list or tuple")

    if not all(isinstance(x, (int, str)) for x in ids):
        raise TypeError("Expected a list/tuple of int/str")

    if len(ids) > 4000:
        raise ValueError("Too many sequences in file (NCBI limit = 4000).")

    return requests.post(
        CDSEARCH_URL, params=SEARCH_PARAMS, files={"queries": "\n".join(ids)}
    )


def _search(query_ids=None, query_file=None):
    """Launch new search with either query IDs or file, then return assigned CDSID."""
    if query_file and not query_ids:
        LOG.info("Launching new CDSearch run with: %s", query_file)
        with open(query_file) as handle:
            response = _search_query_file(handle)
    elif query_ids:
        LOG.info("Launching new CDSearch run on IDs: %s", query_ids)
        response = _search_query_ids(query_ids)
    else:
        raise ValueError("A query must be specified with query_file OR query_ids")
    try:
        return re.search(r"#cdsid\t(.+?)\n", response.text).group(1)
    except AttributeError:
        LOG.exception("Search failed; no search ID returned")
        raise


def _check_status(cdsid):
    """Check the status of a running CD-search job.

    CD-Search runs are assigned a unique search ID, which typically take the form::

        QM3-qcdsearch-xxxxxxxxxxx-yyyyyyyyyyy

    This function queries NCBI for the status of a running CD-Search job
    corresponding to the search ID specified by ``cdsid``.

    >>> response = _check_status('QM3-qcdsearch-B4BAD4B59BC5B80-3E7CFCD3F93E21D0')

    If the job has finished, this function will return the ``requests.Response`` object
    which contains the run results. If the job is still running, this function will
    return None. If an error is encountered, a ValueError will be thrown with the
    corresponding error code and message.

    Parameters
    ----------
    cdsid : str
        CD-search job ID.

    Returns
    -------
    requests.models.Response
        If the job has successfully completed (Response contains status code 0).
        This is the object returned by ``requests.get()``; if the search has
        completed, this object will contain the search results in its ``text`` and
        ``contents`` attributes.
    None
        If the job is still running (Response contains status code 3).

    Raises
    ------
    ValueError
        If the returned results file has a successful status code but is actually
        empty (i.e. contains no results), perhaps due to an invalid query.
    ValueError
        When a status code of 1, 2, 4 or 5 is returned from the request.
    """
    response = requests.get(
        CDSEARCH_URL, params={"cdsid": cdsid, "dmode": "full", "tdata": "hits"}
    )
    code = re.search(r"#status\t([012345])[\n\t]", response.text).group(1)
    if code == "0":
        if response.text.endswith("Superfamily\n"):
            raise ValueError("Empty results file; perhaps invalid query?")
        return response
    if code == "3":
        return None
    errors = {
        "1": "Invalid search ID",
        "2": "No effective input (usually no query proteins or search ID specified)",
        "4": "Queue manager (qman) service error",
        "5": "Data is corrupted or no longer available (cache cleaned, etc)",
    }
    raise ValueError(f"Request failed; NCBI returned code {code} ({errors[code]})")


def _retrieve_results(cdsid, max_retries=-1, delay=20):
    """Poll CDSearch for results.

    This method queries the NCBI for results from a CDSearch job corresponding to
    the supplied ``cdsid``. If ``max_retries`` is -1, this function will check for
    results every ``delay`` interval until something is returned.

    If you wish to save the results of a CD-Search run to file, you can supply an
    open file handle via the ``output`` parameter:

    >>> with open('results.tsv', 'w') as results:
    ...     _retrieve_results(
    ...         'QM3-qcdsearch-B4BAD4B59BC5B80-3E7CFCD3F93E21D0',
    ...         output=results
    ...     )

    This function returns the ``Response`` object returned by
    ``CDSearch.check_status()``:

    >>> response = _retrieve_results('QM3-qcdsearch-B4BAD4B59BC5B80-3E7CFCD3F93E21D0')
    >>> print(response.text)
    #Batch CD-search tool	NIH/NLM/NCBI
    #cdsid	QM3-qcdsearch-B4BAD4B59BC5B80-3E7CFCD3F93E21D0
    #datatype	hitsFull Results
    #status	0
    ...

    Parameters
    ----------
    cdsid : str
        CD-search job ID. Looks like ``QM3-qcdsearch-xxxxxxxxxxx-yyyyyyyyyyy``.
    output : open file handle
        Save results to a given open file handle instead of a local file. This
        facilitates usage of e.g. tempfile objects.
    max_retries : int
        Maximum number of retries for checking job completion. If -1 is given, this
        function will keep paging for results until something is returned.
    delay : int
        Number of seconds to wait between each request to the NCBI. The wait time is
        re-calculated to this value each time, based on the time taken by the
        previous request. By default, this is set to 20; giving a value less than 10
        will result in a ValueError being thrown.

    Returns
    -------
    response : requests.Response
        Response returned by the ``requests.get()`` in ``CDSearch.check_status()``.

    Raises
    -------
    ValueError
        If ``delay`` is < 10.
    ValueError
        If no Response model is returned by self.check_status()
    """
    if delay < 10:
        raise ValueError("Delay must be at least 10s")
    retries, previous = 0, 0
    while True:
        current = time.time()
        wait = previous + delay - current
        if wait > 0:
            time.sleep(wait)
            previous = current + wait
        else:
            previous = current
        LOG.info("Checking search status...")
        response = _check_status(cdsid)
        if response:
            LOG.info("Search successfully completed!")
            break
        if max_retries > 0 and retries == max_retries:
            LOG.error("Maximum retry limit (%i) exceeded, breaking", max_retries)
            break
        retries += 1
    if not response:
        raise ValueError("No results were returned")
    return response


def history():
    """Print out summary of previously saved CD-Search runs.

    The parameters and results of prior searches are stored in `SEARCH_HISTORY`, which
    is simply a list of dictionaries:

    >>> ncbi.SEARCH_HISTORY
    [{'cdsid': 'QM3-qcdsearch-C7558163144A288-147D9ECB39A09F8B',
    'parameters': {'db': 'cdd', 'smode': 'auto', 'useid1': 'true', 'compbasedadj': '1',
    'filter': 'true', 'evalue': '3.0', 'maxhit': '500', 'dmode': 'full', 'tdata':
    'hits'}, 'results': <Response [200]>}]

    This function simply formats the entries in `SEARCH_HISTORY` nicely:

    >>> ncbi.history()
    1.      Run ID: QM3-qcdsearch-B4BAD4B59BC5B80-3E7CFCD3F93E21D0
        Parameters:
                    db: cdd
                 smode: auto
                useid1: true
          compbasedadj: 1
                filter: true
                evalue: 3.0
                maxhit: 500
                 dmode: full
                 tdata: hits

    Raises
    ------
    ValueError
        If `SEARCH_HISTORY` is empty (i.e. no searches have been run).
    """
    if not SEARCH_HISTORY:
        raise ValueError("No searches have been run")

    slen = max(len(key) for key in SEARCH_PARAMS)

    for index, run in enumerate(SEARCH_HISTORY, 1):
        print(
            f"{f'{index}.':8}Run ID: {run['cdsid']}\n    Parameters:\n"
            + "\n".join(
                f"{setting:>{slen+6}}: {value}"
                for setting, value in run["parameters"].items()
            )
        )


def CDSearch(
    query_file=None, query_ids=None, cdsid=None, output=None, delay=20, max_retries=-1
):
    """Launch a new CD-Search job.

    This function takes a query FASTA file or collection of NCBI sequence
    identifiers, sends them to the CD-Search server and then polls for response until
    one is returned.

    >>> results = CDSearch(query_file='path/to/query.fasta')
    >>> results = CDSearch(query_ids=['XP_000000001.1', ... ])
    >>> results
    <Response [200]>

    Search parameters are specified in `SEARCH_PARAMS`. For example, to adjust the
    e-value cutoff used in the search, simply change it there:

    >>> SEARCH_PARAMS['evalue'] = 2.0

    Then, future searches will use the updated value.
    """
    if not cdsid:
        cdsid = _search(query_ids=query_ids, query_file=query_file)

    LOG.info("Run ID: %s", cdsid)
    LOG.info("Polling NCBI for results...")
    results = _retrieve_results(cdsid, delay=delay, max_retries=max_retries)

    SEARCH_HISTORY.append(
        {"cdsid": cdsid, "parameters": SEARCH_PARAMS, "results": results}
    )

    if output:
        LOG.info("Writing results to %s", output)
        with open(output, "w") as handle:
            handle.write(results.text)

    return results


def efetch_sequences(headers):
    """Retrieve protein sequences from NCBI for supplied accessions.

    This function uses EFetch from the NCBI E-utilities to retrieve the sequences for
    all synthases specified in `headers`. It then calls `fasta.parse` to parse the
    returned response; note that extra processing has to occur because the returned
    FASTA will contain a full sequence description in the header line after the
    accession.

    Parameters
    ----------
    headers : list, tuple
        A list of valid NCBI sequence identifiers (accession, GI, etc). Should
        correspond to an entry in the Protein database.
    """
    response = requests.post(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?",
        params={"db": "protein", "rettype": "fasta"},
        files={"id": ",".join(headers)},
    )
    if response.status_code != 200:
        raise requests.HTTPError(
            f"Error fetching sequences from NCBI [code {response.status_code}]."
            " Bad query IDs?"
        )
    sequences = {}
    for key, value in fasta.parse(response.text.split("\n")).items():
        for header in headers:
            if header not in sequences and header in key:
                sequences[header] = value
                break
    return sequences


def set_search_params(
    db=None,
    smode=None,
    useid1=None,
    compbasedadj=None,
    filter=None,
    evalue=None,
    maxhit=None,
    dmode=None,
):
    """Set CD-Search search parameters."""
    for kw, value in locals().items():
        if not value:
            continue
        SEARCH_PARAMS[kw] = value
