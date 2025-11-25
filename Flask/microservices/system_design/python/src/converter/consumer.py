import os
import sys
import pika
import gridfs
from pymongo import MongoClient
from convert.to_mp3 import convert_to_mp3


def main():
    # ------------------------------
    # MongoDB + GridFS
    # ------------------------------
    client = MongoClient("host.minikube.internal", 27017)

    db_videos = client["videos"]
    db_mp3s = client["mp3s"]

    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3s)

    # ------------------------------
    # RabbitMQ connection
    # ------------------------------
    rabbit_user = os.environ.get("RABBITMQ_USER", "guest")
    rabbit_pass = os.environ.get("RABBITMQ_PASS", "guest")
    rabbit_host = os.environ.get("RABBIT_HOST", "rabbitmq")
    queue_name = os.environ.get("VIDEO_QUEUE", "video")

    credentials = pika.PlainCredentials(rabbit_user, rabbit_pass)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbit_host,
            credentials=credentials,
        )
    )

    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_qos(prefetch_count=1)  # allows fair distribution

    print(" [*] Converter service ready. Waiting for messages…")

    # ------------------------------
    # Callback for RabbitMQ messages
    # ------------------------------
    def callback(ch, method, properties, body):
        print(f" [x] Received: {body}")

        error = convert_to_mp3(body, fs_videos, fs_mp3s, ch)

        if error:
            print(" [!] Conversion failed → NACK")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        else:
            print(" [✓] Conversion completed → ACK")
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback
    )

    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)
