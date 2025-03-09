---
description: Guide to automating BanglaNLP for continuous dataset updates and maintenance
title: Automation - BanglaNLP
tags:
  - automation
  - scheduling
  - continuous integration
---

# Automation

This guide explains how to automate BanglaNLP for continuous dataset updates, scheduled scraping, and maintenance tasks.

## Scheduled Scraping

### Using Cron Jobs (Linux/macOS)

Cron is a time-based job scheduler in Unix-like operating systems. You can use it to run BanglaNLP scraping scripts on a regular schedule.

1. Create a shell script for the scraping task:

   ```bash
   # scrape_daily.sh
   #!/bin/bash
   
   # Navigate to the BanglaNLP directory
   cd /path/to/BanglaNLP
   
   # Activate virtual environment if needed
   source venv/bin/activate
   
   # Run the scraper with desired options
   python main.py --max-articles 100 --output data/$(date +%Y-%m-%d)
   
   # Build and upload the dataset
   python main.py --build --upload --hf-repo yourusername/bengali-english-news
   
   # Log completion
   echo "Scraping completed on $(date)" >> logs/cron.log
   ```

2. Make the script executable:

   ```bash
   chmod +x scrape_daily.sh
   ```

3. Add a cron job to run the script daily at 2 AM:

   ```bash
   crontab -e
   ```

   Add this line:

   ```
   0 2 * * * /path/to/BanglaNLP/scrape_daily.sh
   ```

### Using Task Scheduler (Windows)

On Windows, you can use Task Scheduler to automate BanglaNLP:

1. Create a batch script for the scraping task:

   ```batch
   @echo off
   REM scrape_daily.bat
   
   REM Navigate to the BanglaNLP directory
   cd /d C:\path\to\BanglaNLP
   
   REM Activate virtual environment if needed
   call venv\Scripts\activate.bat
   
   REM Run the scraper with desired options
   python main.py --max-articles 100 --output data\%date:~-4,4%-%date:~-7,2%-%date:~-10,2%
   
   REM Build and upload the dataset
   python main.py --build --upload --hf-repo yourusername/bengali-english-news
   
   REM Log completion
   echo Scraping completed on %date% %time% >> logs\cron.log
   ```

2. Open Task Scheduler (taskschd.msc)
3. Create a new task:
   - Triggers: Daily at 2:00 AM
   - Actions: Start a program > Browse to your batch file
   - Conditions: Start only if the computer is idle
   - Settings: Run task as soon as possible after a scheduled start is missed

## Docker Automation

For consistent environment and easier deployment, use Docker:

1. Create a Dockerfile:

   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY . .
   RUN pip install -r requirements.txt
   
   # Environment variables
   ENV BANGLA_NLP_OUTPUT_DIR=/app/data
   ENV HUGGINGFACE_TOKEN=${HUGGINGFACE_TOKEN}
   
   # Default command
   CMD ["python", "main.py"]
   ```

2. Build the Docker image:

   ```bash
   docker build -t bangla-nlp .
   ```

3. Run the container with custom parameters:

   ```bash
   docker run -v $(pwd)/data:/app/data -e HUGGINGFACE_TOKEN=your_token bangla-nlp python main.py --sources prothomalo
   ```

4. Set up a scheduled task to run the Docker container.

### Docker Compose

For more complex setups, use Docker Compose:

```yaml
# docker-compose.yml
version: '3'

services:
  scraper:
    build: .
    volumes:
      - ./data:/app/data
    environment:
      - HUGGINGFACE_TOKEN=${HUGGINGFACE_TOKEN}
    command: python main.py --sources prothomalo ittefaq --max-articles 200
    restart: unless-stopped
```

Run with:

```bash
docker-compose up -d
```

## GitHub Actions

You can use GitHub Actions to automate scraping and dataset updates:

1. Create a GitHub Actions workflow file:

   ```yaml
   # .github/workflows/scrape-daily.yml
   name: Daily Scraping
   
   on:
     schedule:
       - cron: '0 2 * * *'  # Run at 2 AM UTC daily
     workflow_dispatch:     # Allow manual triggering
   
   jobs:
     scrape-and-update:
       runs-on: ubuntu-latest
       
       steps:
       - uses: actions/checkout@v3
       
       - name: Set up Python
         uses: actions/setup-python@v4
         with:
           python-version: '3.9'
       
       - name: Install dependencies
         run: |
           python -m pip install --upgrade pip
           pip install -r requirements.txt
       
       - name: Run scraper
         run: python main.py --max-articles 100 --output data/$(date +%Y-%m-%d)
       
       - name: Build dataset
         run: python main.py --build
       
       - name: Upload to Hugging Face
         env:
           HUGGINGFACE_TOKEN: ${{ secrets.HUGGINGFACE_TOKEN }}
         run: python main.py --upload --hf-repo yourusername/bengali-english-news
       
       - name: Commit changes
         run: |
           git config --local user.email "actions@github.com"
           git config --local user.name "GitHub Actions"
           git add data/
           git commit -m "Update dataset - $(date +%Y-%m-%d)" || echo "No changes to commit"
       
       - name: Push changes
         uses: ad-m/github-push-action@master
         with:
           github_token: ${{ secrets.GITHUB_TOKEN }}
           branch: ${{ github.ref }}
   ```

2. Add the `HUGGINGFACE_TOKEN` secret in your GitHub repository settings.

## Incremental Updates

For efficiency, implement incremental updates to only scrape new content:

1. Create a state tracker script:

   ```python
   # scripts/incremental_update.py
   import json
   import os
   from datetime import datetime
   import argparse
   
   def load_state(state_file):
       if os.path.exists(state_file):
           with open(state_file, 'r') as f:
               return json.load(f)
       return {'last_run': None, 'sources': {}}
   
   def save_state(state, state_file):
       with open(state_file, 'w') as f:
           json.dump(state, f, indent=2)
   
   def main():
       parser = argparse.ArgumentParser(description='Incremental dataset update')
       parser.add_argument('--state-file', default='state.json', help='State file path')
       parser.add_argument('--output', default='data/incremental', help='Output directory')
       args = parser.parse_args()
       
       # Load previous state
       state = load_state(args.state_file)
       
       # Run the scraper with incremental mode
       from main import run_scrapers
       sources_state = run_scrapers(
           incremental=True, 
           last_run_state=state['sources'],
           output_dir=args.output
       )
       
       # Update state
       state['last_run'] = datetime.now().isoformat()
       state['sources'] = sources_state
       save_state(state, args.state_file)
       
   if __name__ == '__main__':
       main()
   ```

2. Run the incremental update script:

   ```bash
   python scripts/incremental_update.py --state-file state.json --output data/incremental
   ```

## Monitoring and Alerting

Implement monitoring to ensure your automated scraping is working properly:

1. Create a health check script:

   ```python
   # scripts/health_check.py
   import os
   import json
   import argparse
   import smtplib
   from email.mime.text import MIMEText
   from datetime import datetime, timedelta
   
   def send_alert(subject, message, recipient):
       msg = MIMEText(message)
       msg['Subject'] = subject
       msg['From'] = 'alerts@yourdomain.com'
       msg['To'] = recipient
       
       smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
       smtp_port = int(os.environ.get('SMTP_PORT', 587))
       smtp_user = os.environ.get('SMTP_USER')
       smtp_pass = os.environ.get('SMTP_PASS')
       
       with smtplib.SMTP(smtp_server, smtp_port) as server:
           server.starttls()
           server.login(smtp_user, smtp_pass)
           server.send_message(msg)
   
   def check_dataset_health(data_dir, state_file, recipient):
       # Check state file recency
       if os.path.exists(state_file):
           with open(state_file, 'r') as f:
               state = json.load(f)
               last_run = datetime.fromisoformat(state['last_run'])
               if datetime.now() - last_run > timedelta(days=2):
                   send_alert(
                       'BanglaNLP Alert: No Recent Updates',
                       f'Last update was on {last_run}',
                       recipient
                   )
       else:
           send_alert(
               'BanglaNLP Alert: State File Missing',
               f'State file not found at {state_file}',
               recipient
           )
       
       # Check data file creation dates
       newest_file = None
       newest_time = None
       for root, _, files in os.walk(data_dir):
           for file in files:
               if file.endswith('.json'):
                   path = os.path.join(root, file)
                   mtime = os.path.getmtime(path)
                   if newest_time is None or mtime > newest_time:
                       newest_time = mtime
                       newest_file = path
       
       if newest_time and datetime.fromtimestamp(newest_time) < datetime.now() - timedelta(days=2):
           send_alert(
               'BanglaNLP Alert: No New Data Files',
               f'Most recent data file ({newest_file}) was created on {datetime.fromtimestamp(newest_time)}',
               recipient
           )
   
   if __name__ == '__main__':
       parser = argparse.ArgumentParser(description='Health check for BanglaNLP')
       parser.add_argument('--data-dir', default='data', help='Data directory')
       parser.add_argument('--state-file', default='state.json', help='State file path')
       parser.add_argument('--recipient', required=True, help='Email recipient for alerts')
       args = parser.parse_args()
       
       check_dataset_health(args.data_dir, args.state_file, args.recipient)
   ```

2. Set up a cron job to run the health check daily:

   ```
   0 9 * * * SMTP_USER=your_email@gmail.com SMTP_PASS=your_app_password python /path/to/BanglaNLP/scripts/health_check.py --recipient admin@example.com
   ```

## Webhook Integration

Set up webhooks to trigger actions based on events:

1. Create a simple webhook server:

   ```python
   # scripts/webhook_server.py
   from flask import Flask, request, jsonify
   import subprocess
   import os
   import hmac
   import hashlib
   
   app = Flask(__name__)
   
   # Secret key for webhook verification
   SECRET_KEY = os.environ.get('WEBHOOK_SECRET', 'your_secret_key')
   
   def verify_signature(payload, signature):
       computed = hmac.new(
           SECRET_KEY.encode(),
           payload,
           hashlib.sha256
       ).hexdigest()
       return hmac.compare_digest(computed, signature)
   
   @app.route('/webhook/scrape', methods=['POST'])
   def trigger_scrape():
       # Verify signature
       signature = request.headers.get('X-Signature')
       if not signature or not verify_signature(request.data, signature):
           return jsonify({'error': 'Invalid signature'}), 403
       
       # Parse request
       data = request.json
       sources = data.get('sources', [])
       max_articles = data.get('max_articles', 100)
       
       # Build command
       cmd = ['python', 'main.py']
       if sources:
           cmd.extend(['--sources'] + sources)
       cmd.extend(['--max-articles', str(max_articles)])
       
       # Execute in background
       subprocess.Popen(cmd)
       
       return jsonify({'status': 'Scraping started', 'command': ' '.join(cmd)})
   
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000)
   ```

2. Run the webhook server:

   ```bash
   WEBHOOK_SECRET=your_secret_key python scripts/webhook_server.py
   ```

3. Trigger scraping via HTTP request:

   ```bash
   # Generate signature
   PAYLOAD='{"sources":["prothomalo"],"max_articles":50}'
   SIGNATURE=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "your_secret_key" | cut -d' ' -f2)
   
   # Send request
   curl -X POST \
     -H "Content-Type: application/json" \
     -H "X-Signature: $SIGNATURE" \
     -d "$PAYLOAD" \
     http://your-server:5000/webhook/scrape
   ```

## Creating a Systemd Service (Linux)

For reliable operation on Linux servers, create a systemd service:

1. Create a service file:

   ```ini
   # /etc/systemd/system/banglanlp.service
   [Unit]
   Description=BanglaNLP Automated Scraping Service
   After=network.target
   
   [Service]
   Type=simple
   User=yourusername
   WorkingDirectory=/path/to/BanglaNLP
   ExecStart=/usr/bin/python3 main.py --max-articles 100
   Restart=on-failure
   Environment=BANGLA_NLP_OUTPUT_DIR=/path/to/data
   Environment=HUGGINGFACE_TOKEN=your_token_here
   
   [Install]
   WantedBy=multi-user.target
   ```

2. Enable and start the service:

   ```bash
   sudo systemctl enable banglanlp.service
   sudo systemctl start banglanlp.service
   ```

3. Check service status:

   ```bash
   sudo systemctl status banglanlp.service
   ```

## Next Steps

Now that you've set up automation for BanglaNLP, you might want to explore:

- [Command Line Interface](cli.md) for detailed CLI options
- [Example Scripts](examples.md) for common patterns
- [API Reference](../api/scrapers.md) for programmatic access
