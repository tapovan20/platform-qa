#!/usr/bin/env python3
#
# =============================================================================================
# IBM Confidential
# (C) Copyright IBM Corp. 2021-2022
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
# =============================================================================================
#
# Description:
# Script to validate the PR message with a modified Conventional Commit format.


import os
import re
import sys


def check(string):
    type_regex = r'(feat|fix|docs|refactor|chore|vuln)'  # TYPE
    compatibility_issue_regex = r'(!)?'  # ! (Optional)
    scope_regex = r'(?:\((\w+)\))?: '  # SCOPE (Optional)
    jira_regex = r'((?:[A-Z]+-\d+)(?:,\s?[A-Z]+-\d+)*): '  # JIRA
    jira_regex_case_insensitive = r'((?:[a-zA-Z]+-\d+)(?:,\s?[a-zA-Z]+-\d+)*): '  # JIRA
    subject_regex = r'(\S.*)'  # SUBJECT

    if re.match(r'Merge pull request', string):
        return True, ""
    elif re.match(r'^Merge', string):
        return True, ""
    elif re.match(type_regex + compatibility_issue_regex + scope_regex +
                  jira_regex + subject_regex, string):
        return True, ""
    elif re.match(type_regex + compatibility_issue_regex, string) is None:
        return False, "TYPE"
    elif re.match(type_regex + compatibility_issue_regex + scope_regex, string) is None:
        return False, "SCOPE"
    elif re.match(type_regex + compatibility_issue_regex +
                  scope_regex + jira_regex, string) is None:
        if re.match(type_regex + compatibility_issue_regex +
                    scope_regex + jira_regex_case_insensitive, string) is not None:
            print("The JIRA Ticket contained lowercase characters in the project field. "
                  "JIRA ticket characters must be uppercase.")
            return False, "JIRA"
        return False, "JIRA"
    else:
        return False, "SUBJECT"


syntax_desc = """
Expected Format:
TYPE[!][(SCOPE)]: JIRA: SUBJECT

Where:
[]      : Indicates an optional component.
TYPE    : Is one of the following:
            feat     : new feature
            fix      : bug fix
            docs     : documentation only change
            refactor : code change that neither fixes a bug nor adds a feature
            chore    : changes to the build or auxiliary tools, libraries, etc.
            vuln     : a fix to address a specific security vulnerability
!       : (Optional) Indicates a compatibility issue.
SCOPE   : (Optional) Indicates the area of project.
JIRA    : JIRA ticket ID. This may be a comma-separated list.
SUBJECT : Succinct description of the change.
"""

if __name__ == '__main__':
    error = True
    for message in sys.stdin.readlines():
        message = message.rstrip()[8:]
        (state, issue) = check(message)
        if not state:
            print("Issue found with commit {}".format(issue))
            print(" -- {}".format(message))
        else:
            error = False
            print("OK: {}".format(message))

    if error:
        sys.exit(1)
