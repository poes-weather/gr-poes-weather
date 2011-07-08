#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Meteor M N1 HRPT Baseband To Frames
# Author: POES Weather Ltd
# Description: Meteor M N1 HRPT Baseband To Frames
# Generated: Fri Jul  8 13:53:45 2011
##################################################

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import noaa
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import ConfigParser
import math, os
import poesweather
import wx

class mn1_hrpt_bb_to_frames(grc_wxgui.top_block_gui):

	def __init__(self, decim=32, sync_check=False, frames_file=os.environ['HOME'] + '/METEOR-M-1.hrpt', satellite='METEOR-M-1', baseband_file=os.environ['HOME'] + '/data/2011-05-25T215242-METEOR-M-1.dat'):
		grc_wxgui.top_block_gui.__init__(self, title="Meteor M N1 HRPT Baseband To Frames")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Parameters
		##################################################
		self.decim = decim
		self.sync_check = sync_check
		self.frames_file = frames_file
		self.satellite = satellite
		self.baseband_file = baseband_file

		##################################################
		# Variables
		##################################################
		self.sym_rate = sym_rate = 600*1109
		self.sample_rate = sample_rate = 64e6/decim
		self.config_filename = config_filename = os.environ['HOME']+'/.gnuradio/mn1_hrpt.conf'
		self.sps = sps = sample_rate/sym_rate
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
		self.sync_check_txt = sync_check_txt = sync_check
		self.satname_txt = satname_txt = satellite
		self.pll_alpha = pll_alpha = saved_pll_alpha
		self.max_clock_offset = max_clock_offset = 100e-6
		self.max_carrier_offset = max_carrier_offset = 2*math.pi*100e3/sample_rate
		self.hs = hs = int(sps/2.0)
		self.frames_file_txt = frames_file_txt = frames_file
		self.decim_txt = decim_txt = decim
		self.clock_alpha = clock_alpha = saved_clock_alpha
		self.baseband_file_txt = baseband_file_txt = baseband_file

		##################################################
		# Blocks
		##################################################
		self.displays = self.displays = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
		self.displays.AddPage(grc_wxgui.Panel(self.displays), "Meteor M N1 HRPT Spectrum")
		self.displays.AddPage(grc_wxgui.Panel(self.displays), "Information")
		self.Add(self.displays)
		_clock_alpha_sizer = wx.BoxSizer(wx.VERTICAL)
		self._clock_alpha_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_clock_alpha_sizer,
			value=self.clock_alpha,
			callback=self.set_clock_alpha,
			label="Clock Alpha",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._clock_alpha_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_clock_alpha_sizer,
			value=self.clock_alpha,
			callback=self.set_clock_alpha,
			minimum=0.0,
			maximum=0.5,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_clock_alpha_sizer, 1, 1, 1, 1)
		self.throttle = gr.throttle(gr.sizeof_short*1, sample_rate*2)
		self._sync_check_txt_static_text = forms.static_text(
			parent=self.GetWin(),
			value=self.sync_check_txt,
			callback=self.set_sync_check_txt,
			label="Sync check",
			converter=forms.int_converter(),
		)
		self.GridAdd(self._sync_check_txt_static_text, 0, 3, 1, 1)
		self._satname_txt_static_text = forms.static_text(
			parent=self.GetWin(),
			value=self.satname_txt,
			callback=self.set_satname_txt,
			label="Satellite",
			converter=forms.str_converter(),
		)
		self.GridAdd(self._satname_txt_static_text, 0, 0, 1, 1)
		self.rx_fft = fftsink2.fft_sink_c(
			self.displays.GetPage(0).GetWin(),
			baseband_freq=0,
			y_per_div=5,
			y_divs=10,
			ref_level=25,
			ref_scale=2.0,
			sample_rate=sample_rate,
			fft_size=1024,
			fft_rate=30,
			average=True,
			avg_alpha=0.1,
			title="Meteor M N1 HRPT Spectrum",
			peak_hold=False,
		)
		self.displays.GetPage(0).Add(self.rx_fft.win)
		self.poesweather_mn1_hrpt_deframer_0 = poesweather.mn1_hrpt_deframer(sync_check)
		_pll_alpha_sizer = wx.BoxSizer(wx.VERTICAL)
		self._pll_alpha_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_pll_alpha_sizer,
			value=self.pll_alpha,
			callback=self.set_pll_alpha,
			label="PLL Alpha",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._pll_alpha_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_pll_alpha_sizer,
			value=self.pll_alpha,
			callback=self.set_pll_alpha,
			minimum=0.0,
			maximum=0.5,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_pll_alpha_sizer, 1, 0, 1, 1)
		self.pll = noaa.hrpt_pll_cf(pll_alpha, pll_alpha**2/4.0, max_carrier_offset)
		self.gr_moving_average_xx_0 = gr.moving_average_ff(hs, 1.0/hs, 4000)
		self.gr_interleaved_short_to_complex_0 = gr.interleaved_short_to_complex()
		self.gr_file_source_0 = gr.file_source(gr.sizeof_short*1, baseband_file, False)
		self.gr_clock_recovery_mm_xx_0 = gr.clock_recovery_mm_ff(sps/2.0, clock_alpha**2/4.0, 0.5, clock_alpha, max_clock_offset)
		self.gr_binary_slicer_fb_0 = gr.binary_slicer_fb()
		self._frames_file_txt_static_text = forms.static_text(
			parent=self.displays.GetPage(1).GetWin(),
			value=self.frames_file_txt,
			callback=self.set_frames_file_txt,
			label="Frames output filename",
			converter=forms.str_converter(),
		)
		self.displays.GetPage(1).GridAdd(self._frames_file_txt_static_text, 2, 0, 1, 1)
		self.frame_sink = gr.file_sink(gr.sizeof_short*1, frames_file)
		self.frame_sink.set_unbuffered(False)
		self._decim_txt_static_text = forms.static_text(
			parent=self.GetWin(),
			value=self.decim_txt,
			callback=self.set_decim_txt,
			label="Decimation",
			converter=forms.str_converter(),
		)
		self.GridAdd(self._decim_txt_static_text, 0, 1, 1, 1)
		self._baseband_file_txt_static_text = forms.static_text(
			parent=self.displays.GetPage(1).GetWin(),
			value=self.baseband_file_txt,
			callback=self.set_baseband_file_txt,
			label="Baseband filename",
			converter=forms.str_converter(),
		)
		self.displays.GetPage(1).GridAdd(self._baseband_file_txt_static_text, 1, 0, 1, 1)
		self.agc = gr.agc_cc(1e-6, 1.0, 1.0, 1.0)

		##################################################
		# Connections
		##################################################
		self.connect((self.gr_interleaved_short_to_complex_0, 0), (self.agc, 0))
		self.connect((self.throttle, 0), (self.gr_interleaved_short_to_complex_0, 0))
		self.connect((self.gr_file_source_0, 0), (self.throttle, 0))
		self.connect((self.agc, 0), (self.rx_fft, 0))
		self.connect((self.agc, 0), (self.pll, 0))
		self.connect((self.pll, 0), (self.gr_moving_average_xx_0, 0))
		self.connect((self.gr_moving_average_xx_0, 0), (self.gr_clock_recovery_mm_xx_0, 0))
		self.connect((self.gr_binary_slicer_fb_0, 0), (self.poesweather_mn1_hrpt_deframer_0, 0))
		self.connect((self.poesweather_mn1_hrpt_deframer_0, 0), (self.frame_sink, 0))
		self.connect((self.gr_clock_recovery_mm_xx_0, 0), (self.gr_binary_slicer_fb_0, 0))

	def get_decim(self):
		return self.decim

	def set_decim(self, decim):
		self.decim = decim
		self.set_sample_rate(64e6/self.decim)
		self.set_decim_txt(self.decim)

	def get_sync_check(self):
		return self.sync_check

	def set_sync_check(self, sync_check):
		self.sync_check = sync_check
		self.set_sync_check_txt(self.sync_check)

	def get_frames_file(self):
		return self.frames_file

	def set_frames_file(self, frames_file):
		self.frames_file = frames_file
		self.set_frames_file_txt(self.frames_file)

	def get_satellite(self):
		return self.satellite

	def set_satellite(self, satellite):
		self.satellite = satellite
		self.set_satname_txt(self.satellite)

	def get_baseband_file(self):
		return self.baseband_file

	def set_baseband_file(self, baseband_file):
		self.baseband_file = baseband_file
		self.set_baseband_file_txt(self.baseband_file)

	def get_sym_rate(self):
		return self.sym_rate

	def set_sym_rate(self, sym_rate):
		self.sym_rate = sym_rate
		self.set_sps(self.sample_rate/self.sym_rate)

	def get_sample_rate(self):
		return self.sample_rate

	def set_sample_rate(self, sample_rate):
		self.sample_rate = sample_rate
		self.set_sps(self.sample_rate/self.sym_rate)
		self.set_max_carrier_offset(2*math.pi*100e3/self.sample_rate)
		self.rx_fft.set_sample_rate(self.sample_rate)

	def get_config_filename(self):
		return self.config_filename

	def set_config_filename(self, config_filename):
		self.config_filename = config_filename
		self._saved_pll_alpha_config = ConfigParser.ConfigParser()
		self._saved_pll_alpha_config.read(self.config_filename)
		if not self._saved_pll_alpha_config.has_section("satname"):
			self._saved_pll_alpha_config.add_section("satname")
		self._saved_pll_alpha_config.set("satname", 'pll_alpha', str(self.pll_alpha))
		self._saved_pll_alpha_config.write(open(self.config_filename, 'w'))
		self._saved_clock_alpha_config = ConfigParser.ConfigParser()
		self._saved_clock_alpha_config.read(self.config_filename)
		if not self._saved_clock_alpha_config.has_section("satname"):
			self._saved_clock_alpha_config.add_section("satname")
		self._saved_clock_alpha_config.set("satname", 'clock_alpha', str(self.clock_alpha))
		self._saved_clock_alpha_config.write(open(self.config_filename, 'w'))

	def get_sps(self):
		return self.sps

	def set_sps(self, sps):
		self.sps = sps
		self.set_hs(int(self.sps/2.0))
		self.gr_clock_recovery_mm_xx_0.set_omega(self.sps/2.0)

	def get_saved_pll_alpha(self):
		return self.saved_pll_alpha

	def set_saved_pll_alpha(self, saved_pll_alpha):
		self.saved_pll_alpha = saved_pll_alpha
		self.set_pll_alpha(self.saved_pll_alpha)

	def get_saved_clock_alpha(self):
		return self.saved_clock_alpha

	def set_saved_clock_alpha(self, saved_clock_alpha):
		self.saved_clock_alpha = saved_clock_alpha
		self.set_clock_alpha(self.saved_clock_alpha)

	def get_sync_check_txt(self):
		return self.sync_check_txt

	def set_sync_check_txt(self, sync_check_txt):
		self.sync_check_txt = sync_check_txt
		self._sync_check_txt_static_text.set_value(self.sync_check_txt)

	def get_satname_txt(self):
		return self.satname_txt

	def set_satname_txt(self, satname_txt):
		self.satname_txt = satname_txt
		self._satname_txt_static_text.set_value(self.satname_txt)

	def get_pll_alpha(self):
		return self.pll_alpha

	def set_pll_alpha(self, pll_alpha):
		self.pll_alpha = pll_alpha
		self._saved_pll_alpha_config = ConfigParser.ConfigParser()
		self._saved_pll_alpha_config.read(self.config_filename)
		if not self._saved_pll_alpha_config.has_section("satname"):
			self._saved_pll_alpha_config.add_section("satname")
		self._saved_pll_alpha_config.set("satname", 'pll_alpha', str(self.pll_alpha))
		self._saved_pll_alpha_config.write(open(self.config_filename, 'w'))
		self.pll.set_alpha(self.pll_alpha)
		self.pll.set_beta(self.pll_alpha**2/4.0)
		self._pll_alpha_slider.set_value(self.pll_alpha)
		self._pll_alpha_text_box.set_value(self.pll_alpha)

	def get_max_clock_offset(self):
		return self.max_clock_offset

	def set_max_clock_offset(self, max_clock_offset):
		self.max_clock_offset = max_clock_offset

	def get_max_carrier_offset(self):
		return self.max_carrier_offset

	def set_max_carrier_offset(self, max_carrier_offset):
		self.max_carrier_offset = max_carrier_offset
		self.pll.set_max_offset(self.max_carrier_offset)

	def get_hs(self):
		return self.hs

	def set_hs(self, hs):
		self.hs = hs
		self.gr_moving_average_xx_0.set_length_and_scale(self.hs, 1.0/self.hs)

	def get_frames_file_txt(self):
		return self.frames_file_txt

	def set_frames_file_txt(self, frames_file_txt):
		self.frames_file_txt = frames_file_txt
		self._frames_file_txt_static_text.set_value(self.frames_file_txt)

	def get_decim_txt(self):
		return self.decim_txt

	def set_decim_txt(self, decim_txt):
		self.decim_txt = decim_txt
		self._decim_txt_static_text.set_value(self.decim_txt)

	def get_clock_alpha(self):
		return self.clock_alpha

	def set_clock_alpha(self, clock_alpha):
		self.clock_alpha = clock_alpha
		self._saved_clock_alpha_config = ConfigParser.ConfigParser()
		self._saved_clock_alpha_config.read(self.config_filename)
		if not self._saved_clock_alpha_config.has_section("satname"):
			self._saved_clock_alpha_config.add_section("satname")
		self._saved_clock_alpha_config.set("satname", 'clock_alpha', str(self.clock_alpha))
		self._saved_clock_alpha_config.write(open(self.config_filename, 'w'))
		self.gr_clock_recovery_mm_xx_0.set_gain_omega(self.clock_alpha**2/4.0)
		self.gr_clock_recovery_mm_xx_0.set_gain_mu(self.clock_alpha)
		self._clock_alpha_slider.set_value(self.clock_alpha)
		self._clock_alpha_text_box.set_value(self.clock_alpha)

	def get_baseband_file_txt(self):
		return self.baseband_file_txt

	def set_baseband_file_txt(self, baseband_file_txt):
		self.baseband_file_txt = baseband_file_txt
		self._baseband_file_txt_static_text.set_value(self.baseband_file_txt)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	parser.add_option("-d", "--decim", dest="decim", type="intx", default=32,
		help="Set Decimation [default=%default]")
	parser.add_option("-c", "--sync-check", dest="sync_check", type="intx", default=False,
		help="Set Sync check [default=%default]")
	parser.add_option("-o", "--frames-file", dest="frames_file", type="string", default=os.environ['HOME'] + '/METEOR-M-1.hrpt',
		help="Set Frames output filename [default=%default]")
	parser.add_option("-S", "--satellite", dest="satellite", type="string", default='METEOR-M-1',
		help="Set Satellite [default=%default]")
	parser.add_option("-F", "--baseband-file", dest="baseband_file", type="string", default=os.environ['HOME'] + '/data/2011-05-25T215242-METEOR-M-1.dat',
		help="Set Baseband input filename [default=%default]")
	(options, args) = parser.parse_args()
	tb = mn1_hrpt_bb_to_frames(decim=options.decim, sync_check=options.sync_check, frames_file=options.frames_file, satellite=options.satellite, baseband_file=options.baseband_file)
	tb.Run(True)

