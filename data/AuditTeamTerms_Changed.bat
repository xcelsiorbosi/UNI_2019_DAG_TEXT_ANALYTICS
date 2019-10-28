echo off
sqlcmd -S DA-PROD1 -d HANSARD -E -Q "DELETE FROM HANSARD.dbo.KeyTerms;"
"C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\python.exe" "..\analytics\ssis\ssis_text_analytics.py"
set /p delExit=Press the ENTER key to exit...: