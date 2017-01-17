#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import numpy
import tempfile
import scipy.io.wavfile as wf

# ----------------------------------------------------------------------------------------------- #

def compute_f0_praat(audio_file,input_parms=None):

	# Uses Praat to extract F0 from the audio signal in the file AUDIO_FILE.
	# AUDIO_FILE must be an uncompressed wav file.
	#
	# Valid input parameters are:
	#
	# parms.time_step
	# parms.pitch_floor
	# parms.pitch_ceiling
	# parms.max_n_candidates
	# parms.very_accurate
	# parms.silence_threshold
	# parms.voicing_threshold
	# parms.octave_cost
	# parms.octave_jump_cost
	# parms.voiced_unvoiced_cost
	#
	# See Praat's manual to understand what each of these parameters
	# mean. Non-provided input parameters are assigned default values.
	#
	# Author: Adriano Vilela Barbosa


	# Get the default parameter values of Praat's pitch extraction algorithm
	parms = get_praat_default_f0_parameters();

	# If the input argument 'input_parms' has been provided, we use
	# the provided parameter values to override the default values
	if input_parms is not None:

		# The names of the provided input parameters
		input_parm_names = input_parms.keys();

		# The names of the default parameters
		parm_names = parms.keys();

		# Use the input parameter values provided in 'input_parms' to update
		# the parameter values in 'parms'
		for input_parm_name in input_parm_names:

			if input_parm_name in parm_names:
				parms[input_parm_name] = input_parms[input_parm_name];
			else:
				# warning_message = sprintf('Ignoring invalid parameter ''%s''.',input_parm_name);
				warning_message = "Ignoring invalid parameter '%s'." % input_parm_name;
				# warning(warning_message);
				print(warning_message);


	# Ensure that the pitch floor, when passed to Praat, will result
	# in a window size that will meet the minimum frame size to frame
	# shift ratio (defined in the check_pitch_parms() function)
	# pitch_floor = check_pitch_parms(pitch_floor,time_step);
	# parms.pitch_floor = check_pitch_parms(parms.pitch_floor,parms.time_step);
	parms["pitch_floor"] = check_pitch_parms(parms["pitch_floor"],parms["time_step"]);

	# Temporary name for the pitch file
	temp_file = tempfile.NamedTemporaryFile(delete=False)
	pitch_file_name = temp_file.name
	temp_file.close()


	# The full path to the Praat pitch extraction algorithm
	praat_script_dir = os.path.dirname(os.path.realpath(__file__));
	praat_script_path = os.path.join(praat_script_dir,"extract_pitch_2.praat");

	# The command string to be executed
	praat_command = "praat %s %s %s %.10f %f %g %g %.10f %.10f %.10f %.10f %.10f %f" % (praat_script_path,audio_file,pitch_file_name,parms["time_step"],parms["pitch_floor"],parms["max_n_candidates"],parms["very_accurate"],parms["silence_threshold"],parms["voicing_threshold"],parms["octave_cost"],parms["octave_jump_cost"],parms["voiced_unvoiced_cost"],parms["pitch_ceiling"]);

	# Execute the command string
	os.system(praat_command);

	# Load the pitch file
	praat_pitch = numpy.loadtxt(pitch_file_name);

	# Delete the temporary files
	os.remove(pitch_file_name);

	# Separate the contents of 'praat_pitch' into the time
	# signal (column 1) and the pitch signal (column 2)
	# time_signal  = praat_pitch(:,1);
	# pitch_signal = praat_pitch(:,2);
	time_signal  = praat_pitch[:,0];
	pitch_signal = praat_pitch[:,1];

	# The sampling rate of the F0 signal
	# f0_rate = round(1/min(diff(time_signal)));
	f0_rate = round(1.0/numpy.amin(numpy.diff(time_signal)));

	# Read the audio file
	(audio_rate, audio_signal) = wf.read(audio_file)

	# The last sample of the F0 signal. Praat only returns samples
	# for which an F0 value exists. We create a new, full F0 signal
	# and assign a value of zero (or nan) to the samples not returned
	# by Praat. In order to do that, we need to know the number of
	# samples in the new F0 signal
	end_time = len(audio_signal)/audio_rate;
	end_sample = int(round(end_time*f0_rate));

	# The indices of the samples returned by Praat
	# indices = round(time_signal*f0_rate);
	# indices = numpy.around(time_signal*f0_rate).astype(int);
	indices = numpy.floor(time_signal*f0_rate).astype(int);

	# The new, extended time signal
	# time_signal_2 = [1:end_sample]/f0_rate;
	time_signal_2 = numpy.arange(0,end_sample)/f0_rate;

	# The new, extended pitch signal
	pitch_signal_2 = numpy.empty(time_signal_2.shape);
	pitch_signal_2[:] = numpy.nan;
	pitch_signal_2[indices] = pitch_signal;

	# # The pitch floor may have been modified in order to produce
	# # the desired window size for the pitch analysis (in Praat,
	# # the analysis window size is determined by the pitch floor
	# # in the following way: window_size = 3/pitch_floor). We now
	# # ensure that the pitch signal is within the original pitch
	# # range provided.
	# pitch_signal_2(pitch_signal_2 < pitch_range(1)) = nan;
	# pitch_signal_2(pitch_signal_2 > pitch_range(2)) = nan;

	# Return variables
	return (pitch_signal_2,time_signal_2,parms)

# ----------------------------------------------------------------------------------------------- #

def check_pitch_parms(pitch_floor,time_step):

	# The minimum frame size to frame shift allowed
	# min_size_shift_ratio = 3;
	min_size_shift_ratio = 2.5;

	# The frame shift
	frame_shift = time_step;

	# Praat's default frame size. If this doesn't satisfy the
	# minimum frame size to frame shift requirement, we will
	# have to change it, by changing the pitch floor .
	frame_size = 3.0/pitch_floor;

	# Ensure that the frame size meets the minimum frame size to
	# frame shift ratio
	# frame_size = max([frame_size frame_shift*min_size_shift_ratio]);
	frame_size = max(frame_size, frame_shift*min_size_shift_ratio);

	# Pitch floor value to be passed to Praat that will result in
	# the desired frame size computed above
	pitch_floor = 3.0/frame_size;

	# Return the pitch floor
	return pitch_floor;

# ----------------------------------------------------------------------------------------------- #

def get_praat_default_f0_parameters():

	# Returns the default parameter values of Praat's pitch extraction algorithm
	#
	# Author: Adriano Vilela Barbosa


	# Default input parameters
	parms = {}

	parms["time_step"]            = 0;
	parms["pitch_floor"]          = 75.0;
	parms["pitch_ceiling"]        = 600.0;
	parms["max_n_candidates"]     = 15;
	parms["very_accurate"]        = False;
	parms["silence_threshold"]    = 0.03;
	parms["voicing_threshold"]    = 0.45;
	parms["octave_cost"]          = 0.01;
	parms["octave_jump_cost"]     = 0.35;
	parms["voiced_unvoiced_cost"] = 0.14;

	# Return the parameters
	return parms;

# ----------------------------------------------------------------------------------------------- #
