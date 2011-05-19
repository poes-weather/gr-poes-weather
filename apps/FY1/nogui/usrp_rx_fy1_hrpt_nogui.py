#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: USRP Feng-Yun 1 HRPT Receiver
# Author: POES Weather Ltd
# Description: Feng-Yun 1 HRPT Receiver
# Generated: Wed Dec 15 21:23:06 2010
##################################################

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import noaa
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from grc_gnuradio import usrp as grc_usrp
from optparse import OptionParser
from time import strftime, localtime
import ConfigParser
import math, os
import poesweather

class usrp_rx_fy1_hrpt_nogui(gr.top_block):

	def __init__(self, sync_check=False, gain=35, side="A", freq=1700.5e6, decim=16, satellite='FENGYUN-1D', frames_file=os.environ['HOME'] + '/FENGYUN-1D.hrpt'):
		gr.top_block.__init__(self, "USRP Feng-Yun 1 HRPT Receiver")

		##################################################
		# Parameters
		##################################################
		self.sync_check = sync_check
		self.gain = gain
		self.side = side
		self.freq = freq
		self.decim = decim
		self.satellite = satellite
		self.frames_file = frames_file

		##################################################
		# Variables
		##################################################
		self.sym_rate = sym_rate = 600*1109*2
		self.samp_rate = samp_rate = 64e6/decim
		self.sps = sps = samp_rate/sym_rate
		self.config_filename = config_filename = os.environ['HOME']+'/.gnuradio/fy1_hrpt.conf'
		self._saved_pll_alpha_config = ConfigParser.ConfigParser()
		self._saved_pll_alpha_config.read(config_filename)
		try: saved_pll_alpha = self._saved_pll_alpha_config.getfloat("satname", 'pll_alpha')
		except: saved_pll_alpha = 0.005
		self.saved_pll_alpha = saved_pll_alpha
		self._saved_gain_config = ConfigParser.ConfigParser()
		self._saved_gain_config.read(config_filename)
		try: saved_gain = self._saved_gain_config.getfloat("satname", 'gain')
		except: saved_gain = gain
		self.saved_gain = saved_gain
		self._saved_clock_alpha_config = ConfigParser.ConfigParser()
		self._saved_clock_alpha_config.read(config_filename)
		try: saved_clock_alpha = self._saved_clock_alpha_config.getfloat("satname", 'clock_alpha')
		except: saved_clock_alpha = 0.001
		self.saved_clock_alpha = saved_clock_alpha
		self.max_clock_offset = max_clock_offset = 0.1
		self.max_carrier_offset = max_carrier_offset = 2*math.pi*100e3/samp_rate
		self.hs = hs = int(sps/2.0)

		##################################################
		# Blocks
		##################################################
		self.agc = gr.agc_cc(1e-5, 1.0, 1.0/32768.0, 1.0)
		self.gr_binary_slicer_fb_0 = gr.binary_slicer_fb()
		self.gr_clock_recovery_mm_xx_0 = gr.clock_recovery_mm_ff(sps/2.0, saved_clock_alpha**2/4.0, 0.5, saved_clock_alpha, max_clock_offset)
		self.gr_file_sink_0_0 = gr.file_sink(gr.sizeof_short*1, frames_file)
		self.gr_file_sink_0_0.set_unbuffered(False)
		self.gr_interleaved_short_to_complex_0 = gr.interleaved_short_to_complex()
		self.gr_moving_average_xx_0 = gr.moving_average_ff(hs, 1.0/hs, 4000)
		self.pll = noaa.hrpt_pll_cf(saved_pll_alpha, saved_pll_alpha**2/4.0, max_carrier_offset)
		self.poesweather_fy1_hrpt_decoder_0 = poesweather.fy1_hrpt_decoder(True,False)
		self.poesweather_fy1_hrpt_deframer_0 = poesweather.fy1_hrpt_deframer(sync_check)
		self.usrp_simple_source_x_0 = grc_usrp.simple_source_s(which=0, side=side, rx_ant="RXA")
		self.usrp_simple_source_x_0.set_decim_rate(decim)
		self.usrp_simple_source_x_0.set_frequency(freq, verbose=True)
		self.usrp_simple_source_x_0.set_gain(gain)

		##################################################
		# Connections
		##################################################
		self.connect((self.gr_clock_recovery_mm_xx_0, 0), (self.gr_binary_slicer_fb_0, 0))
		self.connect((self.agc, 0), (self.pll, 0))
		self.connect((self.pll, 0), (self.gr_moving_average_xx_0, 0))
		self.connect((self.gr_moving_average_xx_0, 0), (self.gr_clock_recovery_mm_xx_0, 0))
		self.connect((self.poesweather_fy1_hrpt_deframer_0, 0), (self.gr_file_sink_0_0, 0))
		self.connect((self.usrp_simple_source_x_0, 0), (self.gr_interleaved_short_to_complex_0, 0))
		self.connect((self.gr_interleaved_short_to_complex_0, 0), (self.agc, 0))
		self.connect((self.gr_binary_slicer_fb_0, 0), (self.poesweather_fy1_hrpt_deframer_0, 0))
		self.connect((self.poesweather_fy1_hrpt_deframer_0, 0), (self.poesweather_fy1_hrpt_decoder_0, 0))

	def set_sync_check(self, sync_check):
		self.sync_check = sync_check

	def set_gain(self, gain):
		self.gain = gain
		self.set_saved_gain(self.gain)
		self._saved_gain_config = ConfigParser.ConfigParser()
		self._saved_gain_config.read(self.config_filename)
		if not self._saved_gain_config.has_section("satname"):
			self._saved_gain_config.add_section("satname")
		self._saved_gain_config.set("satname", 'gain', str(self.gain))
		self._saved_gain_config.write(open(self.config_filename, 'w'))
		self.usrp_simple_source_x_0.set_gain(self.gain)

	def set_side(self, side):
		self.side = side

	def set_freq(self, freq):
		self.freq = freq
		self.usrp_simple_source_x_0.set_frequency(self.freq)

	def set_decim(self, decim):
		self.decim = decim
		self.set_samp_rate(64e6/self.decim)
		self.usrp_simple_source_x_0.set_decim_rate(self.decim)

	def set_satellite(self, satellite):
		self.satellite = satellite

	def set_frames_file(self, frames_file):
		self.frames_file = frames_file

	def set_sym_rate(self, sym_rate):
		self.sym_rate = sym_rate
		self.set_sps(self.samp_rate/self.sym_rate)

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.set_sps(self.samp_rate/self.sym_rate)
		self.set_max_carrier_offset(2*math.pi*100e3/self.samp_rate)

	def set_sps(self, sps):
		self.sps = sps
		self.set_hs(int(self.sps/2.0))
		self.gr_clock_recovery_mm_xx_0.set_omega(self.sps/2.0)

	def set_config_filename(self, config_filename):
		self.config_filename = config_filename
		self._saved_pll_alpha_config = ConfigParser.ConfigParser()
		self._saved_pll_alpha_config.read(self.config_filename)
		if not self._saved_pll_alpha_config.has_section("satname"):
			self._saved_pll_alpha_config.add_section("satname")
		self._saved_pll_alpha_config.set("satname", 'pll_alpha', str(self.saved_pll_alpha))
		self._saved_pll_alpha_config.write(open(self.config_filename, 'w'))
		self._saved_gain_config = ConfigParser.ConfigParser()
		self._saved_gain_config.read(self.config_filename)
		if not self._saved_gain_config.has_section("satname"):
			self._saved_gain_config.add_section("satname")
		self._saved_gain_config.set("satname", 'gain', str(self.gain))
		self._saved_gain_config.write(open(self.config_filename, 'w'))
		self._saved_clock_alpha_config = ConfigParser.ConfigParser()
		self._saved_clock_alpha_config.read(self.config_filename)
		if not self._saved_clock_alpha_config.has_section("satname"):
			self._saved_clock_alpha_config.add_section("satname")
		self._saved_clock_alpha_config.set("satname", 'clock_alpha', str(self.saved_clock_alpha))
		self._saved_clock_alpha_config.write(open(self.config_filename, 'w'))

	def set_saved_pll_alpha(self, saved_pll_alpha):
		self.saved_pll_alpha = saved_pll_alpha
		self._saved_pll_alpha_config = ConfigParser.ConfigParser()
		self._saved_pll_alpha_config.read(self.config_filename)
		if not self._saved_pll_alpha_config.has_section("satname"):
			self._saved_pll_alpha_config.add_section("satname")
		self._saved_pll_alpha_config.set("satname", 'pll_alpha', str(self.saved_pll_alpha))
		self._saved_pll_alpha_config.write(open(self.config_filename, 'w'))
		self.pll.set_alpha(self.saved_pll_alpha)
		self.pll.set_beta(self.saved_pll_alpha**2/4.0)

	def set_saved_gain(self, saved_gain):
		self.saved_gain = saved_gain

	def set_saved_clock_alpha(self, saved_clock_alpha):
		self.saved_clock_alpha = saved_clock_alpha
		self._saved_clock_alpha_config = ConfigParser.ConfigParser()
		self._saved_clock_alpha_config.read(self.config_filename)
		if not self._saved_clock_alpha_config.has_section("satname"):
			self._saved_clock_alpha_config.add_section("satname")
		self._saved_clock_alpha_config.set("satname", 'clock_alpha', str(self.saved_clock_alpha))
		self._saved_clock_alpha_config.write(open(self.config_filename, 'w'))
		self.gr_clock_recovery_mm_xx_0.set_gain_omega(self.saved_clock_alpha**2/4.0)
		self.gr_clock_recovery_mm_xx_0.set_gain_mu(self.saved_clock_alpha)

	def set_max_clock_offset(self, max_clock_offset):
		self.max_clock_offset = max_clock_offset

	def set_max_carrier_offset(self, max_carrier_offset):
		self.max_carrier_offset = max_carrier_offset
		self.pll.set_max_offset(self.max_carrier_offset)

	def set_hs(self, hs):
		self.hs = hs
		self.gr_moving_average_xx_0.set_length_and_scale(self.hs, 1.0/self.hs)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	parser.add_option("-c", "--sync-check", dest="sync_check", type="intx", default=False,
		help="Set Sync check [default=%default]")
	parser.add_option("-g", "--gain", dest="gain", type="eng_float", default=eng_notation.num_to_str(35),
		help="Set Gain [default=%default]")
	parser.add_option("-R", "--side", dest="side", type="string", default="A",
		help="Set Side [default=%default]")
	parser.add_option("-f", "--freq", dest="freq", type="eng_float", default=eng_notation.num_to_str(1700.5e6),
		help="Set Frequency [default=%default]")
	parser.add_option("-d", "--decim", dest="decim", type="intx", default=16,
		help="Set Decimation [default=%default]")
	parser.add_option("-S", "--satellite", dest="satellite", type="string", default='FENGYUN-1D',
		help="Set Satellite [default=%default]")
	parser.add_option("-o", "--frames-file", dest="frames_file", type="string", default=os.environ['HOME'] + '/FENGYUN-1D.hrpt',
		help="Set Frames output filename [default=%default]")
	(options, args) = parser.parse_args()
	tb = usrp_rx_fy1_hrpt_nogui(sync_check=options.sync_check, gain=options.gain, side=options.side, freq=options.freq, decim=options.decim, satellite=options.satellite, frames_file=options.frames_file)
	tb.start()
	raw_input('Press Enter to quit: ')
	tb.stop()

