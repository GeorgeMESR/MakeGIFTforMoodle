import numpy as np
import scipy.constants as const
import test
import random
import matplotlib.pyplot as plt


tst=test.tests()
tst.AddCategor('Период функции')

N=50 # число вопросов теста


unitsF=['Гц', 'кГц', 'MГц', 'ГГц', 'TГц']
unitsT=['с', 'мс', 'мкс', 'нс', 'pc', 'фс']
for i in range(N):

    T_pwr= -random.random()*9 # диаппазон большой, лучше рандомизировать log частоты
    T, Tprn, Tpwr, unit_indx   = test.PhysicalFormatNumber(10**T_pwr)

    test.plot_figure_preambule("время (%sсекунд)" % (test.SiPrefixRUSfull[unit_indx]), 'x')

    x=np.linspace(0,Tprn*(8+random.random()*2),1024)
    phi=random.random()*2*np.pi
    y=np.sin(2*np.pi*x/Tprn+phi)

    plt.plot(x,y)

    fig0=test.plot_figure_convertimageToBase64()


    text_qst='Из рисунка <p><img src="%s" alt="" /></p> определите <B>линейную</B> частоту' % (fig0)


    valueR, valueRprn, valueRpwr, valueRunit_indx=test.PhysicalFormatNumber(1/T)
    test_answR='%g %sгерц' %(valueRprn, test.SiPrefixRUSfull[valueRunit_indx])

    valueW1, valueW1prn, valueW1pwr, valueW1unit_indx=test.PhysicalFormatNumber(2*np.pi/T)
    commentW1='расчет для периода проводится по формуле 1/T, а не 2 pi /Т'
    test_answW1='%g %sгерц' %(valueW1prn, test.SiPrefixRUSfull[valueW1unit_indx])

    valueW2, valueW2prn, valueW2pwr, valueW2unit_indx=test.PhysicalFormatNumber(1/T)
    commentW2='обратите внимание на размерность'
    test_answW2='%g %sгерц' %(valueW2prn, test.SiPrefixRUSfull[valueW2unit_indx+1])

    valueW3, valueW3prn, valueW3pwr, valueW3unit_indx=test.PhysicalFormatNumber(2*np.pi/T)
    commentW3='расчет для периода проводится по формуле 1/Т, а не 2 pi /Т, обратите внимание на размерность'
    test_answW3='%g %sгерц' %(valueW3prn, test.SiPrefixRUSfull[valueW3unit_indx-1])




    tst.defaultcat.qsts.append(test.qst())
    tst.defaultcat.qsts[-1].txt=text_qst
    tst.defaultcat.qsts[-1].AddNew(test_answR, 1, '')
    tst.defaultcat.qsts[-1].AddNew(test_answW1, 0, commentW1)
    tst.defaultcat.qsts[-1].AddNew(test_answW2, 0, commentW2)
    tst.defaultcat.qsts[-1].AddNew(test_answW3, 0, commentW3)


test.SaveTest('period2.txt',tst)
test.SaveTestInHtml('period2.htm', tst)




