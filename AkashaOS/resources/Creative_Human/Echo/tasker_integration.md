# Tasker Integration for Nexus AI System

This document provides Tasker profiles and tasks to integrate with the Nexus AI Problem-Solving system.

## Setup Instructions

1. Install Tasker on your Android device
2. Import the profiles and tasks below
3. Configure the server URL and authentication token
4. Enable the profiles

## Variables to Set

In Tasker, create these global variables:

- `%NEXUS_URL` = Your server URL (e.g., "http://192.168.1.100:8080")
- `%NEXUS_TOKEN` = Your authentication token (if enabled)

## Profile 1: Nexus Status Check

**Trigger**: Time-based (every 30 minutes) or Manual
**Action**: Check Nexus Status

### Task: Check Nexus Status

```
A1: HTTP Request [
    Method: GET
    URL: %NEXUS_URL/api/status
    Headers: Authorization: Bearer %NEXUS_<REDACTED_Password_label> File: 
    Timeout: 30
    Structure Output: On
]

A2: If [ %http_response_code eq 200 ]
    A3: Variable Set [
        Name: %nexus_status
        To: %http_data.status
    ]
    A4: Variable Set [
        Name: %current_problem_title
        To: %http_data.current_problem.title
    ]
    A5: If [ %current_problem_title neq %NULL ]
        A6: Notify [
            Title: Nexus Active
            Text: Working on: %current_problem_title
            Icon: android.resource://net.dinglisch.android.taskerm/drawable/mw_action_build
        ]
    A7: Else
        A8: Notify [
            Title: Nexus Idle
            Text: No current problem
            Icon: android.resource://net.dinglisch.android.taskerm/drawable/mw_action_pause
        ]
    A9: End If
A10: Else
    A11: Notify [
        Title: Nexus Error
        Text: Failed to connect to Nexus
        Icon: android.resource://net.dinglisch.android.taskerm/drawable/mw_action_error
    ]
A12: End If
```

## Profile 2: Quick Note Entry

**Trigger**: AutoVoice Recognition with phrase "Nexus note"
**Action**: Add Note to Current Session

### Task: Add Note

```
A1: Get Voice [
    Prompt: What's your note?
    Timeout: 30
]

A2: If [ %VOICE neq %NULL ]
    A3: HTTP Request [
        Method: POST
        URL: %NEXUS_URL/api/add_note
        Headers: Authorization: Bearer %NEXUS_<REDACTED_Password_label>: application/json
        Body: {"note": "%VOICE"}
        Timeout: 30
    ]
    
    A4: If [ %http_response_code eq 200 ]
        A5: Say [
            Text: Note added
            Engine: Voice
            Stream: Notification
        ]
    A6: Else
        A7: Say [
            Text: Failed to add note
            Engine: Voice
            Stream: Notification
        ]
    A8: End If
A9: End If
```

## Profile 3: Progress Update

**Trigger**: AutoVoice Recognition with phrase "Nexus progress"
**Action**: Add Progress Update

### Task: Add Progress

```
A1: Get Voice [
    Prompt: What progress do you want to report?
    Timeout: 30
]

A2: If [ %VOICE neq %NULL ]
    A3: HTTP Request [
        Method: POST
        URL: %NEXUS_URL/api/add_progress
        Headers: Authorization: Bearer %NEXUS_<REDACTED_Password_label>: application/json
        Body: {"progress": "%VOICE"}
        Timeout: 30
    ]
    
    A4: If [ %http_response_code eq 200 ]
        A5: Say [
            Text: Progress recorded
            Engine: Voice
            Stream: Notification
        ]
        A6: Vibrate [
            Pattern: 100,100,100
        ]
    A7: Else
        A8: Say [
            Text: Failed to record progress
            Engine: Voice
            Stream: Notification
        ]
    A9: End If
A10: End If
```

## Profile 4: Complete Problem

**Trigger**: AutoVoice Recognition with phrase "Nexus complete"
**Action**: Mark Current Problem as Complete

### Task: Complete Problem

```
A1: Get Voice [
    Prompt: Any final notes about completion?
    Timeout: 30
]

A2: HTTP Request [
    Method: POST
    URL: %NEXUS_URL/api/complete_problem
    Headers: Authorization: Bearer %NEXUS_<REDACTED_Password_label>: application/json
    Body: {"note": "%VOICE"}
    Timeout: 30
]

A3: If [ %http_response_code eq 200 ]
    A4: Say [
        Text: Problem completed successfully
        Engine: Voice
        Stream: Notification
    ]
    A5: Notify [
        Title: Problem Completed!
        Text: Great work! Problem marked as done.
        Icon: android.resource://net.dinglisch.android.taskerm/drawable/mw_action_done
    ]
    A6: Vibrate [
        Pattern: 200,100,200,100,200
    ]
A7: Else
    A8: Say [
        Text: Failed to complete problem
        Engine: Voice
        Stream: Notification
    ]
A9: End If
```

## Profile 5: Get Current Problem Details

**Trigger**: AutoVoice Recognition with phrase "Nexus status"
**Action**: Read Current Problem Details

### Task: Read Current Problem

```
A1: HTTP Request [
    Method: GET
    URL: %NEXUS_URL/api/current_problem
    Headers: Authorization: Bearer %NEXUS_<REDACTED_Password_label>: 30
    Structure Output: On
]

A2: If [ %http_response_code eq 200 ]
    A3: Variable Set [
        Name: %problem_title
        To: %http_data.title
    ]
    A4: Variable Set [
        Name: %problem_url
        To: %http_data.url
    ]
    A5: Variable Set [
        Name: %estimated_effort
        To: %http_data.estimated_effort
    ]
    A6: Variable Set [
        Name: %actual_effort
        To: %http_data.actual_effort
    ]
    
    A7: Say [
        Text: Currently working on: %problem_title. Estimated effort: %estimated_effort hours. Actual effort so far: %actual_effort hours.
        Engine: Voice
        Stream: Notification
    ]
    
    A8: Notify [
        Title: Current Problem
        Text: %problem_title
        Actions: View:url:%problem_url
    ]
    
A9: Else If [ %http_response_code eq 404 ]
    A10: Say [
        Text: No current problem. System is idle.
        Engine: Voice
        Stream: Notification
    ]
A11: Else
    A12: Say [
        Text: Error getting current problem status
        Engine: Voice
        Stream: Notification
    ]
A13: End If
```

## Profile 6: Pause Session

**Trigger**: AutoVoice Recognition with phrase "Nexus pause"
**Action**: Pause Current Work Session

### Task: Pause Session

```
A1: Get Voice [
    Prompt: Why are you pausing?
    Timeout: 30
]

A2: HTTP Request [
    Method: POST
    URL: %NEXUS_URL/api/pause_session
    Headers: Authorization: Bearer %NEXUS_<REDACTED_Password_label>: application/json
    Body: {"note": "Paused: %VOICE"}
    Timeout: 30
]

A3: If [ %http_response_code eq 200 ]
    A4: Say [
        Text: Session paused
        Engine: Voice
        Stream: Notification
    ]
    A5: Notify [
        Title: Session Paused
        Text: Work session has been paused
        Icon: android.resource://net.dinglisch.android.taskerm/drawable/mw_action_pause
    ]
A6: Else
    A7: Say [
        Text: Failed to pause session
        Engine: Voice
        Stream: Notification
    ]
A8: End If
```

## Profile 7: View Queue

**Trigger**: AutoVoice Recognition with phrase "Nexus queue"
**Action**: Display Problem Queue

### Task: Show Queue

```
A1: HTTP Request [
    Method: GET
    URL: %NEXUS_URL/api/queue
    Headers: Authorization: Bearer %NEXUS_<REDACTED_Password_label>: 30
    Structure Output: On
]

A2: If [ %http_response_code eq 200 ]
    A3: Variable Set [
        Name: %queue_count
        To: %http_data.count
    ]
    
    A4: For [ Variable:%item Items:%http_data.queue() ]
        A5: Variable Set [
            Name: %queue_list
            To: %queue_list
%item.title (Priority: %item.priority)
            Append: On
        ]
    A6: End For
    
    A7: Say [
        Text: There are %queue_count problems in the queue
        Engine: Voice
        Stream: Notification
    ]
    
    A8: Notify [
        Title: Problem Queue (%queue_count)
        Text: %queue_list
        Actions: Refresh:task:Show Queue
    ]
    
A9: Else
    A10: Say [
        Text: Error getting queue information
        Engine: Voice
        Stream: Notification
    ]
A11: End If
```

## Profile 8: Smart Notifications

**Trigger**: Time-based (every 25 minutes during work hours)
**Action**: Smart Focus Reminder

### Task: Focus Reminder

```
A1: HTTP Request [
    Method: GET
    URL: %NEXUS_URL/api/current_problem
    Headers: Authorization: Bearer %NEXUS_<REDACTED_Password_label>: 30
    Structure Output: On
]

A2: If [ %http_response_code eq 200 ]
    A3: Variable Set [
        Name: %session_start
        To: %http_data.current_session.start_time
    ]
    
    A4: Variable Set [
        Name: %current_time
        To: %TIMES
    ]
    
    A5: Variable Set [
        Name: %time_diff
        To: %current_time - %session_start
    ]
    
    A6: If [ %time_diff gt 1500 ] // 25 minutes
        A7: Notify [
            Title: Focus Check
            Text: You've been working for 25+ minutes. Take a break or add progress?
            Actions: Break:task:Take Break,Progress:task:Add Progress
        ]
        A8: Vibrate [
            Pattern: 50,50,50
        ]
    A9: End If
A10: End If
```

## Profile 9: Daily Summary

**Trigger**: Time-based (8:00 PM daily)
**Action**: Generate Daily Summary

### Task: Daily Summary

```
A1: HTTP Request [
    Method: GET
    URL: %NEXUS_URL/api/status
    Headers: Authorization: Bearer %NEXUS_<REDACTED_Password_label>: 30
    Structure Output: On
]

A2: If [ %http_response_code eq 200 ]
    A3: Variable Set [
        Name: %completed_today
        To: %http_data.problem_counts.completed
    ]
    
    A