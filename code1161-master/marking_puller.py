# -*- coding: UTF-8 -*-
"""Get the latest copy of all the repos.

This pulls the latest copy of all the repos
It can clone new repos if you set THERE_ARE_NEW_STUDENTS to true
"""



from io import StringIO
from .codeHelpers import RunCmd
from datetime import datetime
from itertools import repeat
import git
import json
import os
import pandas as pd
import re
import requests
import ruamel.yaml as yaml
import time

LOCAL = os.path.dirname(os.path.realpath(__file__))  # the context of this file
CWD = os.getcwd()  # The curent working directory
print("LOCAL", LOCAL)
print("CWD", CWD)


def getDFfromCSVURL(url, columnNames=False):
    """Get a csv of values from google docs."""
    r = requests.get(url)
    data = r.content
    if columnNames:
        return pd.read_csv(StringIO(data), header=0, names=columnNames)
    else:
        return pd.read_csv(StringIO(data))


def update_for_new_students(chatty=False):
    """Get an updated copy of the spreadsheet."""
    # pull the forks list
    ss_of_details_url = ("https://docs.google.com/spreadsheets/d/"
                         "1qeOp6PZ48BFLlHaH3ZEil09MBNfQD0gztuCm2cEiyOo/"
                         "pub?gid=2144767463"
                         "&single=true&output=csv")

    student_details = getDFfromCSVURL(ss_of_details_url, ["paste",
                                                          "their_username",
                                                          "repo_name",
                                                          "check",
                                                          "repo_url",
                                                          "slack"])

    for index, student in student_details.iterrows():
        try:
            git.Repo.clone_from(student.repo_url,
                                os.path.join(rootdir, student.their_username))
            print("{} new repo for {}".format(index,
                                              student.their_username))
        except Exception as e:
            if chatty:
                print("{} we already have {} {}".format(index,
                                                        student.their_username,
                                                        e))

    return student_details


def try_to_kill(file_path, chatty=False):
    """Attempt to delete the file specified by file_path."""
    try:
        os.remove(file_path)
        print("deleted {}".format(file_path))
    except Exception as e:
        if chatty:
            print(file_path, e)


def pull_all_repos(dirList, chatty=False):
    """Pull latest version of all repos."""
    of_total = len(dirList)
    for i, student_repo in enumerate(dirList):
        repo_is_here = os.path.join(rootdir, student_repo)
        try:
            repo = git.cmd.Git(repo_is_here)
            repo.execute(["git", "fetch", "--all"])
            repo.execute(["git", "reset", "--hard", "origin/master"])
            repo.pull()  # probably not needed, but belt and braces
            t = datetime.now().strftime('%H:%M:%S')
            print("{}: {}/{} pulled {}'s repo".format(t,
                                                      i,
                                                      of_total,
                                                      student_repo))
        except Exception as e:
            print(student_repo, e)


def csvOfDetails(dirList):
    """Make a CSV of all the students."""
    results = []
    for student_repo in dirList:
        path = os.path.join(rootdir, student_repo, "aboutMe.yml")
        details = open(path).read()
        details = details.replace("@", "^AT^")
        details = re.sub(":(\w)", ": \g<1>", details)
        details = re.sub(" -", " None", details)
        details = details.replace("é", "e")
        details = details.replace("w:", "w: ")
        try:
            details = yaml.load(details, yaml.RoundTripLoader)
            details["repoName"] = student_repo
            details["error"] = False
            if details["mediumUsername"][:4] != "^AT^":
                details["mediumUsername"] = "^AT^" + details["mediumUsername"]
            results.append(details)

            if details["studentNumber"] == "z1234567":
                print(student_repo, "hasn't updated")
        except Exception as e:
            print(details)
            results.append({'error': e, "repoName": student_repo})

    print("\n\nResults:")
    resultsDF = pd.DataFrame(results)
    # print(resultsDF)
    resultsDF.to_csv(os.path.join(CWD, "csv/studentDetails.csv"))
    fix_up_csv()


def fix_up_csv(path="csv/studentDetails.csv"):
    """Do replacements on csv.

    Mostly to undo tricks that were needed to deal with invalid yml
    """
    lines = []
    with open(path) as infile:
        for line in infile:
            line = line.replace("^AT^", "@")
            line = line.replace(",,", ",-,")
            lines.append(line)
    with open(path, 'w') as outfile:
        for line in lines:
            print(line)
            outfile.write(line)


def log_progress(message, logfile_name):
    """Write a message to a logfile."""
    completed_students_list = open(logfile_name, "a")
    completed_students_list.write(message)
    completed_students_list.close()


def test_in_clean_environment(student_repo,
                              root_dir,
                              week_number,
                              logfile_name,
                              timeout=5,
                              temp_file_path='temp_results.json',
                              test_file_path='./test_shim.py'):
    """Test a single student's work in a clean environment.

    This calls a subprocess that opens a fresh python environment, runs the
    tests and then saves the results to a temp file.

    Back in this process, we read that temp file, and then use its values to
    constuct a dictionary of results (or errors).

    The logging is just to see real time progress as this can run for a long
    time and hang the machine.
    """
    results_dict = {}
    log_progress(student_repo, logfile_name)
    start_time = time.time()
    try:
        test_args = ['python',
                     test_file_path,
                     "week{}.tests".format(week_number),
                     "{}/{}".format(root_dir, student_repo)
                     ]
        # print("\ntest_args", test_args,
        #       "\nstudent_repo", student_repo,
        #       "\nroot_dir", root_dir,
        #       "\nweek_number", week_number,
        #       "\nlogfile_name", logfile_name,
        #       "\ntemp_file_path", temp_file_path,
        #       "\ntest_file_path", test_file_path,
        #       "\ntimeout", timeout,
        #       "\nLOCAL", LOCAL)
        RunCmd(test_args, timeout).Run()

        full_path = os.path.join(LOCAL,  temp_file_path)
        temp_results = open(full_path, 'r')
        contents = temp_results.read()
        results_dict = json.loads(contents)
        results_dict["bigerror"] = ":)"
        temp_results.close()

        log_progress(" good for w{}\n".format(week_number),
                     logfile_name)
    except Exception as e:
        results_dict = {"bigerror": str(e).replace(",", "~"),
                        "name": student_repo}  # the comma messes with the csv

        log_progress(" bad {} w{}\n".format(e, week_number),
                     logfile_name)
    elapsed_time = time.time() - start_time
    results_dict["time"] = elapsed_time
    return results_dict


def prepare_log(logfile_name, firstLine="here we go:\n"):
    """Create or empty the log file."""
    completed_students_list = open(logfile_name, "w")
    completed_students_list.write(firstLine)
    completed_students_list.close()


def mark_work(dirList, week_number, root_dir, dfPlease=True, timeout=5):
    """Mark the week's exercises."""
    logfile_name = "temp_completion_log"
    prepare_log(logfile_name)
    r = len(dirList)  # for repeat count

    results = list(map(test_in_clean_environment,  # Function name
                  dirList,  # student_repo
                  repeat(root_dir, r),  # root_dir
                  repeat(week_number, r),  # week_number
                  repeat(logfile_name, r),  # logfile_name
                  repeat(timeout, r)  # timeout
                  ))

    resultsDF = pd.DataFrame(results)
    csv_path = "csv/week{}marks.csv".format(week_number)
    resultsDF.to_csv(os.path.join(CWD, csv_path), index=False)
    for _ in [1, 2, 3]:
        # this is pretty dirty, but it gets tricky when you have
        # ,,, -> ,-,, because each intance needs to be replaced multiple times
        # TODO; #makeitnice
        fix_up_csv(path=csv_path)
    print("\n+-+-+-+-+-+-+-+\n\n")
    if dfPlease:
        return resultsDF


rootdir = '../code1161StudentRepos'

print("\nCheck to see if there are any new students in the spreadsheet")
update_for_new_students(chatty=True)

dirList = os.listdir(rootdir)
print("dir list", dirList)

print("\nPull all the repos so we have the latest copy.")
print("(This takes a while.)")
pull_all_repos(dirList, chatty=True)

print("\nUpdate the CSV of details")
csvOfDetails(dirList)  # This feeds the sanity check spreadsheet


print("\nMark week 1's work")
mark_work(dirList, 1, rootdir, dfPlease=False, timeout=5)

print("\nMark week 2's work")
mark_work(dirList, 2, rootdir, dfPlease=False, timeout=5)

print("\nMark week 3's work")
mark_work(dirList, 3, rootdir, dfPlease=False, timeout=25)

print("\nMark week 4's work")
mark_work(dirList, 4, rootdir, dfPlease=False, timeout=45)

print("\nMark week 5's work")
mark_work(dirList, 5, rootdir, dfPlease=False, timeout=45)
