#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: USRP Meteor M N1 HRPT Receiver
# Author: POES Weather Ltd
# Description: Meteor M N1 HRPT Receiver
# Generated: Wed Dec 15 21:29:41 2010
##################################################

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import noaa
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import numbersink2
from grc_gnuradio import usrp as grc_usrp
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
from time import strftime, localtime
import ConfigParser
import math, os
import poesweather
import wx

class usrp_rx_mn1_bb_hrpt(grc_wxgui.top_block_gui):

	def __init__(self, side="A", gain=35, decim=32, sync_check=False, frames_file=os.environ['HOME'] + '/METEOR-M-1.hrpt', satellite='METEOR-M-1', baseband_file=os.environ['HOME'] + '/METEOR-M-1.dat', freq=1700e6):
		grc_wxgui.top_block_gui.__init__(self, title="USRP Meteor M N1 HRPT Receiver")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Parameters
		##################################################
		self.side = side
		self.gain = gain
		self.decim = decim
		self.sync_check = sync_check
		self.frames_file = frames_file
		self.satellite = satellite
		self.baseband_file = baseband_file
		self.freq = freq

		##################################################
		# Variables
		##################################################
		self.sym_rate = sym_rate = 600*1109
		self.samp_rate = samp_rate = 64e6/decim
		self.config_filename = config_filename = os.environ['HOME']+'/.gnuradio/mn1_hrpt.conf'
		self.sps = sps = samp_rate/sym_rate
		self._saved_pll_alpha_config = ConfigParser.ConfigParser()
		self._saved_pll_alpha_config.read(config_filename)
		try: saved_pll_alpha = self._saved_pll_alpha_config.getfloat("satname", 'pll_alpha')
		except: saved_pll_alpha = 0.005
		self.saved_pll_alpha = saved_pll_alpha
		self._saved_clock_alpha_config = ConfigParser.ConfigParser()
		self._saved_clock_alpha_config.read(config_filename)
		try: saved_clock_alpha = self._saved_clock_alpha_config.getfloat("satname", 'clock_alpha')
		except: saved_clock_alpha = 0.001
		self.saved_clock_alpha = saved_clock_alpha
		self.sync_check_txt = sync_check_txt = sync_check
		self.side_text = side_text = side
		self._saved_gain_config = ConfigParser.ConfigParser()
		self._saved_gain_config.read(config_filename)
		try: saved_gain = self._saved_gain_config.getfloat("satname", 'gain')
		except: saved_gain = gain
		self.saved_gain = saved_gain
		self.satellite_text = satellite_text = satellite
		self.sample_rate_text = sample_rate_text = samp_rate
		self.pll_alpha = pll_alpha = saved_pll_alpha
		self.max_clock_offset = max_clock_offset = 0.1
		self.max_carrier_offset = max_carrier_offset = 2*math.pi*100e3/samp_rate
		self.hs = hs = int(sps/2.0)
		self.gain_slider = gain_slider = gain
		self.freq_tb = freq_tb = freq
		self.frames_outfile_text = frames_outfile_text = frames_file
		self.decim_tb = decim_tb = decim
		self.datetime_text = datetime_text = strftime("%A, %B %d %Y %H:%M:%S", localtime())
		self.clock_alpha = clock_alpha = saved_clock_alpha
		self.baseband_outfile_text = baseband_outfile_text = baseband_file

		##################################################
		# Notebooks
		##################################################
		self.displays = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
		self.displays.AddPage(grc_wxgui.Panel(self.displays), "RX Meteor M N1 HRPT")
		self.displays.AddPage(grc_wxgui.Panel(self.displays), "Information")
		self.Add(self.displays)

		##################################################
		# Controls
		##################################################
		self._sync_check_txt_static_text = forms.static_text(
			parent=self.GetWin(),
			value=self.sync_check_txt,
			callback=self.set_sync_check_txt,
			label="Sync check",
			converter=forms.float_converter(),
		)
		self.GridAdd(self._sync_check_txt_static_text, 0, 2, 1, 1)
		self._side_text_static_text = forms.static_text(
			parent=self.GetWin(),
			value=self.side_text,
			callback=self.set_side_text,
			label="USRP Side",
			converter=forms.str_converter(),
		)
		self.GridAdd(self._side_text_static_text, 0, 0, 1, 1)
		self._satellite_text_static_text = forms.static_text(
			parent=self.GetWin(),
			value=self.satellite_text,
			callback=self.set_satellite_text,
			label="Satellite",
			converter=forms.str_converter(),
		)
		self.GridAdd(self._satellite_text_static_text, 0, 1, 1, 1)
		self._sample_rate_text_static_text = forms.static_text(
			parent=self.displays.GetPage(1).GetWin(),
			value=self.sample_rate_text,
			callback=self.set_sample_rate_text,
			label="Sample rate",
			converter=forms.float_converter(),
		)
		self.displays.GetPage(1).GridAdd(self._sample_rate_text_static_text, 3, 0, 1, 1)
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
			minimum=0.005,
			maximum=0.5,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_pll_alpha_sizer, 2, 1, 1, 1)
		_gain_slider_sizer = wx.BoxSizer(wx.VERTICAL)
		self._gain_slider_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_gain_slider_sizer,
			value=self.gain_slider,
			callback=self.set_gain_slider,
			label="Gain",
			converter=forms.int_converter(),
			proportion=0,
		)
		self._gain_slider_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_gain_slider_sizer,
			value=self.gain_slider,
			callback=self.set_gain_slider,
			minimum=0,
			maximum=100,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=int,
			proportion=1,
		)
		self.GridAdd(_gain_slider_sizer, 2, 0, 1, 1)
		self._freq_tb_text_box = forms.text_box(
			parent=self.GetWin(),
			value=self.freq_tb,
			callback=self.set_freq_tb,
			label="Frequency",
			converter=forms.float_converter(),
		)
		self.GridAdd(self._freq_tb_text_box, 1, 1, 1, 1)
		self._frames_outfile_text_static_text = forms.static_text(
			parent=self.displays.GetPage(1).GetWin(),
			value=self.frames_outfile_text,
			callback=self.set_frames_outfile_text,
			label="Frames filename",
			converter=forms.str_converter(),
		)
		self.displays.GetPage(1).GridAdd(self._frames_outfile_text_static_text, 5, 0, 1, 1)
		self._decim_tb_text_box = forms.text_box(
			parent=self.GetWin(),
			value=self.decim_tb,
			callback=self.set_decim_tb,
			label="Decimation",
			converter=forms.int_converter(),
		)
		self.GridAdd(self._decim_tb_text_box, 1, 0, 1, 1)
		self._datetime_text_static_text = forms.static_text(
			parent=self.displays.GetPage(1).GetWin(),
			value=self.datetime_text,
			callback=self.set_datetime_text,
			label="Acquisition start",
			converter=forms.str_converter(),
		)
		self.displays.GetPage(1).GridAdd(self._datetime_text_static_text, 2, 0, 1, 1)
		_clock_alpha_sizer = wx.BoxSizer(wx.VERTICAL)
		self._clock_alpha_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_clock_alpha_sizer,
			value=self.clock_alpha,
			callback=self.set_clock_alpha,
			label="Clock alpha",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._clock_alpha_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_clock_alpha_sizer,
			value=self.clock_alpha,
			callback=self.set_clock_alpha,
			minimum=0.001,
			maximum=0.1,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_clock_alpha_sizer, 2, 2, 1, 1)
		self._baseband_outfile_text_static_text = forms.static_text(
			parent=self.displays.GetPage(1).GetWin(),
			value=self.baseband_outfile_text,
			callback=self.set_baseband_outfile_text,
			label="Baseband filename",
			converter=forms.str_converter(),
		)
		self.displays.GetPage(1).GridAdd(self._baseband_outfile_text_static_text, 4, 0, 1, 1)

		##################################################
		# Blocks
		##################################################
		self.agc = gr.agc_cc(1e-5, 1.0, 1.0/32768.0, 1.0)
		self.gr_binary_slicer_fb_0 = gr.binary_slicer_fb()
		self.gr_clock_recovery_mm_xx_0 = gr.clock_recovery_mm_ff(sps/2.0, clock_alpha**2/4.0, 0.5, clock_alpha, max_clock_offset)
		self.gr_file_sink_0 = gr.file_sink(gr.sizeof_short*1, baseband_file)
		self.gr_file_sink_0.set_unbuffered(False)
		self.gr_file_sink_0_0 = gr.file_sink(gr.sizeof_short*1, "frames_outfile")
		self.gr_file_sink_0_0.set_unbuffered(False)
		self.gr_interleaved_short_to_complex_0 = gr.interleaved_short_to_complex()
		self.gr_moving_average_xx_0 = gr.moving_average_ff(hs, 1.0/hs, 4000)
		self.gr_rms_xx_0 = gr.rms_cf(0.2)
		self.pll = noaa.hrpt_pll_cf(pll_alpha, pll_alpha**2/4.0, max_carrier_offset)
		self.poesweather_mn1_hrpt_deframer_0 = poesweather.mn1_hrpt_deframer(sync_check)
		self.usrp_simple_source_x_0 = grc_usrp.simple_source_s(which=0, side=side, rx_ant="RXA")
		self.usrp_simple_source_x_0.set_decim_rate(decim)
		self.usrp_simple_source_x_0.set_frequency(freq, verbose=True)
		self.usrp_simple_source_x_0.set_gain(gain)
		self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
			self.displays.GetPage(0).GetWin(),
			baseband_freq=0,
			y_per_div=5,
			y_divs=10,
			ref_level=45,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=30,
			average=True,
			avg_alpha=0.1,
			title="Meteor M N1 HRPT FFT Spectrum",
			peak_hold=False,
		)
		self.displays.GetPage(0).Add(self.wxgui_fftsink2_0.win)
		self.wxgui_numbersink2_0 = numbersink2.number_sink_f(
			self.GetWin(),
			unit="Units",
			minval=0,
			maxval=5000,
			factor=1.0,
			decimal_places=4,
			ref_level=0,
			sample_rate=samp_rate,
			number_rate=15,
			average=True,
			avg_alpha=0.07,
			label="S-Meter",
			peak_hold=False,
			show_gauge=True,
		)
		self.Add(self.wxgui_numbersink2_0.win)

		##################################################
		# Connections
		##################################################
		self.connect((self.poesweather_mn1_hrpt_deframer_0, 0), (self.gr_file_sink_0_0, 0))
		self.connect((self.gr_binary_slicer_fb_0, 0), (self.poesweather_mn1_hrpt_deframer_0, 0))
		self.connect((self.usrp_simple_source_x_0, 0), (self.gr_interleaved_short_to_complex_0, 0))
		self.connect((self.gr_interleaved_short_to_complex_0, 0), (self.agc, 0))
		self.connect((self.gr_clock_recovery_mm_xx_0, 0), (self.gr_binary_slicer_fb_0, 0))
		self.connect((self.agc, 0), (self.pll, 0))
		self.connect((self.pll, 0), (self.gr_moving_average_xx_0, 0))
		self.connect((self.gr_moving_average_xx_0, 0), (self.gr_clock_recovery_mm_xx_0, 0))
		self.connect((self.gr_interleaved_short_to_complex_0, 0), (self.wxgui_fftsink2_0, 0))
		self.connect((self.gr_interleaved_short_to_complex_0, 0), (self.gr_rms_xx_0, 0))
		self.connect((self.usrp_simple_source_x_0, 0), (self.gr_file_sink_0, 0))
		self.connect((self.gr_rms_xx_0, 0), (self.wxgui_numbersink2_0, 0))

	def set_side(self, side):
		self.side = side
		self.set_side_text(self.side)

	def set_gain(self, gain):
		self.gain = gain
		self.set_saved_gain(self.gain)
		self._saved_gain_config = ConfigParser.ConfigParser()
		self._saved_gain_config.read(self.config_filename)
		if not self._saved_gain_config.has_section("satname"):
			self._saved_gain_config.add_section("satname")
		self._saved_gain_config.set("satname", 'gain', str(self.gain))
		self._saved_gain_config.write(open(self.config_filename, 'w'))
		self.set_gain_slider(self.gain)
		self.usrp_simple_source_x_0.set_gain(self.gain)

	def set_decim(self, decim):
		self.decim = decim
		self.set_samp_rate(64e6/self.decim)
		self.set_decim_tb(self.decim)
		self.usrp_simple_source_x_0.set_decim_rate(self.decim)

	def set_sync_check(self, sync_check):
		self.sync_check = sync_check
		self.set_sync_check_txt(self.sync_check)

	def set_frames_file(self, frames_file):
		self.frames_file = frames_file
		self.set_frames_outfile_text(self.frames_file)

	def set_satellite(self, satellite):
		self.satellite = satellite
		self.set_satellite_text(self.satellite)

	def set_baseband_file(self, baseband_file):
		self.baseband_file = baseband_file
		self.set_baseband_outfile_text(self.baseband_file)

	def set_freq(self, freq):
		self.freq = freq
		self.set_freq_tb(self.freq)
		self.usrp_simple_source_x_0.set_frequency(self.freq)

	def set_sym_rate(self, sym_rate):
		self.sym_rate = sym_rate
		self.set_sps(self.samp_rate/self.sym_rate)

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.set_sps(self.samp_rate/self.sym_rate)
		self.set_max_carrier_offset(2*math.pi*100e3/self.samp_rate)
		self.set_sample_rate_text(self.samp_rate)
		self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)

	def set_config_filename(self, config_filename):
		self.config_filename = config_filename
		self._saved_pll_alpha_config = ConfigParser.ConfigParser()
		self._saved_pll_alpha_config.read(self.config_filename)
		if not self._saved_pll_alpha_config.has_section("satname"):
			self._saved_pll_alpha_config.add_section("satname")
		self._saved_pll_alpha_config.set("satname", 'pll_alpha', str(self.pll_alpha))
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
		self._saved_clock_alpha_config.set("satname", 'clock_alpha', str(self.clock_alpha))
		self._saved_clock_alpha_config.write(open(self.config_filename, 'w'))

	def set_sps(self, sps):
		self.sps = sps
		self.set_hs(int(self.sps/2.0))
		self.gr_clock_recovery_mm_xx_0.set_omega(self.sps/2.0)

	def set_saved_pll_alpha(self, saved_pll_alpha):
		self.saved_pll_alpha = saved_pll_alpha
		self.set_pll_alpha(self.saved_pll_alpha)

	def set_saved_clock_alpha(self, saved_clock_alpha):
		self.saved_clock_alpha = saved_clock_alpha
		self.set_clock_alpha(self.saved_clock_alpha)

	def set_sync_check_txt(self, sync_check_txt):
		self.sync_check_txt = sync_check_txt
		self._sync_check_txt_static_text.set_value(self.sync_check_txt)

	def set_side_text(self, side_text):
		self.side_text = side_text
		self._side_text_static_text.set_value(self.side_text)

	def set_saved_gain(self, saved_gain):
		self.saved_gain = saved_gain

	def set_satellite_text(self, satellite_text):
		self.satellite_text = satellite_text
		self._satellite_text_static_text.set_value(self.satellite_text)

	def set_sample_rate_text(self, sample_rate_text):
		self.sample_rate_text = sample_rate_text
		self._sample_rate_text_static_text.set_value(self.sample_rate_text)

	def set_pll_alpha(self, pll_alpha):
		self.pll_alpha = pll_alpha
		self._pll_alpha_slider.set_value(self.pll_alpha)
		self._pll_alpha_text_box.set_value(self.pll_alpha)
		self._saved_pll_alpha_config = ConfigParser.ConfigParser()
		self._saved_pll_alpha_config.read(self.config_filename)
		if not self._saved_pll_alpha_config.has_section("satname"):
			self._saved_pll_alpha_config.add_section("satname")
		self._saved_pll_alpha_config.set("satname", 'pll_alpha', str(self.pll_alpha))
		self._saved_pll_alpha_config.write(open(self.config_filename, 'w'))
		self.pll.set_alpha(self.pll_alpha)
		self.pll.set_beta(self.pll_alpha**2/4.0)

	def set_max_clock_offset(self, max_clock_offset):
		self.max_clock_offset = max_clock_offset

	def set_max_carrier_offset(self, max_carrier_offset):
		self.max_carrier_offset = max_carrier_offset
		self.pll.set_max_offset(self.max_carrier_offset)

	def set_hs(self, hs):
		self.hs = hs
		self.gr_moving_average_xx_0.set_length_and_scale(self.hs, 1.0/self.hs)

	def set_gain_slider(self, gain_slider):
		self.gain_slider = gain_slider
		self._gain_slider_slider.set_value(self.gain_slider)
		self._gain_slider_text_box.set_value(self.gain_slider)

	def set_freq_tb(self, freq_tb):
		self.freq_tb = freq_tb
		self._freq_tb_text_box.set_value(self.freq_tb)

	def set_frames_outfile_text(self, frames_outfile_text):
		self.frames_outfile_text = frames_outfile_text
		self._frames_outfile_text_static_text.set_value(self.frames_outfile_text)

	def set_decim_tb(self, decim_tb):
		self.decim_tb = decim_tb
		self._decim_tb_text_box.set_value(self.decim_tb)

	def set_datetime_text(self, datetime_text):
		self.datetime_text = datetime_text
		self._datetime_text_static_text.set_value(self.datetime_text)

	def set_clock_alpha(self, clock_alpha):
		self.clock_alpha = clock_alpha
		self._saved_clock_alpha_config = ConfigParser.ConfigParser()
		self._saved_clock_alpha_config.read(self.config_filename)
		if not self._saved_clock_alpha_config.has_section("satname"):
			self._saved_clock_alpha_config.add_section("satname")
		self._saved_clock_alpha_config.set("satname", 'clock_alpha', str(self.clock_alpha))
		self._saved_clock_alpha_config.write(open(self.config_filename, 'w'))
		self._clock_alpha_slider.set_value(self.clock_alpha)
		self._clock_alpha_text_box.set_value(self.clock_alpha)
		self.gr_clock_recovery_mm_xx_0.set_gain_omega(self.clock_alpha**2/4.0)
		self.gr_clock_recovery_mm_xx_0.set_gain_mu(self.clock_alpha)

	def set_baseband_outfile_text(self, baseband_outfile_text):
		self.baseband_outfile_text = baseband_outfile_text
		self._baseband_outfile_text_static_text.set_value(self.baseband_outfile_text)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	parser.add_option("-R", "--side", dest="side", type="string", default="A",
		help="Set Side [default=%default]")
	parser.add_option("-g", "--gain", dest="gain", type="eng_float", default=eng_notation.num_to_str(35),
		help="Set Gain [default=%default]")
	parser.add_option("-d", "--decim", dest="decim", type="intx", default=32,
		help="Set Decimation [default=%default]")
	parser.add_option("-c", "--sync-check", dest="sync_check", type="intx", default=False,
		help="Set Sync check [default=%default]")
	parser.add_option("-o", "--frames-file", dest="frames_file", type="string", default=os.environ['HOME'] + '/METEOR-M-1.hrpt',
		help="Set Frames output filename [default=%default]")
	parser.add_option("-S", "--satellite", dest="satellite", type="string", default='METEOR-M-1',
		help="Set Satellite [default=%default]")
	parser.add_option("-F", "--baseband-file", dest="baseband_file", type="string", default=os.environ['HOME'] + '/METEOR-M-1.dat',
		help="Set Baseband output filename [default=%default]")
	parser.add_option("-f", "--freq", dest="freq", type="eng_float", default=eng_notation.num_to_str(1700e6),
		help="Set Frequency [default=%default]")
	(options, args) = parser.parse_args()
	tb = usrp_rx_mn1_bb_hrpt(side=options.side, gain=options.gain, decim=options.decim, sync_check=options.sync_check, frames_file=options.frames_file, satellite=options.satellite, baseband_file=options.baseband_file, freq=options.freq)
	tb.Run(True)

