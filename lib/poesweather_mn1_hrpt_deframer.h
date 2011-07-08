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

#ifndef INCLUDED_POESWEATHER_MN1_HRPT_DEFRAMER_H
#define INCLUDED_POESWEATHER_MN1_HRPT_DEFRAMER_H

#include <gr_block.h>

class poesweather_mn1_hrpt_deframer;
typedef boost::shared_ptr<poesweather_mn1_hrpt_deframer> poesweather_mn1_hrpt_deframer_sptr;

poesweather_mn1_hrpt_deframer_sptr
poesweather_make_mn1_hrpt_deframer(bool sync_check);

class poesweather_mn1_hrpt_deframer : public gr_block
{
  friend poesweather_mn1_hrpt_deframer_sptr poesweather_make_mn1_hrpt_deframer(bool sync_check);
  poesweather_mn1_hrpt_deframer(bool sync_check);

  bool           d_sync_check;

  unsigned int   d_state;
  bool           d_mid_bit;
  unsigned char  d_last_bit;
  unsigned int   d_bit_count;
  unsigned int   d_word_count;
  unsigned long  d_shifter;     // 32 bit sync word
  unsigned short d_word;        // 10 bit HRPT word

  void enter_idle();
  void enter_synced();
 
public:
  int general_work(int noutput_items,
		   gr_vector_int &ninput_items,
		   gr_vector_const_void_star &input_items,
		   gr_vector_void_star &output_items);
};

#endif /* INCLUDED_POESWEATHER_MN1_HRPT_DEFRAMER_H */
