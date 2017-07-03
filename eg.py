import chenzh
import os
for file in os.listdir(os.getcwd()):
    if file=='ATLAS17gvm.txt':
        chenzh.judge(file,'o')