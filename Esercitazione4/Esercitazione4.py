from pylab import *
path = "C:\\Users\\Roberto\\Documents\\GitHub\\Lab3\\"
#path = "C:\\Users\\Studenti\\Desktop\\Lab3\\"
#path = "/home/alessandro/Documents/Università/3°anno/Laboratorio3/Lab3/"
sys.path = sys.path + [path]
from analyzer import *
import uncertainties
dir= path + "Esercitazione4\\"

###########################################################################

#Guadagno per piccoli segnali

Vin, Vout = loadtxt(dir+"data/guadagnopiccolisegnali.txt", unpack= True)

dVin = Vin*0.035
dVout = Vout*0.035

Vin = unumpy.uarray(Vin, dVin)
Vout = unumpy. uarray(Vout, dVout)

index = arange(len(Vin))
Av = Vout/Vin
dAv = unumpy.std_devs(Av)
Av = unumpy.nominal_values(Av)

Afit, sigmaA = fit_const_yerr(Av, dAv)
dAfit = sqrt(sigmaA)

# plot

figure(1)
subplot(211)
title("Guadagno per piccoli segnali")
ylabel("guadagno")

errorbar(index, Av, dAv, fmt = "b,")
x = linspace(0, max(index), 1000)
y = linspace(Afit, Afit, 1000)
grid()
xticks(arange(0))
plot(x,y,"g")

# scarti normalizzati

subplot(212)
ylabel("scarti normalizzati")
grid()
xticks(arange(0))
plot(index, (Av-Afit)/dAv, ".", color="blue")
savefig(dir+"grafici/fit_guadagnopiccolisegnali.pdf")

#Chi quadro

chi = sum((Av-Afit)**2/dAv**2)
ndof = len(Av) - 1
print("\nFIT RESULT guadagno piccoli segnali\n")
print("Av = ", Afit, "\pm", dAfit)
print("chi / ndof =",chi,"/",ndof, "\n")

###########################################################################

#FREQUENCY DOMAIN#

file="f_domain"
V1 = uncertainties.ufloat(1.00,1.00*0.035)

def f(x, a, b, c):
    return c/sqrt(1+(a/x)**2)*1/sqrt(1+(x/b)**2)

p0=[1,1,1]

def XYfun(a):
    return a[0],a[1]/V1

unit=["tempo_osc","volt_osc"]

titolo="Diagramma di Bode"
Xlab="Frequenza [Hz]"
Ylab="Guadagno $A_v$"

tab=["Frequenza [Hz]","$V_{OUT}$ [$V$]"]

fit(dir,file,unit,f,p0,titolo,Xlab,Ylab,XYfun,preplot=True,table=True,tab=tab,Xscale="log",Yscale="log")

###########################################################################

#GUADAGNO CON C_E#

file="C_E"

def f(x, a):
    return 0*x + a

p0=[40]

def XYfun(a):
    return a[0],a[1]/a[0]

unit=["volt_osc","volt_osc"]

titolo="Guadagno con condensatore $C_E$"
Xlab="Tensione di ingresso $V_{IN}$ [$V$]"
Ylab="Guadagno $A_v$"

tab=["$V_{IN} [$V$]$","$V_{OUT}$ [$V$]"]

fit(dir,file,unit,f,p0,titolo,Xlab,Ylab,XYfun,preplot=True,table=True,tab=tab)

###########################################################################