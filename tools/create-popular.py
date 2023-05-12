#!/usr/bin/env python3

import gapandas4 as gp
import os
import json
import argparse
import sys

KEY_FILE_LOCATION = os.path.expanduser('~/.ssh/blog-ga-secrets.json')
PROPERTY_ID = '363350028'
FORMAT ='json'
HOST = 'blog.ipspace.net'

def get_report():
  report_request = gp.RunReportRequest(
    property=f"properties/{PROPERTY_ID}",
    dimensions=[
        gp.Dimension(name="hostName"),
        gp.Dimension(name="pagePath"),
        gp.Dimension(name="pageTitle")
    ],
    metrics=[
        gp.Metric(name="activeUsers")
    ],
    limit=50,
    date_ranges=[gp.DateRange(start_date="30daysAgo", end_date="today")],
    dimension_filter=gp.FilterExpression(
      and_group=gp.FilterExpressionList(
        expressions=[
          gp.FilterExpression(
            filter=gp.Filter(
              field_name="hostName",
              string_filter=gp.Filter.StringFilter(value="blog.ipspace.net"))),
        ]
      )
    )
  )

  return gp.query(KEY_FILE_LOCATION, report_request, report_type="report")

def blog_metrics(results,limit):
  blog_posts = []
  for (idx,row) in results.iterrows():
    path = row['pagePath']
    if limit and not limit in path:
      continue
    if len(path.split('/')) < 3:
      continue

    blog_posts.append({
      'url':   row['pagePath'],
      'title': row['pageTitle'].split(" « ")[0],
    })

  return blog_posts

def print_html_list(blog_list):
  if len(blog_list) == 0:
    print('No entries matching your query')
    return
  for entry in blog_list:
    print('* [%s](https://%s%s)' % (entry['title'],HOST,entry['url']))

def parseCLI():
  parser = argparse.ArgumentParser(description='Create blog metadata and templates')
  parser.add_argument('--config', dest='config', action='store', default='~/.ga.json',
                  help='Google Analytics credentials')
  parser.add_argument('--output', dest='output', action='store', default='data/popular.json',
                  help='JSON output file')
  parser.add_argument('--format', dest='format', action='store', help='Output format (JSON or HTML)')
  parser.add_argument('--limit', dest='limit', action='store', help='Limit the search to specified URLs')
  parser.add_argument('--log', dest='logging', action='store_true',
                  help='Enable basic logging')
  parser.add_argument('--quiet', dest='quiet', action='store_true',
                  help='Report only major errors')
  parser.add_argument('--verbose', dest='verbose', action='store_true',
                  help='Enable more verbose logging')
  return parser.parse_args()

def main():
  args = parseCLI()

  fmt = 'html' if args.limit else 'json'
  fmt = args.format or fmt

  response = get_report()
  metrics = blog_metrics(response,args.limit)

  if fmt == 'json':
    with open(os.path.expanduser(args.output),"w") as output:
      json.dump(metrics,output,sort_keys=True,indent=2)
      output.close()
  elif fmt == 'html':
    print_html_list(metrics)

if __name__ == '__main__':
  main()
