from datetime import datetime
import requests
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    # Setup GraphQL client
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=False)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql("""
    query {
      totalCustomers
      totalOrders
      totalRevenue
    }
    """)

    try:
        result = client.execute(query)
        customers = result.get("totalCustomers", 0)
        orders = result.get("totalOrders", 0)
        revenue = result.get("totalRevenue", 0)
    except Exception as e:
        customers, orders, revenue = 0, 0, 0
        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(f"{datetime.now()} - Error fetching report: {e}\n")
        return

    # Log correctly to /tmp/crm_report_log.txt
    with open("/tmp/crm_report_log.txt", "a") as f:
        f.write(f"{datetime.now()} - Report: {customers} customers, {orders} orders, {revenue} revenue\n")
