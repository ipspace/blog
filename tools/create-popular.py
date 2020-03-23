#!/usr/bin/python3

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
import argparse

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = ""
VIEW_ID = '175841614'


def initialize_analyticsreporting(keyfile):
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_report(analytics):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:pageviews'}],
          'dimensions': [{'name': 'ga:hostname'},{'name': 'ga:pagePath'},{'name':'ga:pageTitle'}],
          'metricFilterClauses': [{
            'filters': [{
              "metricName": "ga:pageviews",
              "operator": "GREATER_THAN",
              "comparisonValue": "100"
            }]
          }]
        }]
      }
  ).execute()

def blog_metrics(results):
  data = results['reports'][0]['data']['rows']
  blog_posts = []
  for row in data:
    (host,path,title) = row['dimensions']
    if host != 'blog.ipspace.net':
      continue
    if len(path.split('/')) < 3:
      continue

    blog_posts.append({
      'url':   path,
      'title': title.split(" « ")[0],
      'count': row['metrics'][0]['values'][0]
    })

  return sorted(blog_posts, key=lambda x: int(x['count']), reverse=True)

def parseCLI():
  parser = argparse.ArgumentParser(description='Create blog metadata and templates')
  parser.add_argument('--config', dest='config', action='store', default='~/.ga.json',
                  help='Google Analytics credentials')
  parser.add_argument('--output', dest='output', action='store', default='data/popular.json',
                  help='JSON output file')
  parser.add_argument('--log', dest='logging', action='store_true',
                  help='Enable basic logging')
  parser.add_argument('--quiet', dest='quiet', action='store_true',
                  help='Report only major errors')
  parser.add_argument('--verbose', dest='verbose', action='store_true',
                  help='Enable more verbose logging')
  return parser.parse_args()

def main():
  args = parseCLI()
  analytics = initialize_analyticsreporting(os.path.expanduser(args.config),)
  response = get_report(analytics)
  with open(os.path.expanduser(args.output),"w") as output:
    json.dump(blog_metrics(response),output,sort_keys=True,indent=2)
    output.close()

if __name__ == '__main__':
  main()
