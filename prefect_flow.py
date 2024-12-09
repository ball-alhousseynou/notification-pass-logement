import json
import os
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import prefect
from prefect import flow, task
from prefect.variables import Variable


def get_prefect_variable(var_name: str):
    return Variable.get(var_name, default=os.getenv(var_name))


@task(log_prints=True)
def run_passlogement_spider():

    try:
        output_file = "offers/great_offers.json"

        scrapy_command = (
            f"scrapy crawl passlogement -a username={get_prefect_variable('username')} "
            f"-a password={get_prefect_variable('password')}"
        )

        result = subprocess.run(
            scrapy_command, shell=True, capture_output=True, text=True
        )

        if result.returncode != 0:
            prefect.get_run_logger().error(f"Spider run failed: {result.stderr}")
            raise Exception(f"Scrapy spider error: {result.stderr}")

        prefect.get_run_logger().info(f"Spider output: {result.stdout}")

        return output_file

    except Exception as e:
        prefect.get_run_logger().error(f"Error running spider: {e}")
        raise


@task(log_prints=True)
def process_passlogement_data(file_path):
    """
    Process and validate scraped data
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        prefect.get_run_logger().info(f"Total offers retrieved: {len(data)}")

        return data
    except Exception as e:
        prefect.get_run_logger().error(f"Error processing data: {e}")
        raise


@task(log_prints=True)
def send_email_notification(data):

    sender_email = get_prefect_variable("sender_email")
    receiver_emails = get_prefect_variable("receiver_email")
    sender_password_app = get_prefect_variable("sender_password_app")
    sample_offer = data[0]

    subject = f"Passlogement: {len(data)} Great offers retrieved"
    message = f"""
    New Rental Opportunity: {sample_offer['city']}
    🌟 Exclusive Offer from {sample_offer['partner_label']} 🌟

    Hi,

    We are pleased to present a fantastic rental opportunity in the heart of {sample_offer['city']}:

    🏠 Accommodation Type: {sample_offer['accommodation_type_label']}
    📐 Surface Area: {sample_offer['surface']} m²
    💰 Rental Price: €{sample_offer['rental_price']}/month
    📍 Address: {sample_offer['address']}, {sample_offer['zipcode']} {sample_offer['city']}

    Key Details:
    - 📌 Reference: {sample_offer['reference']}
    - 👥 Roommate Friendly: {'Yes' if sample_offer['roommate'] else 'No'}
    - 🏢 Partner: {sample_offer['partner_label']}
    - 🕒 Available Until: {sample_offer['date_validity']}
    - 👤 Current Candidates on Offer: {sample_offer['number_candidates_on_offer']}

    Don't miss your chance to apply!

    Warm regards,
    """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password_app)
            for receiver_email in receiver_emails:
                msg["To"] = receiver_email
                text = msg.as_string()
                server.sendmail(sender_email, receiver_email, text)
        prefect.get_run_logger().info("Email notification sent successfully!")
    except Exception as e:
        prefect.get_run_logger().error(f"Failed to send email: {e}")
        raise


@flow(log_prints=True)
def passlogement_workflow():

    output_file = run_passlogement_spider()

    data = process_passlogement_data(output_file)

    if data:
        send_email_notification(data)


if __name__ == "__main__":
    passlogement_workflow.deploy(
        name="passlogement-workflow", cron="*/30 * * * *", work_queue_name="default"
    )
