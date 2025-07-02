from datetime import datetime

def to_mm_yyyy(date_str: str) -> str:
    """
    Converte 'YYYY-MM-DD' → 'MM/YYYY'.

    Parameters
    ----------
    date_str : str
        Data no formato 'YYYY-MM-DD'.

    Returns
    -------
    str
        String no formato 'MM/YYYY'.
    """
    date = datetime.strptime(date_str, "%Y-%m-%d")

    return date.strftime("%m/%Y")
