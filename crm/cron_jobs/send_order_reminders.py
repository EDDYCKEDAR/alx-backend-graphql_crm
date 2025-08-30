import sys
import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL client setup
transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=False)
client = Client(transport=transport, fetch_schema_from_transport=True)

# Calculate cutoff
cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")

query = gql("""
query {
  orders(filter: { orderDate_Gte: "%s" }) {
    id
    customer {
      email
    }
  }
}
""" % cutoff_date)

result = client.execute(query)
orders = result.get("orders", [])

with open("/tmp/order_reminders_log.txt", "a") as log:
    for order in orders:
        log.write(f"{datetime.datetime.now()} - Order {order['id']} - {order['customer']['email']}\n")

print("Order reminders processed!")
