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
    if mag1 != []:
        plt.errorbar(mjd1,mag1,yerr=dm1, fmt='o',color='k',label='o-band',markersize=5,markerfacecolor=color)
    if mag2 != []:
        arrow = u'$\u2193$'
        plt.plot(mjd2,mag2,marker=arrow,color=color,label='o-band(>)',markersize=7,linestyle='None')
    if mag1==mag2==[]:
        print 'no such data!'
        return [0,0]
    else:
        return [min(mag1+mag2),max(mag1+mag2)]

def plot(filename,a,b,c):
    magmax=[]
    magmin=[]
    magmin.append(plottool(filename,'o','r')[0])
    magmax.append(plottool(filename,'c','b')[1])
    x=np.arange(57870,57930,0.1)
    plt.plot(x,a*x**2+b*x+c,'k')
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

    f = open(filename, 'r')
    f0 = open('re_' + band + '_' + filename, 'w')
    alldata = f.read()
    rows = alldata.split('\n')

    mjd=[]
    mag=[]
    dm=[]
    intmjd=[]

    for row in rows[1:]:
        data = row.split(",")
        if 'None' not in data and data != ['']:
            if band in data[4]:
                if '>' not in data[1] and float(data[2]):
                    mag.append(float(data[1]))
                    dm.append(float(data[2]))
                    mjd.append(float(data[6][:-1]))
                    intmjd.append(int(float(data[6][:-1])))

    mjdf = []
    magf = []
    dmf = []
    i = 0

    intmjd.append(0)
    while i<len(mag):
        for j in range(len(mag)):
            if intmjd[i]!=intmjd[i+j+1]:
                break
        mjdf.append(np.average(mjd[i:i+j+1]))
        magf.append(np.average(mag[i:i+j+1], weights=np.divide(1, np.multiply(dm[i:i+j+1], dm[i:i+j+1]))))
        dmf.append(np.sqrt(np.dot(dm[i:i + j + 1], dm[i:i + j + 1]) / (j+1)))
        i = i+j+1
    intmjd.pop()

    for num in range(len(magf)):
        if mjdf[num+1]-mjdf[num]<=5:
            f0.writelines(str(mjdf[num])+'\n')
            for i in range(5):
                if mjdf[num+i]-mjdf[num] > 5:
                    break
            if i==2:
                f0.writelines(str(np.polyfit(mjdf[num: num + i], magf[num:num + i], 1, w = dmf[num:num + i]))[1:-1])
                return [0]+list(np.polyfit(mjdf[num:num+i], magf[num:num+i], 1, w = dmf[num:num+i]))
            else:
                f0.writelines(str(np.polyfit(mjdf[num:num+i], magf[num:num+i], 2, w = dmf[num:num+i]))[1:-1])
                return np.polyfit(mjdf[num:num+i], magf[num:num+i], 2, w = dmf[num:num+i])
            break
    f0.close()