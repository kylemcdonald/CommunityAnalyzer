# CommunityAnalyzer

Experimenting with automated analysis of GitHub community behaviors.

## Motivation

The idea is to take a data-driven approach to understanding what works and doesn't work in a community.

1. What causes issues to be closed faster?
2. What causes issues to linger for a long time?
3. What style of working creates positive sentiment?

## Process

1. Download all issues (takes 30 minutes for openFrameworks).
2. Visualize issues opening/closing the way you would the [lineup of Grateful Dead](http://upload.wikimedia.org/wikipedia/en/timeline/4d052688fe7d1eda97e91c09c6477a00.png).
3. Extract metrics from issues.
4. Determine impact of metrics on time to completion.

## Issue Metrics

* Number of comments.
* Number of participants.
* Comments per participant.
* Average, minimum, and maximum length of comments.
* Presence of code in comments.
* Number of labels, and which labels.
* Whether someone is assigned to the issue.
* Whether the issue is milestoned.
* The size of the diff in the commit that closes the issue.
* LIWC and sentiment analysis of the comments.

## API Notes

* 5000 requests / hour (stick with one a second and you're safe)
* https://developer.github.com/v3/oauth/
* https://api.github.com/repos/openframeworks/openFrameworks/issues/1/comments
* https://api.github.com/repos/openframeworks/openFrameworks/issues/1/events