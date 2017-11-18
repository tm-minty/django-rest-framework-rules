#!/bin/sh
coverage run --source=rest_framework_rules runtests.py --nologcapture --nocapture "$@"
result=$?
echo
coverage report -m
echo
exit $result
