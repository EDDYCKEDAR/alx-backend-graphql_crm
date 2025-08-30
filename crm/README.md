# CRM Celery Setup

## Setup Instructions
1. Install Redis:
   ```bash
   sudo apt-get install redis-server
Install dependencies:

pip install -r requirements.txt


Run migrations:

python manage.py migrate


Start Celery worker:

celery -A crm worker -l info


Start Celery Beat:

celery -A crm beat -l info


Check logs:

cat /tmp/crm_report_log.txt
