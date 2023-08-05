from .utils import parse_query, enhanced_css
from .x_processors import x


def _parsel_one(sel, query: str, **kwargs):
    """Use parsel to extract original values"""
    if not isinstance(query, str):
        raise TypeError(f"Query should be string: {query}")
    q = parse_query(query)
    lang = q["lang"]

    # extract values
    if lang == "xpath":
        val = getattr(getattr(sel, lang)(q["query"], **kwargs), q["meth"])()
    else:
        query = enhanced_css(q["query"])
        val = getattr(getattr(sel, lang)(query), q["meth"])()

    # apply filters function
    filters = q["filters"]
    for filt in filters:
        func = x.filters[filt["name"]]
        val = func(val, *filt["args"])
    return val


def process(sel, queries, **kwargs):

    if isinstance(queries, list):
        if should_divide(queries):
            divider = queries.pop(0)
            d_query = parse_query(divider)
            return [
                process(sel, queries)
                for sel in getattr(sel, d_query["lang"])(d_query["query"])
            ]

        query = queries[0]
        funcs = queries[1:]
        val = process(sel, query, **kwargs)
        return _process_by_funcs(val, funcs)
    elif isinstance(queries, dict):
        return {k: process(sel, v, **kwargs) for k, v in queries.items()}
    else:
        query = queries
        return _parsel_one(sel, query, **kwargs)


def _process_by_funcs(val, funcs=None):
    for func in funcs or []:
        val = func(val)
    return val


def should_divide(queries: list):
    return len(queries) > 1 and not callable(queries[1])
