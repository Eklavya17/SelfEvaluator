import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt
import lightkurve as lk
from scipy.signal import find_peaks

# Downloading the Kepler-90 light curves
lcfs = lk.search_lightcurve('Kepler-90', mission='Kepler').download_all()[:12]

def squelch_rednoise(lc):
    corrected_lc = lc.remove_outliers(sigma_upper=10, sigma_lower=10).normalize().flatten(window_length=101)
    return corrected_lc

stitched_lc = lcfs.stitch(corrector_func=squelch_rednoise)

clc = stitched_lc.remove_nans().bin(time_bin_size=15*u.min)

# Plotting the cleaned light curve
# clc.plot()

bls_periodogram = clc.to_periodogram(method="bls", period=np.arange(50, 500, 0.01), frequency_factor=0.1)

peaks, _ = find_peaks(bls_periodogram.power.value, height=10)

plt.plot(bls_periodogram.period, bls_periodogram.power)
plt.plot(bls_periodogram.period[peaks], bls_periodogram.power[peaks], "x")
plt.xscale('log')
plt.xticks(ticks=[50, 100, 200, 300, 400], labels=[50, 100, 200, 300, 400])
plt.show()

# Checking the peaks and removing periods that are half or a third of others
peak_periods = bls_periodogram.period[peaks].value
peak_powers = bls_periodogram.power[peaks].value

# Sorting the peaks by period
peak_periods, peak_powers = zip(*sorted(zip(peak_periods, peak_powers)))

possible_periods = []
for period, power in zip(peak_periods, peak_powers):
    half_period = period/2
    third_period = period/3
    if not any(np.isclose(possible_periods, half_period, rtol=1e-1)) and \
       not any(np.isclose(possible_periods, third_period, rtol=1e-1)):
        possible_periods.append(period)
        
# Printing the periods
for period in possible_periods:
    print(f"Period: {period}")
    
# Selecting four periods from different ranges
selected_periods = []
for lb in np.arange(0, 400, 100):
    for period in possible_periods:
        if lb < period <= lb + 100:
            selected_periods.append(period)
            break

# Refining the periods
refined_periods = []
for period in selected_periods:
    period_grid = np.linspace(period-5, period+5, 5000)
    bls_periodogram_zoom = clc.to_periodogram(method="bls", period=period_grid)
    refined_periods.append(bls_periodogram_zoom.period_at_max_power.value)

# Plotting the folded light curves
for period in refined_periods:
    lc_fold = clc.fold(period)
    lc_fold.plot()
    plt.title(f"Folded light curve for period {period} days")
    plt.show()