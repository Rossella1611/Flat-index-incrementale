@echo on
set PYTHONPATH=.
python compare_strategies_script/compare_strategies.py --plot
echo Exit code: %ERRORLEVEL%
pause