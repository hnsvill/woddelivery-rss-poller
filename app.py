import feedparser
import calendar, time
import boto3
import sys
from botocore.config import Config
import os


# Retrieve details of the most recent entry to the RSS feed
def constructedMessageMostRecentEntry():
    feedAddress = "https://www.crossfitswbeaverton.com/feed/"
    parsedFeed = feedparser.parse(feedAddress)
    publishedTimeRSSParsed = parsedFeed.entries[0]['published_parsed']
    publishedTimeEpoch = calendar.timegm(publishedTimeRSSParsed)
    publishedTimeHuman = time.ctime(publishedTimeEpoch)
    author = parsedFeed.entries[0]['author']
    link = parsedFeed.entries[0]['link']
    # title = parsedFeed.entries[0]['title']
    return {
        'author':author,
        'publishedTimeEpoch':publishedTimeEpoch,
        'publishedTimeHuman':publishedTimeHuman,
        'link':link
        }

# Determine if the most recent entry was posted within 12h/is tomorrow's WOD
def publishedWithinNHours(publishedTimeInEpochSeconds, hoursAgoToCheckFor):
    return ((time.time() - publishedTimeInEpochSeconds)/60)/60 <= hoursAgoToCheckFor

def publishToSNS(messageBody):
    return boto3.client('sns').publish(
    Message=str(messageBody),
    TopicArn='arn:aws:sns:us-west-2:587838441384:testMessages'
)

# def recievedFromSQS():
#     sqs = boto3.client('sqs')
#     queue_url = 'https://sqs.us-west-2.amazonaws.com/587838441384/testmessage'
#     return sqs.receive_message(
#         QueueUrl=queue_url,
#         AttributeNames=[
#             'All'
#         ],
#         # MaxNumberOfMessages=5,
#         MessageAttributeNames=[
#             'All'
#         ],
#         VisibilityTimeout=0,
#         WaitTimeSeconds=20
#     )

def handler(event=None, context=None):
    latestEntry = constructedMessageMostRecentEntry()
    if publishedWithinNHours(latestEntry['publishedTimeEpoch'], 48):
        print(publishToSNS(latestEntry))
    return 'Hello from AWS Lambda on: ' + sys.version + '!'

if __name__ == "__main__":
    handler()