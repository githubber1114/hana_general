# hana_general

hana_compare_config_params.py 
  - created to compare configuration parameters between 3 scale-out HANA databases (Production, Production Support and Quality Assurance).
  - script queries all parameters from M_CONFIGURATION_PARAMETER_VALUES
  - for each parameter, script queries AUDIT_LOG to try to determine last changed date/by, assuming auditing is enabled for system configuration changes
  - compares results, ignoring server name and port
  - creates an Excel file with the results, and flags differences in a column called Match
  - When executed, should see somethiing like the following output:

    4860 parameters returned from Production
    Validated 4860 parameters from Production
    4969 parameters returned from QA
    Validated 4969 parameters from QA
    4989 parameters returned from Production Support
    Validated 4989 parameters from Production Support
    517 parameters not matching

    And an Excel spreadsheet like the following:
    
    MATCH | SECTION           | KEY                  | PORT        | HOST_PR     | VALUE_PR | LAST_CHANGED_PR | HOST_QA     | VALUE_QA | LAST_CHANGED_QA | HOST_PS     | VALUE_PS | LAST_CHANGED_PS
    TRUE  | abstract_sql_plan | capture_thread_count | indexserver | pr-server-1 | 8        |                 | qa-server-1 | 8        |                 | ps-server-1 | 8        |
    TRUE  | abstract_sql_plan | capture_thread_count | xsengine    | pr-server-1 | 8        |                 | qa-server-1 | 8        |                 | ps-server-1 | 8        | 
    TRUE  | abstract_sql_plan | capture_thread_count | dpserver    | pr-server-1 | 8        |                 | qa-server-1 | 8        |                 | ps-server-1 | 8        |
    TRUE  | abstract_sql_plan | capture_thread_count | indexserver | pr-server-2 | 8        |                 | qa-server-2 | 8        |                 | ps-server-2 | 8        |
    TRUE  | abstract_sql_plan | capture_thread_count | indexserver | pr-server-2 | 8        |                 | qa-server-2 | 8        |                 | ps-server-2 | 8        |
    TRUE  | abstract_sql_plan | capture_thread_count | indexserver | pr-server-3 | 8        |                 | qa-server-3 | 8        |                 | ps-server-3 | 8        |
    TRUE  | abstract_sql_plan | capture_thread_count | indexserver | pr-server-4 | 8        |                 | qa-server-4 | 8        |                 | ps-server-4 | 8        |
    TRUE  | abstract_sql_plan | max_count            | xsengine    | pr-server-1 | 1000000  |                 | qa-server-1 | 1000000  |                 | ps-server-1 | 1000000  |
    TRUE  | abstract_sql_plan | max_count            | dpserver    | pr-server-1 | 1000000  |                 | qa-server-1 | 1000000  |                 | ps-server-1 | 1000000  |
    TRUE  | abstract_sql_plan | max_count            | indexserver | pr-server-1 | 1000000  |                 | qa-server-1 | 1000000  |                 | ps-server-1 | 1000000  |
    TRUE  | abstract_sql_plan | max_count            | indexserver | pr-server-2 | 1000000  |                 | qa-server-2 | 1000000  |                 | ps-server-2 | 1000000  |
    TRUE  | abstract_sql_plan | max_count            | indexserver | pr-server-3 | 1000000  |                 | qa-server-3 | 1000000  |                 | ps-server-3 | 1000000  |
    TRUE  | abstract_sql_plan | max_count            | indexserver | pr-server-4 | 1000000  |                 | qa-server-4 | 1000000  |                 | ps-server-4 | 1000000  |
    TRUE  | abstract_sql_plan | max_size             | indexserver | pr-server-1 | 30000    |                 | qa-server-1 | 30000    |                 | ps-server-1 | 30000    |
    TRUE  | abstract_sql_plan | max_size             | xsengine    | pr-server-1 | 30000    |                 | qa-server-1 | 30000    |                 | ps-server-1 | 30000    |
    TRUE  | abstract_sql_plan | max_size             | dpserver    | pr-server-1 | 30000    |                 | qa-server-1 | 30000    |                 | ps-server-1 | 30000    |
    TRUE  | abstract_sql_plan | max_size             | indexserver | pr-server-2 | 30000    |                 | qa-server-2 | 30000    |                 | ps-server-2 | 30000    |
    TRUE  | abstract_sql_plan | max_size             | indexserver | pr-server-3 | 30000    |                 | qa-server-3 | 30000    |                 | ps-server-3 | 30000    |
    TRUE  | abstract_sql_plan | max_size             | indexserver | pr-server-4 | 30000    |                 | qa-server-4 | 30000    |                 | ps-server-4 | 30000    |
