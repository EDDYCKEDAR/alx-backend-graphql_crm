from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    now = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    # Setup GraphQL client
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=False)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Try querying the hello field
    try:
        query = gql(""" query { hello } """)
        result = client.execute(query)
        hello_response = result.get("hello", "No response")
    except Exception as e:
        hello_response = f"GraphQL error: {e}"

    # Log heartbeat with GraphQL response
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(f"{now} CRM is alive - Hello field: {hello_response}\n")
