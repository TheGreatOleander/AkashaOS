def nudge_code(snippet:str)->str:
    if 'for i in range(len(' in snippet: return 'Try iterating directly: for item in items: ...'
    if '== True' in snippet: return 'No need to compare with True: if condition: ...'
    if 'import *' in snippet: return 'Avoid wildcard imports. Import only what you need.'
    if 'except:' in snippet and 'Exception' not in snippet: return 'Catch specific exceptions to avoid masking errors.'
    return 'Looks good. Remember: clarity > cleverness.'
