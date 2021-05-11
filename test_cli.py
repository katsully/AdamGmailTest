import subprocess
import re
result = subprocess.run(["C:\\Users\\kmsul\\AJO_Game\\Adam\\signal-cli\\build\\install\\signal-cli\\bin\\signal-cli.bat", "-u", "+16503088054", "receive"], stdout=subprocess.PIPE, errors='ignore', encoding='utf-8').stdout	

print(result)
num = [word for word in result.split() if word.startswith('+')][0]
print(num[1:])
