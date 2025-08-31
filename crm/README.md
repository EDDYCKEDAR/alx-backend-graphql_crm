# CRM System with Celery Task Scheduling

This Django CRM system includes automated weekly report generation using Celery and Redis for background task processing.

## Prerequisites

- Python 3.8+
- Django 4.2+
- Redis server
- GraphQL schema configured

## Installation and Setup

### 1. Install Redis

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

**macOS (using Homebrew):**
```bash
brew install redis
brew services start redis
```

**Windows:**
Download and install Redis from the official website or use Docker.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Django Setup

Run database migrations:
```bash
python manage.py migrate
```

Create Django-Celery-Beat tables:
```bash
python manage.py migrate django_celery_beat
```

### 4. Verify Redis Connection

Test Redis connection:
```bash
redis-cli ping
```
You should see `PONG` as response.

## Running the Application

### 1. Start Django Development Server

```bash
python manage.py runserver
```

### 2. Start Celery Worker

In a new terminal window:
```bash
celery -A crm worker -l info
```

### 3. Start Celery Beat Scheduler

In another terminal window:
```bash
celery -A crm beat -l info
```

## Scheduled Tasks

### CRM Report Generation

- **Task:** `generate_crm_report`
- **Schedule:** Every Monday at 6:00 AM UTC
- **Function:** Generates a weekly summary of:
  - Total number of customers
  - Total number of orders
  - Total revenue (sum of all order amounts)

### Manual Task Execution

You can manually trigger the report generation:

```bash
# Using Django shell
python manage.py shell
>>> from crm.tasks import generate_crm_report
>>> result = generate_crm_report.delay()
>>> print(result.get())
```

Or using Celery command:
```bash
celery -A crm call crm.tasks.generate_crm_report
```

## Monitoring and Logs

### Check Report Logs

View the generated reports:
```bash
cat /tmp/crm_report_log.txt
```

Example log output:
```
2024-08-31 06:00:01 - Report: 150 customers, 45 orders, $12750.50 revenue.
2024-09-07 06:00:01 - Report: 163 customers, 52 orders, $14230.75 revenue.
```

### Monitor Celery Tasks

#### Celery Flower (Optional Monitoring Tool)

Install Flower for a web-based monitoring interface:
```bash
pip install flower
celery -A crm flower
```

Access the monitoring dashboard at `http://localhost:5555`

#### Check Task Status

```python
# In Django shell
from celery.result import AsyncResult
from crm.tasks import generate_crm_report

# Get task result
result = generate_crm_report.delay()
print(f"Task ID: {result.id}")
print(f"Task Status: {result.status}")
print(f"Task Result: {result.get()}")
```

## GraphQL Integration

The CRM report task integrates with your GraphQL schema by:

1. Fetching customer count using Django ORM
2. Fetching order count using Django ORM  
3. Calculating total revenue by summing `totalamount` from orders
4. Formatting and logging the results

### Testing GraphQL Queries

You can test the underlying data queries in GraphQL playground:

```graphql
query {
  customers {
    edges {
      node {
        id
        name
      }
    }
  }
  orders {
    edges {
      node {
        id
        totalamount
      }
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **Redis Connection Error:**
   - Ensure Redis server is running: `redis-cli ping`
   - Check Redis configuration in `settings.py`

2. **Celery Worker Not Starting:**
   - Check for import errors in tasks
   - Verify Django settings are properly configured
   - Ensure all dependencies are installed

3. **Tasks Not Executing:**
   - Verify Celery Beat is running
   - Check beat schedule configuration
   - Monitor Celery worker logs for errors

4. **Permission Errors for Log File:**
   - Ensure write permissions for `/tmp/` directory
   - Alternative: Change log path in `tasks.py` to a writable location

### Debugging Commands

```bash
# Check Celery configuration
celery -A crm inspect conf

# List active tasks
celery -A crm inspect active

# Check scheduled tasks
celery -A crm inspect scheduled

# Purge all tasks
celery -A crm purge
```

## Development Notes

- The task uses Django ORM instead of direct GraphQL queries for better performance
- Logs are written to `/tmp/crm_report_log.txt` with timestamps
- Error handling includes both file logging and Django logging
- The schedule can be modified in `settings.py` under `CELERY_BEAT_SCHEDULE`

## Production Considerations

1. **Redis Security:** Configure Redis authentication and network security
2. **Log Rotation:** Implement log rotation for report files
3. **Monitoring:** Use tools like Flower or Datadog for production monitoring
4. **Error Handling:** Set up email notifications for task failures
5. **Scaling:** Consider using multiple worker processes for high-volume tasks

## File Structure

```
crm/
├── __init__.py
├── celery.py
├── settings.py
├── tasks.py
├── README.md
└── requirements.txt
```
