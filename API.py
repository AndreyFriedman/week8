import requests
import xmltodict

URL = "http://knesset.gov.il/Odata/ParliamentInfo.svc/KNS_Bill()?$filter=SubTypeID%20eq%2054&$expand=KNS_BillInitiators"


def get_data():

    response = requests.get(URL)
    response.raise_for_status()
    xml_data = xmltodict.parse(response.content)
    xml_data_entry = xml_data.get('feed').get('entry')
    return xml_data_entry