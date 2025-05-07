import matplotlib.pyplot as plt
from scipy.fftpack import fft, irfft, rfft
from thesis.src.lib.combine import combine_cobb_douglas
from thesis.src.lib.transform import transform_cobb_douglas

if __name__ == '__main__':
    # =========================================================================
    # Discrete Fourier Transform
    # =========================================================================
    YEAR_BASE = 1899

    df = combine_cobb_douglas().pipe(
        transform_cobb_douglas, year_base=YEAR_BASE
    )[0].iloc[:, [3, 4]]

    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    df['lab_cap_int_ft'] = df['lab_cap_int'].apply(rfft)

    plt.plot(df['lab_cap_int'])
    plt.plot(df['lab_cap_int_ft'], 'r:')
    plt.grid()
    plt.legend()
    plt.show()
