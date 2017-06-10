# Extract pitch from an audio file and write it out to a text file

# Input parameters:
#	audio_file_name -> input audio file
#	pitch_file_name -> output pitch file
#	pitch_floor     -> minimum pitch value
#	pitch_ceiling   -> maximum pitch value
#	time_step       -> analysis time step, in seconds

# The input parameters
# form PitchExtractor
#	sentence audio_file_name
#	sentence pitch_file_name
#	natural pitch_floor
#	natural pitch_ceiling
#	real time_step
# endform

# The input parameters
form PitchExtractor
	sentence audio_file_name
	sentence pitch_file_name
	real time_step 0.0 (= auto)
	natural pitch_floor 75.0
	natural max_n_candidates 15
	boolean very_accurate false
	positive silence_threshold 0.03
	positive voicing_threshold 0.45
	positive octave_cost 0.01
	positive octave_jump_cost 0.35
	positive voiced_unvoiced_cost 0.14
	natural pitch_ceiling 600.0
endform

# Read the input audio file
# echo Reading audio from 'audio_file_name$'
Read from file... 'audio_file_name$'

# Extract pitch
# To Pitch... 0.0 75 500
# To Pitch... 'time_step' 'pitch_floor' 'pitch_ceiling'
To Pitch (ac)... 'time_step' 'pitch_floor' 'max_n_candidates' 'very_accurate' 'silence_threshold' 'voicing_threshold' 'octave_cost' 'octave_jump_cost' 'voiced_unvoiced_cost' 'pitch_ceiling'

# Get the number of samples in the pitch object
pitchID = selected("Pitch");
Down to PitchTier
pitchtierID = selected("PitchTier")
n_samples = Get number of points

# If a pitch file with the given name already exists,
# we delete it  before we write the new pitch values.
# We need to do this to ensure that the output file
# is empty, as the new pitch values are appended to
# the file
filedelete 'pitch_file_name$'

# Print out a progress message
# echo Writing pitch to 'pitch_file_name$'

# Loop over the samples in the pitch object and write
# them to the output pitch file. We do this instead
# of simply saving the pitch object to a text file
# because we want a simpler file containing only
# two columns: time and pitch value
for i to n_samples
	time = Get time from index... i
	hertz = Get value at index... i
	fileappend 'pitch_file_name$' 'time' 'hertz' 'newline$'
endfor

#-----------------------------------------------------------------------------#
