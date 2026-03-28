passed = 0
failed = 0
not_executed = 0
with open("testslog_results.txt","r" ) as file:
    for f in file:
        if "PASSED" in f:
            passed = passed + 1 
        elif "FAILED" in f:
            failed = failed + 1 
        elif "Not Executed" in f:
            not_executed = not_executed +1 

print("Passed Testscases:", passed) 
print("Failed Testscases:", failed) 
print("Not executed Testscases:", not_executed) 
