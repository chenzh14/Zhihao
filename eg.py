import chenzh
import os
for file in os.listdir(os.getcwd()):
    if file[:5]=='ATLAS':
        [a,b,c]=chenzh.judge(file,'')
        chenzh.plot(file,a,b,c)