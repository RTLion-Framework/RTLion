from pylab import *
from rtlsdr import *

sdr = RtlSdr()

# configure device
sdr.sample_rate = 2.4e6
sdr.center_freq = 90e6
sdr.gain = 4

samples = sdr.read_samples(256*1024)


#print(np.where(samples==samples.max()))
    #print(str(sample.real) + " ||| " + str(sample.imag))

#for mag in mags:
    #print(mag)

sdr.close()

# use matplotlib to estimate and plot the PSD


[Y, F] = psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
xlabel('Frequency (MHz)')
ylabel('Relative power (dB)')

n = 3
biggest_nums = Y[np.argsort(Y)[-n:]]
for num in biggest_nums:
    freq_val = F[np.where(Y == num)[0][0]]
    print(freq_val)
#max = np.max(Y)
#print(F[np.where(Y == max)[0][0]])

#log=10*math.log10(max)
#print(log)


show()