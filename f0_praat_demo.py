    #!/usr/bin/python
# -*- coding: utf-8 -*-

import f0_praat
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------------------------- #

# The name of the audio file
audio_file = "/home/tiagohbalves/Documentos/Eclipse/Processing/Nova_Gravacao_2.wav";


#Diretório dos modelos de treinamentos e teste
dire_file = "/home/tiagohbalves/Documentos/Eclipse/Processing/LapsBM1.4";




# The base rate
srate = 100.0;

# The pitch range to be used by the pitch extraction algorithm
pitch_range = (70, 500);
# pitch_range = (120 400);
#pitch_range = (140, 400);

# Parameters for Praat's pitch extraction algorithm
input_parms = {};
input_parms["time_step"]     = 1.0/srate;
input_parms["pitch_floor"]   = pitch_range[0];
input_parms["pitch_ceiling"] = pitch_range[1];

# Extract the F0 signal
(f0_signal,f0_time,f0_parms) = f0_praat.compute_f0_praat(audio_file,input_parms);

# Plot the F0 signal
plt.plot(f0_time, f0_signal);
plt.grid("on");
plt.show();

# ----------------------------------------------------------------------------------------------- #
