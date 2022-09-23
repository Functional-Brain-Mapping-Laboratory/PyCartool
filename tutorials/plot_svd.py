"""
Conpute SVD
====================

"""

import matplotlib.pyplot as plt
import numpy as np

# %%
import pycartool as cart

# %% [markdown]
# #### Import  from Cartool files

# %%
fname_spi = "MNI152.NlinAsym09c.204.5000.2017.spi"
fname_roi = "MNI152.NlinAsym09c.204.5000.2017.AAL.rois"

spi = cart.spi.read_spi(fname_spi)
roi = cart.rois.read_roi(fname_roi, spi)

# %% [markdown]
# #### Constants

# %%
sfreq = 512
n_sources = len(spi.names)
snr = 10
n_times = 2048

# %% [markdown]
# ### Simulate sources time course

# %% [markdown]
# Here we simulate the sources time course as random noise generators everywhere in the brain, expect in the first Region of interest where sources time course are simulated are sin waves in the x direction.

# %% [markdown]
# #### Create random noise

# %%
simulated_tc = np.random.normal(size=(n_sources, 3, n_times))

# %%
plt.figure()
plt.plot(simulated_tc[0, 0], color="navy")
plt.title("Time course of a source outside the first Roi")
plt.show()

# %% [markdown]
# #### Create sin wave in Roi

# %%
x = np.arange(0, n_times, 1)
sin = snr * np.sin(x / (2 * np.pi))

# %%
for elem in roi.groups_of_indexes[0]:
    simulated_tc[elem][0] = sin
    simulated_tc[elem][1] = np.zeros(sin.shape)
    simulated_tc[elem][2] = np.zeros(sin.shape)

# %%
plt.figure()
plt.plot(sin, color="red")
plt.title("Time course of sources inside the first Roi  (x direction)")
plt.show()

# %%
source_estimate_simulated = cart.ris.SourceEstimate(
    simulated_tc, sfreq=sfreq, source_space=spi
)

# %% [markdown]
# #### Compute the regions of interest time course

# %%
roi_t_simulated = source_estimate_simulated.compute_rois_tc(roi)

# %%
plt.figure()
plt.plot(roi_t_simulated.sources_tc[0:4, 0, :].T)
plt.title("Rois time course")
plt.show()

# %% [markdown]
#
