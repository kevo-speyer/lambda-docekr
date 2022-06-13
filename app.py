import json
import requests
import pandas as pd


def handler(event, context):
    """Lambda app entrypoint"""

    ret_dolar = max_compra(event)
    body = f"Hello from Dockerized-Lambda! Max Dolar value {ret_dolar}"
    ret = {"statusCode": 200, "body": json.dumps(body)}

    return ret


def read_query(event):
    """Normalize query string depending on source"""

    if "queryStringParameters" in event:  # Source: API Gateway
        query = event["queryStringParameters"]
    else:  # Direct Lambda call (Tests)
        query = event

    return query


def max_compra(event):
    """Get max exchange rate from peso to dollar"""

    def invert_date(date):
        return "-".join(date.split("-")[::-1])

    # Set date range
    query = read_query(event)
    from_date = query.get("from")
    to_date = query.get("to")

    from_date = invert_date(from_date) if from_date else invert_date("2022-01-01")
    to_date = invert_date(to_date) if to_date else invert_date("2022-05-05")

    # Request historical exchange rate data in date range
    url = f"https://mercados.ambito.com//dolar/informal/historico-general/{from_date}/{to_date}"
    r = requests.get(url=url)

    # Get maximum value and it's date. In case of tie, most recent wins
    df = pd.DataFrame(r.json()[1:])
    df.columns = ["fecha", "compra", "venta"]
    df["fecha"] = df.fecha.apply(invert_date)
    df["compra"] = df.compra.apply(lambda x: float(x.replace(",", ".")))
    df["venta"] = df.venta.apply(lambda x: float(x.replace(",", ".")))

    ret = (
        df[df.compra == df.compra.max()]
        .sort_values(by="fecha", ascending=False)
        .head(1)
        .to_dict()
    )
    max_compra = {k: list(v.values()).pop() for k, v in ret.items()}

    return max_compra
