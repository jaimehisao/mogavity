import mogavity

print("=======================================================")
print("=======Hi! Welcome to the Mogavity Testing Suite=======")
print("=======================================================")

print("We will run a series of tests and show their expected and actual output")

print("=======================================================")
print("TEST 1 - Array Declaration and Access (arrays.mog)")
print("Expected Output \n"
      "7\n"
      "5\n"
      "35\n"
      "64339296875")
print("=======================================================")
print("Actual Output TEST 1 ==================================")
mogavity.compile_and_run("tests/arrays.mog", False, False)
print("=======================================================")
