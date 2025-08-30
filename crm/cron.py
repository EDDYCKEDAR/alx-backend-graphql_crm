import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def update_low_stock():
    # Setup GraphQL client
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=False)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Correct mutation name: updateLowStockProducts
    mutation = gql("""
    mutation {
      updateLowStockProducts {
        success
        updated
      }
    }
    """)

    result = client.execute(mutation)
    updates = result["updateLowStockProducts"]["updated"]

    # Correct log path: /tmp/low_stock_updates_log.txt
    with open("/tmp/low_stock_updates_log.txt", "a") as f:
        for line in updates:
            f.write(f"{datetime.datetime.now()} - {line}\n")
