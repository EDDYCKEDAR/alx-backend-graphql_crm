#!/bin/bash

# Navigate to project root
cd "$(dirname "$0")/../.."

# Run Django shell command
deleted_count=$(python3 manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer
cutoff = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(orders__isnull=True, created_at__lt=cutoff)
count = qs.count()
qs.delete()
print(count)
")

# Log with timestamp
echo \"$(date '+%Y-%m-%d %H:%M:%S') - Deleted $deleted_count inactive customers\" >> /tmp/customer_cleanup_log.txt
