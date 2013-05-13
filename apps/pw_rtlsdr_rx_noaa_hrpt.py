#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Enhanced NOAA HRPT Receiver using USB DVB-T Dongles
# Author: POES Weather Ab Ltd & Martin Blaho
# Description: Enhanced NOAA HRPT Receiver
# Generated: Tue May 14 01:51:50 2013
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
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
from time import strftime, localtime
import ConfigParser
import math, os
import osmosdr
import poesweather
import wx

class pw_rtlsdr_rx_noaa_hrpt(grc_wxgui.top_block_gui):

	def __init__(self, freq=1698e6, rate=2e6, frames_file=os.environ['HOME'] + '/data/noaa/frames/NOAA-XX.hrpt', rtlsdr="rtl=0", ifgain=20, satellite='NOAA-XX', sync_check=False, rfgain=40):
		grc_wxgui.top_block_gui.__init__(self, title="Enhanced NOAA HRPT Receiver using USB DVB-T Dongles")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Parameters
		##################################################
		self.freq = freq
		self.rate = rate
		self.frames_file = frames_file
		self.rtlsdr = rtlsdr
		self.ifgain = ifgain
		self.satellite = satellite
		self.sync_check = sync_check
		self.rfgain = rfgain

		##################################################
		# Variables
		##################################################
		self.sym_rate = sym_rate = 600*1109
		self.samp_rate = samp_rate = rate
		self.config_filename = config_filename = os.environ['HOME']+'/.gnuradio/rtlsdr_noaa_hrpt.conf'
		self.sps = sps = samp_rate/sym_rate
		self._saved_pll_alpha_config = ConfigParser.ConfigParser()
		self._saved_pll_alpha_config.read(config_filename)
		try: saved_pll_alpha = self._saved_pll_alpha_config.getfloat(satellite, 'pll_alpha')
		except: saved_pll_alpha = 0.005
		self.saved_pll_alpha = saved_pll_alpha
		self._saved_clock_alpha_config = ConfigParser.ConfigParser()
		self._saved_clock_alpha_config.read(config_filename)
		try: saved_clock_alpha = self._saved_clock_alpha_config.getfloat(satellite, 'clock_alpha')
		except: saved_clock_alpha = 0.001
		self.saved_clock_alpha = saved_clock_alpha
		self.sync_check_cb = sync_check_cb = sync_check
		self._saved_rf_gain_config = ConfigParser.ConfigParser()
		self._saved_rf_gain_config.read(config_filename)
		try: saved_rf_gain = self._saved_rf_gain_config.getfloat(satellite, 'rf-gain')
		except: saved_rf_gain = rfgain
		self.saved_rf_gain = saved_rf_gain
		self._saved_if_gain_config = ConfigParser.ConfigParser()
		self._saved_if_gain_config.read(config_filename)
		try: saved_if_gain = self._saved_if_gain_config.getfloat(satellite, 'if-gain')
		except: saved_if_gain = ifgain
		self.saved_if_gain = saved_if_gain
		self.satellite_text = satellite_text = satellite
		self.sample_rate_text = sample_rate_text = samp_rate
		self.rf_gain_slider = rf_gain_slider = rfgain
		self.rate_tb = rate_tb = rate
		self.pll_alpha = pll_alpha = saved_pll_alpha
		self.max_clock_offset = max_clock_offset = 0.1
		self.max_carrier_offset = max_carrier_offset = 2*math.pi*100e3/samp_rate
		self.if_gain_slider = if_gain_slider = ifgain
		self.hs = hs = int(sps/2.0)
		self.freq_tb = freq_tb = freq
		self.frames_outfile_text = frames_outfile_text = frames_file
		self.datetime_text = datetime_text = strftime("%A, %B %d %Y %H:%M:%S", localtime())
		self.clock_alpha = clock_alpha = saved_clock_alpha

		##################################################
		# Blocks
		##################################################
		_rf_gain_slider_sizer = wx.BoxSizer(wx.VERTICAL)
		self._rf_gain_slider_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_rf_gain_slider_sizer,
			value=self.rf_gain_slider,
			callback=self.set_rf_gain_slider,
			label="RF Gain",
			converter=forms.int_converter(),
			proportion=0,
		)
		self._rf_gain_slider_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_rf_gain_slider_sizer,
			value=self.rf_gain_slider,
			callback=self.set_rf_gain_slider,
			minimum=0,
			maximum=100,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=int,
			proportion=1,
		)
		self.GridAdd(_rf_gain_slider_sizer, 2, 0, 1, 1)
		_if_gain_slider_sizer = wx.BoxSizer(wx.VERTICAL)
		self._if_gain_slider_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_if_gain_slider_sizer,
			value=self.if_gain_slider,
			callback=self.set_if_gain_slider,
			label="IF Gain",
			converter=forms.int_converter(),
			proportion=0,
		)
		self._if_gain_slider_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_if_gain_slider_sizer,
			value=self.if_gain_slider,
			callback=self.set_if_gain_slider,
			minimum=0,
			maximum=100,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=int,
			proportion=1,
		)
		self.GridAdd(_if_gain_slider_sizer, 2, 1, 1, 1)
		self.displays = self.displays = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
		self.displays.AddPage(grc_wxgui.Panel(self.displays), "RX NOAA HRPT")
		self.displays.AddPage(grc_wxgui.Panel(self.displays), "Information")
		self.Add(self.displays)
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
		self.GridAdd(_clock_alpha_sizer, 2, 3, 1, 1)
		self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
			self.displays.GetPage(0).GetWin(),
			baseband_freq=0,
			y_per_div=5,
			y_divs=10,
			ref_level=-30,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=512,
			fft_rate=5,
			average=True,
			avg_alpha=0.4,
			title="NOAA HRPT FFT Spectrum",
			peak_hold=False,
		)
		self.displays.GetPage(0).Add(self.wxgui_fftsink2_0.win)
		self._sync_check_cb_check_box = forms.check_box(
			parent=self.GetWin(),
			value=self.sync_check_cb,
			callback=self.set_sync_check_cb,
			label="Continuous sync check",
			true=True,
			false=False,
		)
		self.GridAdd(self._sync_check_cb_check_box, 1, 2, 1, 1)
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
		self._rate_tb_text_box = forms.text_box(
			parent=self.GetWin(),
			value=self.rate_tb,
			callback=self.set_rate_tb,
			label="Sample rate",
			converter=forms.float_converter(),
		)
		self.GridAdd(self._rate_tb_text_box, 1, 0, 1, 1)
		self.poesweather_noaa_hrpt_deframer_0 = poesweather.noaa_hrpt_deframer(False)
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
		self.GridAdd(_pll_alpha_sizer, 2, 2, 1, 1)
		self.pll = noaa.hrpt_pll_cf(pll_alpha, pll_alpha**2/4.0, max_carrier_offset)
		self.osmosdr_source_c_0 = osmosdr.source_c( args="nchan=" + str(1) + " " + rtlsdr )
		self.osmosdr_source_c_0.set_sample_rate(samp_rate)
		self.osmosdr_source_c_0.set_center_freq(freq, 0)
		self.osmosdr_source_c_0.set_freq_corr(0, 0)
		self.osmosdr_source_c_0.set_iq_balance_mode(0, 0)
		self.osmosdr_source_c_0.set_gain_mode(0, 0)
		self.osmosdr_source_c_0.set_gain(rf_gain_slider, 0)
		self.osmosdr_source_c_0.set_if_gain(if_gain_slider, 0)
			
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
		self.displays.GetPage(1).GridAdd(self._frames_outfile_text_static_text, 4, 0, 1, 1)
		self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(sps/2.0, clock_alpha**2/4.0, 0.5, clock_alpha, max_clock_offset)
		self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
		self._datetime_text_static_text = forms.static_text(
			parent=self.displays.GetPage(1).GetWin(),
			value=self.datetime_text,
			callback=self.set_datetime_text,
			label="Acquisition start",
			converter=forms.str_converter(),
		)
		self.displays.GetPage(1).GridAdd(self._datetime_text_static_text, 2, 0, 1, 1)
		self.blocks_moving_average_xx_0 = blocks.moving_average_ff(hs, 1.0/hs, 4000)
		self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_short*1, frames_file)
		self.blocks_file_sink_0.set_unbuffered(False)
		self.analog_agc_xx_0 = analog.agc_cc(1e-5, 1.0, 1.0/32768.0, 1.0)

		##################################################
		# Connections
		##################################################
		self.connect((self.analog_agc_xx_0, 0), (self.pll, 0))
		self.connect((self.pll, 0), (self.blocks_moving_average_xx_0, 0))
		self.connect((self.blocks_moving_average_xx_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))
		self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
		self.connect((self.poesweather_noaa_hrpt_deframer_0, 0), (self.blocks_file_sink_0, 0))
		self.connect((self.digital_binary_slicer_fb_0, 0), (self.poesweather_noaa_hrpt_deframer_0, 0))
		self.connect((self.osmosdr_source_c_0, 0), (self.wxgui_fftsink2_0, 0))
		self.connect((self.osmosdr_source_c_0, 0), (self.analog_agc_xx_0, 0))


	def get_freq(self):
		return self.freq

	def set_freq(self, freq):
		self.freq = freq
		self.set_freq_tb(self.freq)
		self.osmosdr_source_c_0.set_center_freq(self.freq, 0)

	def get_rate(self):
		return self.rate

	def set_rate(self, rate):
		self.rate = rate
		self.set_samp_rate(self.rate)
		self.set_rate_tb(self.rate)

	def get_frames_file(self):
		return self.frames_file

	def set_frames_file(self, frames_file):
		self.frames_file = frames_file
		self.set_frames_outfile_text(self.frames_file)
		self.blocks_file_sink_0.open(self.frames_file)

	def get_rtlsdr(self):
		return self.rtlsdr

	def set_rtlsdr(self, rtlsdr):
		self.rtlsdr = rtlsdr

	def get_ifgain(self):
		return self.ifgain

	def set_ifgain(self, ifgain):
		self.ifgain = ifgain
		self.set_saved_if_gain(self.ifgain)
		self.set_if_gain_slider(self.ifgain)

	def get_satellite(self):
		return self.satellite

	def set_satellite(self, satellite):
		self.satellite = satellite
		self.set_satellite_text(self.satellite)
		self._saved_pll_alpha_config = ConfigParser.ConfigParser()
		self._saved_pll_alpha_config.read(self.config_filename)
		if not self._saved_pll_alpha_config.has_section(self.satellite):
			self._saved_pll_alpha_config.add_section(self.satellite)
		self._saved_pll_alpha_config.set(self.satellite, 'pll_alpha', str(self.pll_alpha))
		self._saved_pll_alpha_config.write(open(self.config_filename, 'w'))
		self._saved_if_gain_config = ConfigParser.ConfigParser()
		self._saved_if_gain_config.read(self.config_filename)
		if not self._saved_if_gain_config.has_section(self.satellite):
			self._saved_if_gain_config.add_section(self.satellite)
		self._saved_if_gain_config.set(self.satellite, 'if-gain', str(self.if_gain_slider))
		self._saved_if_gain_config.write(open(self.config_filename, 'w'))
		self._saved_rf_gain_config = ConfigParser.ConfigParser()
		self._saved_rf_gain_config.read(self.config_filename)
		if not self._saved_rf_gain_config.has_section(self.satellite):
			self._saved_rf_gain_config.add_section(self.satellite)
		self._saved_rf_gain_config.set(self.satellite, 'rf-gain', str(self.rf_gain_slider))
		self._saved_rf_gain_config.write(open(self.config_filename, 'w'))
		self._saved_clock_alpha_config = ConfigParser.ConfigParser()
		self._saved_clock_alpha_config.read(self.config_filename)
		if not self._saved_clock_alpha_config.has_section(self.satellite):
			self._saved_clock_alpha_config.add_section(self.satellite)
		self._saved_clock_alpha_config.set(self.satellite, 'clock_alpha', str(self.clock_alpha))
		self._saved_clock_alpha_config.write(open(self.config_filename, 'w'))

	def get_sync_check(self):
		return self.sync_check

	def set_sync_check(self, sync_check):
		self.sync_check = sync_check
		self.set_sync_check_cb(self.sync_check)

	def get_rfgain(self):
		return self.rfgain

	def set_rfgain(self, rfgain):
		self.rfgain = rfgain
		self.set_saved_rf_gain(self.rfgain)
		self.set_rf_gain_slider(self.rfgain)

	def get_sym_rate(self):
		return self.sym_rate

	def set_sym_rate(self, sym_rate):
		self.sym_rate = sym_rate
		self.set_sps(self.samp_rate/self.sym_rate)

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.set_sps(self.samp_rate/self.sym_rate)
		self.set_max_carrier_offset(2*math.pi*100e3/self.samp_rate)
		self.set_sample_rate_text(self.samp_rate)
		self.osmosdr_source_c_0.set_sample_rate(self.samp_rate)
		self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)

	def get_config_filename(self):
		return self.config_filename

	def set_config_filename(self, config_filename):
		self.config_filename = config_filename
		self._saved_pll_alpha_config = ConfigParser.ConfigParser()
		self._saved_pll_alpha_config.read(self.config_filename)
		if not self._saved_pll_alpha_config.has_section(self.satellite):
			self._saved_pll_alpha_config.add_section(self.satellite)
		self._saved_pll_alpha_config.set(self.satellite, 'pll_alpha', str(self.pll_alpha))
		self._saved_pll_alpha_config.write(open(self.config_filename, 'w'))
		self._saved_if_gain_config = ConfigParser.ConfigParser()
		self._saved_if_gain_config.read(self.config_filename)
		if not self._saved_if_gain_config.has_section(self.satellite):
			self._saved_if_gain_config.add_section(self.satellite)
		self._saved_if_gain_config.set(self.satellite, 'if-gain', str(self.if_gain_slider))
		self._saved_if_gain_config.write(open(self.config_filename, 'w'))
		self._saved_rf_gain_config = ConfigParser.ConfigParser()
		self._saved_rf_gain_config.read(self.config_filename)
		if not self._saved_rf_gain_config.has_section(self.satellite):
			self._saved_rf_gain_config.add_section(self.satellite)
		self._saved_rf_gain_config.set(self.satellite, 'rf-gain', str(self.rf_gain_slider))
		self._saved_rf_gain_config.write(open(self.config_filename, 'w'))
		self._saved_clock_alpha_config = ConfigParser.ConfigParser()
		self._saved_clock_alpha_config.read(self.config_filename)
		if not self._saved_clock_alpha_config.has_section(self.satellite):
			self._saved_clock_alpha_config.add_section(self.satellite)
		self._saved_clock_alpha_config.set(self.satellite, 'clock_alpha', str(self.clock_alpha))
		self._saved_clock_alpha_config.write(open(self.config_filename, 'w'))

	def get_sps(self):
		return self.sps

	def set_sps(self, sps):
		self.sps = sps
		self.set_hs(int(self.sps/2.0))
		self.digital_clock_recovery_mm_xx_0.set_omega(self.sps/2.0)

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

	def get_sync_check_cb(self):
		return self.sync_check_cb

	def set_sync_check_cb(self, sync_check_cb):
		self.sync_check_cb = sync_check_cb
		self._sync_check_cb_check_box.set_value(self.sync_check_cb)

	def get_saved_rf_gain(self):
		return self.saved_rf_gain

	def set_saved_rf_gain(self, saved_rf_gain):
		self.saved_rf_gain = saved_rf_gain

	def get_saved_if_gain(self):
		return self.saved_if_gain

	def set_saved_if_gain(self, saved_if_gain):
		self.saved_if_gain = saved_if_gain

	def get_satellite_text(self):
		return self.satellite_text

	def set_satellite_text(self, satellite_text):
		self.satellite_text = satellite_text
		self._satellite_text_static_text.set_value(self.satellite_text)

	def get_sample_rate_text(self):
		return self.sample_rate_text

	def set_sample_rate_text(self, sample_rate_text):
		self.sample_rate_text = sample_rate_text
		self._sample_rate_text_static_text.set_value(self.sample_rate_text)

	def get_rf_gain_slider(self):
		return self.rf_gain_slider

	def set_rf_gain_slider(self, rf_gain_slider):
		self.rf_gain_slider = rf_gain_slider
		self._saved_rf_gain_config = ConfigParser.ConfigParser()
		self._saved_rf_gain_config.read(self.config_filename)
		if not self._saved_rf_gain_config.has_section(self.satellite):
			self._saved_rf_gain_config.add_section(self.satellite)
		self._saved_rf_gain_config.set(self.satellite, 'rf-gain', str(self.rf_gain_slider))
		self._saved_rf_gain_config.write(open(self.config_filename, 'w'))
		self._rf_gain_slider_slider.set_value(self.rf_gain_slider)
		self._rf_gain_slider_text_box.set_value(self.rf_gain_slider)
		self.osmosdr_source_c_0.set_gain(self.rf_gain_slider, 0)

	def get_rate_tb(self):
		return self.rate_tb

	def set_rate_tb(self, rate_tb):
		self.rate_tb = rate_tb
		self._rate_tb_text_box.set_value(self.rate_tb)

	def get_pll_alpha(self):
		return self.pll_alpha

	def set_pll_alpha(self, pll_alpha):
		self.pll_alpha = pll_alpha
		self.pll.set_alpha(self.pll_alpha)
		self.pll.set_beta(self.pll_alpha**2/4.0)
		self._saved_pll_alpha_config = ConfigParser.ConfigParser()
		self._saved_pll_alpha_config.read(self.config_filename)
		if not self._saved_pll_alpha_config.has_section(self.satellite):
			self._saved_pll_alpha_config.add_section(self.satellite)
		self._saved_pll_alpha_config.set(self.satellite, 'pll_alpha', str(self.pll_alpha))
		self._saved_pll_alpha_config.write(open(self.config_filename, 'w'))
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

	def get_if_gain_slider(self):
		return self.if_gain_slider

	def set_if_gain_slider(self, if_gain_slider):
		self.if_gain_slider = if_gain_slider
		self._saved_if_gain_config = ConfigParser.ConfigParser()
		self._saved_if_gain_config.read(self.config_filename)
		if not self._saved_if_gain_config.has_section(self.satellite):
			self._saved_if_gain_config.add_section(self.satellite)
		self._saved_if_gain_config.set(self.satellite, 'if-gain', str(self.if_gain_slider))
		self._saved_if_gain_config.write(open(self.config_filename, 'w'))
		self.osmosdr_source_c_0.set_if_gain(self.if_gain_slider, 0)
		self._if_gain_slider_slider.set_value(self.if_gain_slider)
		self._if_gain_slider_text_box.set_value(self.if_gain_slider)

	def get_hs(self):
		return self.hs

	def set_hs(self, hs):
		self.hs = hs
		self.blocks_moving_average_xx_0.set_length_and_scale(self.hs, 1.0/self.hs)

	def get_freq_tb(self):
		return self.freq_tb

	def set_freq_tb(self, freq_tb):
		self.freq_tb = freq_tb
		self._freq_tb_text_box.set_value(self.freq_tb)

	def get_frames_outfile_text(self):
		return self.frames_outfile_text

	def set_frames_outfile_text(self, frames_outfile_text):
		self.frames_outfile_text = frames_outfile_text
		self._frames_outfile_text_static_text.set_value(self.frames_outfile_text)

	def get_datetime_text(self):
		return self.datetime_text

	def set_datetime_text(self, datetime_text):
		self.datetime_text = datetime_text
		self._datetime_text_static_text.set_value(self.datetime_text)

	def get_clock_alpha(self):
		return self.clock_alpha

	def set_clock_alpha(self, clock_alpha):
		self.clock_alpha = clock_alpha
		self.digital_clock_recovery_mm_xx_0.set_gain_omega(self.clock_alpha**2/4.0)
		self.digital_clock_recovery_mm_xx_0.set_gain_mu(self.clock_alpha)
		self._clock_alpha_slider.set_value(self.clock_alpha)
		self._clock_alpha_text_box.set_value(self.clock_alpha)
		self._saved_clock_alpha_config = ConfigParser.ConfigParser()
		self._saved_clock_alpha_config.read(self.config_filename)
		if not self._saved_clock_alpha_config.has_section(self.satellite):
			self._saved_clock_alpha_config.add_section(self.satellite)
		self._saved_clock_alpha_config.set(self.satellite, 'clock_alpha', str(self.clock_alpha))
		self._saved_clock_alpha_config.write(open(self.config_filename, 'w'))

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	parser.add_option("-f", "--freq", dest="freq", type="eng_float", default=eng_notation.num_to_str(1698e6),
		help="Set Frequency [default=%default]")
	parser.add_option("-r", "--rate", dest="rate", type="eng_float", default=eng_notation.num_to_str(2e6),
		help="Set Sample rate [default=%default]")
	parser.add_option("-o", "--frames-file", dest="frames_file", type="string", default=os.environ['HOME'] + '/data/noaa/frames/NOAA-XX.hrpt',
		help="Set Frames output filename [default=%default]")
	parser.add_option("-d", "--rtlsdr", dest="rtlsdr", type="string", default="rtl=0",
		help="Set RTLSDR Device [default=%default]")
	parser.add_option("-i", "--ifgain", dest="ifgain", type="eng_float", default=eng_notation.num_to_str(20),
		help="Set IF Gain [default=%default]")
	parser.add_option("-S", "--satellite", dest="satellite", type="string", default='NOAA-XX',
		help="Set Satellite [default=%default]")
	parser.add_option("-c", "--sync-check", dest="sync_check", type="intx", default=False,
		help="Set Sync check [default=%default]")
	parser.add_option("-g", "--rfgain", dest="rfgain", type="eng_float", default=eng_notation.num_to_str(40),
		help="Set RF Gain [default=%default]")
	(options, args) = parser.parse_args()
	tb = pw_rtlsdr_rx_noaa_hrpt(freq=options.freq, rate=options.rate, frames_file=options.frames_file, rtlsdr=options.rtlsdr, ifgain=options.ifgain, satellite=options.satellite, sync_check=options.sync_check, rfgain=options.rfgain)
	tb.Run(True)

