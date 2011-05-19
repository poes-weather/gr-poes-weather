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

#ifndef INCLUDED_POESWEATHER_FY1_HRPT_DECODER_H
#define INCLUDED_POESWEATHER_FY1_HRPT_DECODER_H

#include <gr_sync_block.h>

class poesweather_fy1_hrpt_decoder;
typedef boost::shared_ptr<poesweather_fy1_hrpt_decoder> poesweather_fy1_hrpt_decoder_sptr;

poesweather_fy1_hrpt_decoder_sptr
poesweather_make_fy1_hrpt_decoder(bool verbose, bool output_files);

class poesweather_fy1_hrpt_decoder : public gr_sync_block
{
  friend poesweather_fy1_hrpt_decoder_sptr poesweather_make_fy1_hrpt_decoder(bool verbose, bool output_files);
  poesweather_fy1_hrpt_decoder(bool verbose, bool output_files);

  // Configuration
  bool d_verbose;
  bool d_output_files;

  // Frame-level state
  unsigned short d_current_word;
  unsigned int   d_word_num;
  int            d_frames_seen;

  // Minor frame number
  int  d_seq_errs;
  bool d_frame_error;

  // Spacecraft id
  unsigned short d_id;

  // Minor frame timestamp
  unsigned short d_day_count;
  unsigned short d_part_of_ms_of_day_count;
  unsigned long  d_milliseconds;
  unsigned long  d_last_time;;

  void process_id();
  void process_day_count();
  void process_part_of_ms_of_day_count();
  void process_part_of_ms();
  void process_remainder_of_ms();

public:
  ~poesweather_fy1_hrpt_decoder();

  int work(int noutput_items,
	   gr_vector_const_void_star &input_items,
	   gr_vector_void_star &output_items);
};

#endif /* INCLUDED_POESWEATHER_FY1_HRPT_DECODER_H */
