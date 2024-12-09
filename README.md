# Notification Pass Logement

---
One morning, my girlfriend said to me, a bit annoyed: "I have to keep logging into the Pass Logement platform to check if new apartments are available!" And I thought to myself: "No, this can't go on like this!" And so, the **Notification Pass Logement** project was born from this daily frustration. The idea? To automate the entire process by retrieving updates from the platform and sending notifications as soon as something new appears.

With this project, no more endless logins and manual checks. With Scrapy for scraping and Prefect for managing workflows, the tool automatically retrieves the relevant information and can send alerts. A simple and effective solution to never miss an important listing again!

<br>
<center><img src="assets/pass-logement-logo.png" alt="Pass Logement Logo" /></center>

---

## Features

- **Automated Scraping**: Uses Scrapy to log in and fetch data from the Pass Logement website.
- **Workflow Orchestration**: Leverages Prefect for scheduling, monitoring, and deployment of scraping tasks.
- **Flexible Deployment**: Supports local execution and Prefect Cloud deployment for distributed task management.
- **Notifications**: Configurable to send alerts or updates based on specific triggers.

---

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ball-alhousseynou/notification-pass-logement.git
   cd notification-pass-logement
   ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables in a `.env` file and in `Variables` prefect cloud:

   ```bash
   receiver_email=""        # List of emails address to receive notifications
   username=""              # Your username for passlogement authentication
   password=""              # Your password for passlogement authentication
   sender_email=""          # Email address from which to send notifications 
   sender_password_app=""   # Token created in app password gmail
   ```

## Usage
### Running Scrapy Locally
To run the Scrapy spider locally:
```bash
    scrapy crawl passlogement -a username=$username -a password=$password
```

## Using Prefect
### Local Prefect Server
1. Start the Prefect server:
    ```bash
    prefect server start
    ```
2. Deploy the Prefect flow:
    ```bash
    prefect deploy
    ```
3. Start a Prefect worker:
    ```bash
    prefect worker start --pool "default" --work-queue "default"
    ```

### Prefect Cloud Deployment
1. Log in to Prefect Cloud:
    ```bash
    prefect cloud login
    ```

2. Deploy the Prefect flow to Prefect Cloud:
    ```bash
    prefect deploy
    ```

3. Start a worker for the cloud:
    ```bash
    prefect worker start --pool "default" --work-queue "default"
    ```


## Contact
For inquiries or support, please contact ballhousseynou@gmail.com