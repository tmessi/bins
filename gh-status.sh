#!/bin/bash
status=$(curl --silent https://status.github.com/api/status.json)

echo "$status" | jq -r '.status'

echo "$status" | jq -r '.last_updated' > .gh_last_updated
