import matplotlib.pyplot as plt
import numpy as np

def plottool(filename,band,color):
    mjd1=[]
    mag1=[]
    dm1=[]
    mjd2=[]
    mag2=[]
    dm2=[]

    f = open(filename, 'r')
    alldata = f.read()
    rows = alldata.split('\n')
    for row in rows[1:]:
        data = row.split(",")
        if 'None' not in data and data!=[''] and band in data[4]:
            if '>' not in data[1]:
                mjd1.append(float(data[6]))
                mag1.append(float(data[1]))
                dm1.append(float(data[2]))
            else:
                mjd2.append(float(data[6]))
                mag2.append(float(data[1][1:]))
                dm2.append(float(data[2]))
    plt.errorbar(mjd1,mag1,yerr=dm1, fmt='o',color='k',label='o-band',markersize=5,markerfacecolor=color)
    arrow = u'$\u2193$'
    plt.plot(mjd2,mag2,marker=arrow,color=color,label='o-band(>)',markersize=7,linestyle='None')
    if mag1==mag2==[]:
        print 'no such data!'
        return [0,0]
    else:
        return [min(mag1+mag2),max(mag1+mag2)]

def plot(filename):
    magmax=[]
    magmin=[]
    magmin.append(plottool(filename,'o','r')[0])
    magmax.append(plottool(filename,'c','b')[1])
    plt.xlabel('mjd')
    plt.ylabel('magnitude')
    plt.title('light curve of '+filename[:-4])
    plt.legend()
    plt.ylim(max(magmax)*1.05,min(magmin)/1.05)
    plt.savefig('light curve of '+filename[:-3]+'jpg')
    plt.show()

def bandplot(filename,band,color):
    [magmin,magmax]=plottool(filename,band,color)
    if [magmin,magmax]!=[0,0]:
        plt.xlabel('mjd')
        plt.ylabel('magnitude')
        plt.title(band+'band of '+filename[:-4])
        plt.legend()
        plt.ylim(magmax*1.05,magmin/1.05)
        plt.savefig(band+'band of '+filename[:-3]+'jpg')
        plt.show()
        

def judge(filename,band):

    single = 5
    f = open(filename, 'r')
    alldata = f.read()
    rows = alldata.split('\n')

    mjd=[]
    mag=[]
    dm=[]
    intmjd=[]
    sig=[]

    for row in rows[1:]:
        data = row.split(",")
        if 'None' not in data and data != ['']:
            if band in data[4]:
                if '>' in data[1] or not float(data[2]):
                    mag.append(float(data[1][1:]))
                    sig.append(0)
                    dm.append(1)
                else:
                    mag.append(float(data[1]))
                    sig.append(1)
                    dm.append(float(data[2]))
                mjd.append(float(data[6][:-1]))
                intmjd.append(int(float(data[6][:-1])))


    mjdf = []
    magf=[]
    dmf=[]
    i=0

    intmjd.append(0)
    while i<len(sig):
        for j in range(len(sig)):
            if intmjd[i]!=intmjd[i+j+1]:
                break
        mjdf.append(intmjd[i])
        if np.sum(sig[i:i+j+1]):
            magf.append(np.average(mag[i:i+j+1], weights=np.divide(sig[i:i+j+1],np.multiply(dm[i:i+j+1],dm[i:i+j+1]))))
        else:
            magf.append(0)
        i=i+j+1
    intmjd.pop()

    file = open('re_' + band + '_' + filename, 'w')
        
    for num in range(len(magf)):
        if magf[num]:
            k=num+1
            while k<len(magf):
                if not magf[k]:
                    magf.pop(k)
                    mjdf.pop(k)
                else:
                    k=k+1
            file.writelines(str(mjdf[num])+'\n')
            file.writelines(str(int((mjdf[num]-mjdf[num-1])<=5 and bool(num)))+'\n'+str(mjdf[num]-mjdf[num-1])+'\n')
            j=1
            tmp1=0
            tmp2=0
            while mjdf[num+j]-mjdf[num]<=5:
                if magf[num+j-1]<=magf[num+j]:
                    tmp1=1
                j=j+1
                tmp2=1
            if tmp1:
                file.writelines('1')#unproper sample
                break
            elif tmp2:
                file.writelines('0')#proper sample
                break
            else:
                file.writelines('2\n')#no data in 5 days
    file.close()