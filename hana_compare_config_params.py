# Compare config parameters across 3 scale-out hana databases
# create excel file with results, including flagging differences

from hdbcli import dbapi
import time
import pandas as pd

cnt=0

##### Begin Production Section #####

# Define connection to HANA
connpr = dbapi.connect(
    key='<hdbuserstore entry>',
    encrypt='true'
)

cursorpr = connpr.cursor()

sql_result_pr = pd.read_sql("""
	SELECT
		 HOST AS HOST_PR,
		 PORT AS PORT,
		 SECTION,
		 KEY,
		 VALUE AS VALUE_PR
	FROM M_CONFIGURATION_PARAMETER_VALUES 
	ORDER BY 
		 SECTION,
		 KEY,
		 HOST
                        """, connpr)
dfpr = pd.DataFrame(sql_result_pr)

print("{} parameters returned from Production".format(len(dfpr)))

for tspr in dfpr.itertuples():
    parnumpr = (getattr(tspr, 'Index') + 1)
    print('Validating parameter number: %d\r'%parnumpr, end="")
    tsresultpr = pd.read_sql("""
		SELECT
			MAX(TIMESTAMP) AS LAST_CHANGED_PR
		FROM AUDIT_LOG 
		where SECTION = '{}' 
		AND KEY = '{}'
    """.format(tspr.SECTION,tspr.KEY), connpr)
    dfpr.at[tspr.Index, "LAST_CHANGED_PR"] = tsresultpr.iloc[0,0]
print("Validated {} parameters from Production".format(parnumpr))

cursorpr.close()
connpr.close()

##### End Production Section #####

##### Begin QA Section #####

connqa = dbapi.connect(
    key='<hdbuserstore entry>',
    encrypt='true'
)

cursorqa = connqa.cursor()

sql_result_qa = pd.read_sql("""
	SELECT
		 HOST AS HOST_QA,
		 PORT AS PORT,
		 SECTION,
		 KEY,
		 VALUE AS VALUE_QA
	FROM M_CONFIGURATION_PARAMETER_VALUES 
	ORDER BY 
		 SECTION,
		 KEY,
		 HOST
                        """, connqa)
dfqa = pd.DataFrame(sql_result_qa)
print("{} parameters returned from QA".format(len(dfqa)))

for tsqa in dfqa.itertuples():
    parnumqa = (getattr(tsqa, 'Index') + 1)
    print('Validating parameter number: %d\r'%parnumqa, end="")
    tsresultqa = pd.read_sql("""
		SELECT
			MAX(TIMESTAMP) AS LAST_CHANGED_QA
		FROM AUDIT_LOG 
		where SECTION = '{}' 
		AND KEY = '{}'
    """.format(tsqa.SECTION,tsqa.KEY), connqa)
    dfqa.at[tsqa.Index, "LAST_CHANGED_QA"] = tsresultqa.iloc[0,0]
print("Validated {} parameters from QA".format(parnumqa))

cursorqa.close()
connqa.close()

##### End QA Section #####

##### Begin PS Section #####

connps = dbapi.connect(
    key='<hdbuserstore entry>',
    encrypt='true'
)

cursorps = connps.cursor()

sql_result_ps = pd.read_sql("""
	SELECT
		 HOST AS HOST_PS,
		 PORT AS PORT,
		 SECTION,
		 KEY,
		 VALUE AS VALUE_PS
	FROM M_CONFIGURATION_PARAMETER_VALUES 
	ORDER BY 
		 SECTION,
		 KEY,
		 HOST
                        """, connps)
dfps = pd.DataFrame(sql_result_ps)
print("{} parameters returned from Production Support".format(len(dfps)))

for tsps in dfps.itertuples():
    parnumps = (getattr(tsps, 'Index') + 1)
    print('Validating parameter number: %d\r'%parnumps, end="")
    tsresultps = pd.read_sql("""
		SELECT
			MAX(TIMESTAMP) AS LAST_CHANGED_PS
		FROM AUDIT_LOG 
		where SECTION = '{}' 
		AND KEY = '{}'
    """.format(tsps.SECTION,tsps.KEY), connps)
    dfps.at[tsps.Index, "LAST_CHANGED_PS"] = tsresultps.iloc[0,0]
print("Validated {} parameters from Production Support".format(parnumps))

cursorps.close()
connps.close()

##### End PS Section #####

# Change hostnames to node1, node2, etc., so that comparisons don't
# find differences just because the hostname is different
# Likewise, change port numbers to service names for the same purpose

dfpr.loc[dfpr.HOST_PR == "<pr server 1>", "NODE"] = "node1"
dfpr.loc[dfpr.HOST_PR == "<pr server 2>", "NODE"] = "node2"
dfpr.loc[dfpr.HOST_PR == "<pr server 3>", "NODE"] = "node3"
dfpr.loc[dfpr.HOST_PR == "<pr server 4>", "NODE"] = "node4"
dfpr.loc[dfpr.PORT == 30103, 'PORT'] = 'indexserver'
dfpr.loc[dfpr.PORT == 30111, 'PORT'] = 'dpserver'
dfpr.loc[dfpr.PORT == 30140, 'PORT'] = 'xsengine'
dfqa.loc[dfqa.HOST_QA == "<qa server 1>", "NODE"] = "node1"
dfqa.loc[dfqa.HOST_QA == "<qa server 2>", "NODE"] = "node2"
dfqa.loc[dfqa.HOST_QA == "<qa server 3>", "NODE"] = "node3"
dfqa.loc[dfqa.HOST_QA == "<qa server 4>", "NODE"] = "node4"
dfqa.loc[dfqa.PORT == 30103, 'PORT'] = 'indexserver'
dfqa.loc[dfqa.PORT == 30111, 'PORT'] = 'dpserver'
dfqa.loc[dfqa.PORT == 30107, 'PORT'] = 'xsengine'
dfps.loc[dfps.HOST_PS == "<ps server 1>", "NODE"] = "node1"
dfps.loc[dfps.HOST_PS == "<ps server 2>", "NODE"] = "node2"
dfps.loc[dfps.HOST_PS == "<ps server 3>", "NODE"] = "node3"
dfps.loc[dfps.HOST_PS == "<ps server 4>", "NODE"] = "node4"
dfps.loc[dfps.PORT == 30103, 'PORT'] = 'indexserver'
dfps.loc[dfps.PORT == 30111, 'PORT'] = 'dpserver'
dfps.loc[dfps.PORT == 30107, 'PORT'] = 'xsengine'

# Join PR/QA/PS dataframes

mid = pd.merge(dfpr, dfqa, how="outer", on=["SECTION", "KEY", "NODE", "PORT"])
result = pd.merge(mid, dfps, how="outer", on=["SECTION", "KEY", "NODE", "PORT"])

# Identify matching/non-matching parameters

for row in result.itertuples():
    if (row.VALUE_PR == row.VALUE_QA) & (row.VALUE_PR == row.VALUE_PS):
        result.at[row.Index, "MATCH"] = "TRUE"
    else:
        result.at[row.Index, "MATCH"] = "FALSE"
        cnt+=1
        
# Write output to Excel file

result = result[["MATCH","SECTION","KEY","PORT","HOST_PR","VALUE_PR","LAST_CHANGED_PR","HOST_QA","VALUE_QA","LAST_CHANGED_QA","HOST_PS","VALUE_PS","LAST_CHANGED_PS"]]
result.to_excel("HANA_Config_Param_Comparison_{}.xlsx".format(time.strftime("%Y%m%d-%H%M%S")))
print("{} parameters not matching".format(cnt))
