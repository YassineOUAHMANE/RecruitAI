#!/bin/bash

BASE_URL="http://localhost:80"


login_response=$(
  curl -s -X PUT "$BASE_URL/api/conversation" \
    -H "Content-Type: application/json" \
    -d '{"text":"hello bot"}'
)