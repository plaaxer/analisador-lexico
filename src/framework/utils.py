def parse_entries(text):
    """
        def-reg1: ER1
        def-reg2: ER2
        ...
        def-regn: ERn
    {def-regn: ERn, ...}
    """
    result = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or ':' not in line:
            continue
        key, value = line.split(':', 1)
        result[key.strip()] = value.strip()
    return result