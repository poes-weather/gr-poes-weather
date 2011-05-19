/* -*- c++ -*- */
/*
 * Copyright 2010 Free Software Foundation, Inc.
 * 
 * This file is part of gr-poes-weather high resolution
 * satellite imagery signal processing package.
 * 
 * POES-Weather Ltd
 * http://www.poes-weather.com
 *
 * gr-poes-weather is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * gr-poes-weather is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

GR_SWIG_BLOCK_MAGIC(poesweather,fy1_hrpt_decoder)

poesweather_fy1_hrpt_decoder_sptr
poesweather_make_fy1_hrpt_decoder(bool verbose, bool output_files);

class poesweather_fy1_hrpt_decoder : public gr_sync_block
{
private:
  poesweather_fy1_hrpt_decoder();
};
