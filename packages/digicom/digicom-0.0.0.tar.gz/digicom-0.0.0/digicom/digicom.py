from numpy import arctan, average, cos, log2, log10, pi, sin, sqrt

ohms = 'Ω'
deg = '°'
powers = { 'm': 10**-3, 'µ': 10**-6, 'n': 10**-9, 'p': 10**-12,
        'f': 10**-15, 'a': 10**-18, 'z': 10**-21, 'y': 10**-24,
        '-': 1, 'k': 10**3, 'M': 10**6, 'G': 10**9,
        'T': 10**12, 'P': 10**15, 'E': 10**18, 'Z': 10**21,
        'Y': 10**24 }

mu0 = 1.256 * 10**-6 # H/m
mur = 1.0000003 # air
bw = lambda capacity, snr: capacity/log2(1 + snr)
bw = lambda freq_amp: 2*freq_amp
capacitive_reactance = lambda f,c: 1 / (2*pi*f*c)
capacity = lambda bw, snr: bw * log2(snr)
capturerange = lambda tolerance: 2*tolerance
carrier_sig_freq_max = lambda fmax, fi: fmax - fi
carrier_sig_freq_min = lambda fmin, fi: fmin + fi
current = lambda r, v: v/r
dbm_to_watts = lambda dbm: 10**((dbm)*10)
dissapation = lambda quality: 1/quality
dynamicrange = lambda input_intercept, noise_floor: (2/3)*(input_intercept - noise_floor)
ei  = lambda output_fmax, output_fmin, fmax, fmin, amps: (output_fmax - output_fmin)/((fmax - fmin)/amps)
emf = lambda n,phee,t: -n * (phee / t)
freq = lambda t: 1 / t
freq_amp = lambda sideband, freq: sideband * freq
imagefrequency = lambda fi, fs: 2*fi + fs
inductive_reactance = lambda f,l: 2*pi*f*l
it = lambda et, zt: et/zt
lockrange = lambda input_tolerance: 2*input_tolerance
modulation_idx = lambda dev, freq: dev/freq
noise = lambda signal, capacity, bw: signal/(2**(capacity / bw) - 1)
noise_amp = lambda signal, capacity, bw: signal/(2**(capacity / bw) - 1)
pc = lambda pt: (1/pt)
percent_modulation = lambda a,b: round((b-a)/(b+a), 3) * 100
period = lambda f: 1 / f
power = lambda v, i:  v * i
psb = lambda pt, pc: round(pt - pc,3)*100
pssb = lambda pc, mu: round((pc*(mu**2))/4, 3)
pt = lambda m: (1 + (m/2))
pvolt = lambda w, i:  w / i
q_capacitor = lambda susceptance, conductance: susceptance / conductance
q_inductor = lambda reactance,resistance: reactance / resistance
quality_factory = lambda x,r: x / r
r2d = lambda r: r * (pi/180)
radiohorizon = lambda ht, hr: sqrt(2*ht) + sqrt(2*hr)
reactancecapacitive = lambda f,c: 1 / (2*pi*f*c)
reactanceinductive = lambda f,l: 2*pi*f*l
resistance = lambda i, v:  i / v
resonant_freq = lambda l,c: 1 / (2 * pi) * sqrt(l * c)
signal = lambda capacity, bw, noise: ((capacity/(bw))-1)/noise
signal_amp = lambda capacity, bw, noise: ((capacity/bw)-1)/noise
snr = lambda sig, noise: sig / noise
snr_ratio = lambda sono_db: round(10 ** (sono_db/10), 3)
sono_db = lambda sini, nf: sini - nf
theta = lambda x,y: arctan((y/x))
total_frequency_deviation = lambda k, ei: (k)*ei
v_to_vdb = lambda v: round(20.0*log10(v) + 120, 3)
voltage = lambda i, r: i * r
vp = lambda vrms: round(vrms * sqrt(2), 4)
vpp = lambda vp: round(2 * vp, 4)
vrms = lambda vp: round(vp / (sqrt(2)), 4)
w_to_dbm = lambda w: round(10.0*log10(w*1000), 3)
wavefront = lambda pt, r: pt / (4 * pi * r**2)
x = lambda z,theta: z*cos(theta)
y = lambda z,theta: z*sin(theta)
z = lambda x,y: sqrt(x**2 + y**2)
"""
This class contains functions which perform Ohm's law and power 
law calculations based on variables from user input
"""
def parse_sym(strnum):
    _strnum = strnum.split(' ')
    significant = float(_strnum[0])
    power = float(powers.get(_strnum[1]))
    return (significant * power)


def get_precision(measurements) -> float:
    avg = average(measurements)
    high = max(measurements)
    low = min(measurements)
    _prec = max([abs( high - avg), abs(low - avg)]) / avg
    prec = round(_prec, 5) * 100
    return prec


def get_accuracy(actual, measurements) -> float:
    _acc = (max([abs(max(measurements)) - actual,
                 min(measurements) - actual]) / actual) * 100
    acc = round(_acc, 5)
    return acc


def get_resolution(measurements, unit=None) -> dict:
    i = 0
    res = {}
    for m in measurements:
        i += len(str(m))
    n_digits = str(int(i / len(measurements))) + ' 1/2'
    res['digits'] = n_digits

    return res


def get_err(measurement, actual, tolerance = 5) -> float:
    err = round(((measurement - actual ) / actual ), 3)
    if abs(err) > tolerance:
        print('Tolerance: ', False)
        return err
    print('Tolerance: ', True)
    return err

