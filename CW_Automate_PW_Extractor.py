import requests
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--clientid", dest="clientid", metavar="N", type=str, help="the ClientID for this API", )
parser.add_argument("--bearer_token", dest="bearer_token", metavar="N", type=str, help="The bearer token in the format 'bearer asdfasdfasdfasdf'")
parser.add_argument("--base_url", dest="base_url", metavar="N", type=str, help="the org URL, E.g. 'https://myorg.hostedrmm.com'")
parser.add_argument("--output_file", dest="output_file", metavar="N", type=str, help="The name of the csv file to output to, E.g. 'cwa_passwords.csv'")

args = parser.parse_args()

headers = {
    "authorization": args.bearer_token,
    "clientid": args.clientid,
    "accept": "application/json"
}

clientsurl = f"{args.base_url}/cwa/api/v1/clients?pageSize=-1&includeFields=Name&orderBy=Name%20asc"

cwclientids = requests.get(clientsurl, headers=headers)
cwclientids = pd.DataFrame(cwclientids.json())

deploymentloginidsurl = "/cwa/api/v1/clients/{cwclientid}/deploymentlogins?pagesize=-1&condition=&orderBy=title%20asc&includeFields=password,Username,Title,Notes,Url"

jsonlist = []
for cwclientid in cwclientids['Id'].values:
    resp = requests.get(args.base_url+deploymentloginidsurl.format(cwclientid=cwclientid), headers=headers)
    if resp.status_code not in [200, 201, "200", "201"]:
        print(f"Failed to get passwords for cw client id {cwclientid}")
        continue
    jsonlist += resp.json()

df = pd.DataFrame(jsonlist)
df['ClientId'] = df['Client'].apply(lambda x: x['ClientId'])
df['ClientName'] = df['Client'].apply(lambda x: cwclientids.loc[cwclientids['Id'] == str(x['ClientId'])]['Name'].values[0])
df = df[["ClientName", "ClientId","Title", "Username", "Password", "Notes", "Url"]]
df.to_csv(args.output_file, index=False)
