print('helo')

from praatinterface import PraatLoader

pl = PraatLoader(praatpath = '/home/tiagohbalves/Downloads/praat')

text = pl.run_script('formants.praat', '/home/tiagohbalves/Downloads/wave1.wav',5,5500)

formants = pl.read_praat_out(text)