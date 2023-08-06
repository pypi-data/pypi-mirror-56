#!/usr/bin/env python

"""tasksscraper.outlook: ...."""

__author__ = "Daniel Engvall"
__email__ = "daniel@engvalls.eu"

import osascript
from typing import List
import json
from loguru import logger


def get_outlook_tasks() -> List:
    """Get Outlook tasks

    Returns:
        List of tasks from Outlook

    """
    # noinspection PyPep8,PyPep8
    c, o, e = osascript.run('''
    -- display dialog "Will now process all current outlook tasks selected"
    tell application "Microsoft Outlook"
        -- activate
        set x to ""
        set selectedTasks to selected objects
        if selectedTasks is {} then
            display dialog "Please select a task first and then run this script." with icon 1
            return
        end if
        repeat with theTask in selectedTasks
            set c to "{"
            if class of theTask is task then
                set c to c & "\\"taskName\\": \\"" & name of theTask & "\\""
                set theContent to plain text content of theTask
                if theContent is missing value then
                    set theContent to ""
                end if
                set c to c & ",\\"taskContent\\": \\"" & theContent & "\\""
                set theFolder to folder of theTask
                set c to c & ",\\"taskFolder\\": \\"" & name of theFolder & "\\""
                set c to c & ",\\"modifiedDate\\": \\"" & modification date of theTask & "\\""
                set c to c & ",\\"startDate\\": \\"" & start date of theTask & "\\""
                set c to c & ",\\"due\\": \\"" & due date of theTask & "\\""
                set c to c & ",\\"completeDate\\": \\"" & completed date of theTask & "\\""
                set c to c & ",\\"taskPriority\\": \\"" & priority of theTask & "\\""
                set theCategory to category of theTask
                set catList to "["
                set cat_count to 0 as number
                repeat with oneCat in theCategory
                    if oneCat is not equal to ""
                        set theCategoryName to name of oneCat
                        if cat_count > 0 then
                            set catList to (catList & ",") as string
                        end if
                        set catList to catList & "\\"" & theCategoryName & "\\""
                        set cat_count to cat_count + 1 as number
                    end if
                end repeat
                set catList to catList & "]"
                set c to c & ",\\"taskCategories\\": " & catList
                set c to c & "},"
            end if
        set x to (x & c) as string
        end repeat
    end tell
    return x
    ''') # nopep8
    o = o.strip(',')
    o = f'[{o}]'
    logger.info(f'osascript error: {e}')
    logger.info(f'osascript output: {o}')
    if c == 0:
        result = json.loads(o)
        return result
    else:
        return None