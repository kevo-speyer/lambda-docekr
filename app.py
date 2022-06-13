import json
import requests
import pandas as pd

def handler(event, context):
    ret_dolar = max_compra(event)
    ret = {
        'statusCode': 200,
        'body': json.dumps(f'Hello from Dockerized-Lambda!\nMax Dolar value {ret_dolar}'),
        'dolar' : json.dumps(ret_dolar),
        'event': json.dumps(event),
        'context': json.dumps(print(context))
    }
    return ret
    
def max_compra(event):
    
    def invert_date(date):
        return '-'.join(date.split('-')[::-1])

    from_date = event.get('from')
    to_date = event.get('to')
    from_date = invert_date(from_date) if from_date else invert_date('2022-01-01')
    to_date = invert_date(to_date) if to_date else invert_date('2022-05-05')

    url = f'https://mercados.ambito.com//dolar/informal/historico-general/{from_date}/{to_date}'
    r = requests.get(url=url)

    df = pd.DataFrame(r.json()[1:])
    df.columns = ['fecha','compra','venta']
    df['fecha'] = df.fecha.apply(invert_date)
    df['compra'] = df.compra.apply(lambda x: float(x.replace(",",".")))
    df['venta'] = df.venta.apply(lambda x: float(x.replace(",",".")))

    ret = df[df.compra==df.compra.max()].sort_values(by='fecha',ascending=False).head(1).to_dict()
    max_compra = {k: list(v.values()).pop() for k,v in ret.items()}
    
    return max_compra
