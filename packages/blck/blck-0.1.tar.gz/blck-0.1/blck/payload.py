def decode(payload):
    """Decode the payload and return it."""
    try:
        for p in payload:
            if p[1] == 1:
                return int(p[2])
            else:
                return payload
    except (Exception,) as error:
        print("Error decoding payload data", error)
        