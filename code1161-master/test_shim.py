# -*- coding: UTF-8 -*-
"""Run tests on a specific repo.

This file is called by marking_puller.py

Its job is to be set up and torn down for every student so that there is no
namespace pollution. Its run as a subprocess. The args are where the tests are,
and where the repo is. In almost all cases the tests are the teacher tests, and
the repo changes for each student.

"""
from importlib import import_module
import sys


def do_the_test(test_path, repo_path):
    """Run tests on a student's repo."""
    try:
        test = import_module(TEST_PATH, package="code1161base")
        r = test.theTests(repo_path)
        r["localError"] = ":)"
        return r
    except Exception as e:
        return {"of_total": 0,
                "mark": 0,
                "localError": str(e).replace(",", "~").encode('utf-8')}
        # the comma messes with the csv


def results_as_json(test_path, repo_path):
    """Save the results to a temporary json file."""
    import json
    results = do_the_test(test_path, repo_path)
    p = ""
    p = repo_path.split("/")[-1]
    results["name"] = p
    return json.dumps(results)


TEST_PATH = sys.argv[1]
REPO_PATH = sys.argv[2]

temp_results = open('temp_results.json', 'w')
temp_results.write(results_as_json(TEST_PATH, REPO_PATH))
temp_results.close()
