# CRM Celery Setup

## Setup Instructions

1. **Install Redis**
   ```bash
   sudo apt-get install redis-server
Install dependencies

bash
Copy code
pip install -r requirements.txt
Run migrations

bash
Copy code
python manage.py migrate
Start Celery worker

bash
Copy code
celery -A crm worker -l info
Start Celery Beat

bash
Copy code
celery -A crm beat -l info
Verify logs

bash
Copy code
cat /tmp/crm_report_log.txt
