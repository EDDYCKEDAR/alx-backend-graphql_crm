import datetime
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=False)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql("""
    query {
      totalCustomers
      totalOrders
      totalRevenue
    }
    """)

    result = client.execute(query)

    with open("/tmp/crm_report_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - Report: {result['totalCustomers']} customers, {result['totalOrders']} orders, {result['totalRevenue']} revenue\n")
