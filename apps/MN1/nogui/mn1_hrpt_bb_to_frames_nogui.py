#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Meteor M N1 HRPT Baseband To Frames
# Author: POES Weather Ltd
# Description: Meteor M N1 HRPT Baseband To Frames
# Generated: Wed Dec 15 21:21:18 2010
##################################################

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import noaa
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from optparse import OptionParser
import ConfigParser
import math, os
import poesweather

class mn1_hrpt_bb_to_frames_nogui(gr.top_block):

	def __init__(self, decim=32, sync_check=False, satellite='METEOR-M-1', baseband_file=os.environ['HOME'] + '/METEOR-M-1.dat', frames_file=os.environ['HOME'] + '/METEOR-M-1.hrpt'):
		gr.top_block.__init__(self, "Meteor M N1 HRPT Baseband To Frames")

		##################################################
		# Parameters
		##################################################
		self.decim = decim
		self.sync_check = sync_check
		self.satellite = satellite
		self.baseband_file = baseband_file
		self.frames_file = frames_file

		##################################################
		# Variables
		##################################################
		self.sym_rate = sym_rate = 600*1109
		self.sample_rate = sample_rate = 64e6/decim
		self.sps = sps = sample_rate/sym_rate
		self.config_filename = config_filename = os.environ['HOME']+'/.gnuradio/mn1_hrpt.conf'
		self._saved_pll_alpha_config = ConfigParser.ConfigParser()
		self._saved_pll_alpha_config.read(config_filename)
		try: saved_pll_alpha = self._saved_pll_alpha_config.getfloat("satname", 'pll_alpha')
		except: saved_pll_alpha = 0.01
		self.saved_pll_alpha = saved_pll_alpha
		self._saved_clock_alpha_config = ConfigParser.ConfigParser()
		self._saved_clock_alpha_config.read(config_filename)
		try: saved_clock_alpha = self._saved_clock_alpha_config.getfloat("satname", 'clock_alpha')
		except: saved_clock_alpha = 0.01
		self.saved_clock_alpha = saved_clock_alpha
		self.max_clock_offset = max_clock_offset = 100e-6
		self.max_carrier_offset = max_carrier_offset = 2*math.pi*100e3/sample_rate
		self.hs = hs = int(sps/2.0)

		##################################################
		# Blocks
		##################################################
		self.agc = gr.agc_cc(1e-6, 1.0, 1.0, 1.0)
		self.frame_sink = gr.file_sink(gr.sizeof_short*1, frames_file)
		self.frame_sink.set_unbuffered(False)
		self.gr_binary_slicer_fb_0 = gr.binary_slicer_fb()
		self.gr_clock_recovery_mm_xx_0 = gr.clock_recovery_mm_ff(sps/2.0, saved_clock_alpha**2/4.0, 0.5, saved_clock_alpha, max_clock_offset)
		self.gr_file_source_0 = gr.file_source(gr.sizeof_short*1, baseband_file, False)
		self.gr_interleaved_short_to_complex_0 = gr.interleaved_short_to_complex()
		self.gr_moving_average_xx_0 = gr.moving_average_ff(hs, 1.0/hs, 4000)
		self.pll = noaa.hrpt_pll_cf(saved_pll_alpha, saved_pll_alpha**2/4.0, max_carrier_offset)
		self.poesweather_mn1_hrpt_deframer_0 = poesweather.mn1_hrpt_deframer(sync_check)
		self.throttle = gr.throttle(gr.sizeof_short*1, sample_rate*10)

		##################################################
		# Connections
		##################################################
		self.connect((self.gr_clock_recovery_mm_xx_0, 0), (self.gr_binary_slicer_fb_0, 0))
		self.connect((self.gr_file_source_0, 0), (self.throttle, 0))
		self.connect((self.throttle, 0), (self.gr_interleaved_short_to_complex_0, 0))
		self.connect((self.gr_interleaved_short_to_complex_0, 0), (self.agc, 0))
		self.connect((self.agc, 0), (self.pll, 0))
		self.connect((self.pll, 0), (self.gr_moving_average_xx_0, 0))
		self.connect((self.gr_moving_average_xx_0, 0), (self.gr_clock_recovery_mm_xx_0, 0))
		self.connect((self.gr_binary_slicer_fb_0, 0), (self.poesweather_mn1_hrpt_deframer_0, 0))
		self.connect((self.poesweather_mn1_hrpt_deframer_0, 0), (self.frame_sink, 0))

	def set_decim(self, decim):
		self.decim = decim
		self.set_sample_rate(64e6/self.decim)

	def set_sync_check(self, sync_check):
		self.sync_check = sync_check

	def set_satellite(self, satellite):
		self.satellite = satellite

	def set_baseband_file(self, baseband_file):
		self.baseband_file = baseband_file

	def set_frames_file(self, frames_file):
		self.frames_file = frames_file

	def set_sym_rate(self, sym_rate):
		self.sym_rate = sym_rate
		self.set_sps(self.sample_rate/self.sym_rate)

	def set_sample_rate(self, sample_rate):
		self.sample_rate = sample_rate
		self.set_max_carrier_offset(2*math.pi*100e3/self.sample_rate)
		self.set_sps(self.sample_rate/self.sym_rate)

	def set_sps(self, sps):
		self.sps = sps
		self.gr_clock_recovery_mm_xx_0.set_omega(self.sps/2.0)
		self.set_hs(int(self.sps/2.0))

	def set_config_filename(self, config_filename):
		self.config_filename = config_filename
		self._saved_clock_alpha_config = ConfigParser.ConfigParser()
		self._saved_clock_alpha_config.read(self.config_filename)
		if not self._saved_clock_alpha_config.has_section("satname"):
			self._saved_clock_alpha_config.add_section("satname")
		self._saved_clock_alpha_config.set("satname", 'clock_alpha', str(self.saved_clock_alpha))
		self._saved_clock_alpha_config.write(open(self.config_filename, 'w'))
		self._saved_pll_alpha_config = ConfigParser.ConfigParser()
		self._saved_pll_alpha_config.read(self.config_filename)
		if not self._saved_pll_alpha_config.has_section("satname"):
			self._saved_pll_alpha_config.add_section("satname")
		self._saved_pll_alpha_config.set("satname", 'pll_alpha', str(self.saved_pll_alpha))
		self._saved_pll_alpha_config.write(open(self.config_filename, 'w'))

	def set_saved_pll_alpha(self, saved_pll_alpha):
		self.saved_pll_alpha = saved_pll_alpha
		self.pll.set_alpha(self.saved_pll_alpha)
		self.pll.set_beta(self.saved_pll_alpha**2/4.0)
		self._saved_pll_alpha_config = ConfigParser.ConfigParser()
		self._saved_pll_alpha_config.read(self.config_filename)
		if not self._saved_pll_alpha_config.has_section("satname"):
			self._saved_pll_alpha_config.add_section("satname")
		self._saved_pll_alpha_config.set("satname", 'pll_alpha', str(self.saved_pll_alpha))
		self._saved_pll_alpha_config.write(open(self.config_filename, 'w'))

	def set_saved_clock_alpha(self, saved_clock_alpha):
		self.saved_clock_alpha = saved_clock_alpha
		self.gr_clock_recovery_mm_xx_0.set_gain_omega(self.saved_clock_alpha**2/4.0)
		self.gr_clock_recovery_mm_xx_0.set_gain_mu(self.saved_clock_alpha)
		self._saved_clock_alpha_config = ConfigParser.ConfigParser()
		self._saved_clock_alpha_config.read(self.config_filename)
		if not self._saved_clock_alpha_config.has_section("satname"):
			self._saved_clock_alpha_config.add_section("satname")
		self._saved_clock_alpha_config.set("satname", 'clock_alpha', str(self.saved_clock_alpha))
		self._saved_clock_alpha_config.write(open(self.config_filename, 'w'))

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
	parser.add_option("-d", "--decim", dest="decim", type="intx", default=32,
		help="Set Decimation [default=%default]")
	parser.add_option("-c", "--sync-check", dest="sync_check", type="intx", default=False,
		help="Set Sync check [default=%default]")
	parser.add_option("-S", "--satellite", dest="satellite", type="string", default='METEOR-M-1',
		help="Set Satellite [default=%default]")
	parser.add_option("-F", "--baseband-file", dest="baseband_file", type="string", default=os.environ['HOME'] + '/METEOR-M-1.dat',
		help="Set Baseband input filename [default=%default]")
	parser.add_option("-o", "--frames-file", dest="frames_file", type="string", default=os.environ['HOME'] + '/METEOR-M-1.hrpt',
		help="Set Frames output filename [default=%default]")
	(options, args) = parser.parse_args()
	tb = mn1_hrpt_bb_to_frames_nogui(decim=options.decim, sync_check=options.sync_check, satellite=options.satellite, baseband_file=options.baseband_file, frames_file=options.frames_file)
	tb.run()

