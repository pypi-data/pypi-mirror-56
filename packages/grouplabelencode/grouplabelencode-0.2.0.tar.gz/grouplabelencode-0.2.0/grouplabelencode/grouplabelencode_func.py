

def grouplabelencode_loop(data: list, mapping: list, encoding: list,
                          nacode: int = None) -> list:
    out = []
    for label in data:
        enc = nacode
        for idx, c in enumerate(mapping):
            if label in c:
                enc = encoding[idx]
                break
        out.append(enc)
    return out


def grouplabelencode(data: list, mapping: dict, nacode: int = None,
                     nastate: bool = False) -> list:
    """Encode data array with grouped labels

    Parameters:
    -----------
    data : list
        array with labels

    mapping : dict, list of list
        the index of each element is used as encoding.
        Each element is a single label (str) or list
        of labels that are mapped to the encoding.

    nacode : integer
        (Default: None) Encoding for unmapped states.

    nastate : bool
        If False (Default) unmatched data labels are encoded as nacode.
        If nastate=True (and nacode=None) then unmatched data labels are
        encoded with the integer nacode=len(mapping).
    """
    # What value is used for missing data?
    if nastate:
        if nacode is None:
            nacode = len(mapping)

    # Process depending on the data type of the data mapping variable
    if isinstance(mapping, list):
        m = mapping
        e = list(range(len(mapping)))
    elif isinstance(mapping, dict):
        m = list(mapping.values())
        e = list(mapping.keys())
    else:
        raise Exception("'data' must be list-of-list or dict.")

    # Convert scalar elements into a list
    m = [[c] if isinstance(c, (str, int, float)) else c for c in m]

    # Loop over 'data' array
    return grouplabelencode_loop(data, m, e, nacode=nacode)
