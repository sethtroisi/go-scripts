#!/usr/bin/env python3

import json
from collections import defaultdict
import dateutil.parser
import datetime

import numpy as np
import scipy.stats as stats

issue_data = "data/lz_issues_combined"

with open(issue_data) as f:
    combined = json.load(f)

pulls  = [issue for issue in combined if 'pull_request' in issue]
issues = [issue for issue in combined if 'pull_request' not in issue]


print ("Issues:", len(issues))
print ("Pulls:", len(pulls))
print ()
print ("Comments:", sum(issue['comments'] for issue in issues))

# both, issues, pulls, comments on issues
issue_info = defaultdict(lambda: [0, 0, 0, []])
comments_per = []
open_age = []
for issue in combined:
    user = issue['user']['login']
    is_pr = 'pull_request' in issue

    if issue['comments'] > 100:
        print (issue['comments'], "comments in", issue['title'])
        issue['comments'] = 100

    issue_info[user][0] += 1
    if is_pr:
        issue_info[user][2] += 1
    else:
        issue_info[user][1] += 1
        issue_info[user][3].append(issue['comments'])
        comments_per.append(issue['comments'])
        created = dateutil.parser.parse(issue['created_at'])
        closed  = issue['closed_at']
        now = datetime.datetime.now(datetime.timezone.utc)
        closed  = dateutil.parser.parse(closed) if closed else now
        age = closed - created
        open_age.append(age)

print ()
print ("Average issue open days:",  np.mean(open_age).days)
print ("20th,50th,95th: {:.1f}, {:.1f}, {:.1f} days".format(
    np.percentile(open_age, 20).total_seconds() / 86400,
    np.percentile(open_age, 50).total_seconds() / 86400,
    np.percentile(open_age, 95).total_seconds() / 86400))
print ()

print ()
issue_discussion = []
for i, (user, data) in enumerate(sorted(issue_info.items(),
                                        key=lambda i: i[1], reverse=True)):
    avg_discussion = np.mean(data[3]) if data[3] else 0
    if data[1] >= 5:
        # lower bound on average discussion
        lb = stats.t.interval(
                0.95,
                df=data[1]-1,
                loc=avg_discussion,
                scale=stats.sem(data[3]))[1]

        issue_discussion.append((-lb, user, data[1], avg_discussion))

    if i < 15:
        print ("{:20} filed {:3} ({:3.0f}%) issues, "
               "{:2} pulls, average comments/issue {:.1f}".format(
            user, data[1], 100 * data[1] / data[0], data[2], avg_discussion))
print (len(issue_info), "unique issue reporters")

print ("\n")
print ("Overall average discussion: {:.2f}".format(np.mean(comments_per)))
print ()

# Sort by spaminess
issue_discussion.sort()
for lower_bound, user, posts, avg in issue_discussion[:10] + issue_discussion[-10:]:
    print ("{:20} discussion_bound: {:.1f}  {:2} posts  {:.1f} avg".format(
        user, -lower_bound, posts, avg))

