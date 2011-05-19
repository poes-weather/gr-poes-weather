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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <poesweather_fy1_hrpt_decoder.h>
#include <poesweather_fy1_hrpt.h>
#include <gr_io_signature.h>
#include <cstdio>

poesweather_fy1_hrpt_decoder_sptr
poesweather_make_fy1_hrpt_decoder(bool verbose, bool output_files)
{
  return gnuradio::get_initial_sptr(new poesweather_fy1_hrpt_decoder(verbose, output_files));
}

poesweather_fy1_hrpt_decoder::poesweather_fy1_hrpt_decoder(bool verbose, bool output_files)
  : gr_sync_block("fy1_hrpt_decoder",
		  gr_make_io_signature(1, 1, sizeof(short)),
		  gr_make_io_signature(0, 0, 0)),
    d_verbose(verbose),
    d_output_files(output_files),
    d_word_num(0),
    d_frames_seen(0),
    d_seq_errs(0),
    d_frame_error(false),
    d_id(0),
    d_day_count(0),
    d_part_of_ms_of_day_count(0),
    d_milliseconds(0),
    d_last_time(0)
{

}

int
poesweather_fy1_hrpt_decoder::work(int noutput_items,
			gr_vector_const_void_star &input_items,
			gr_vector_void_star &output_items)
{
  const unsigned short *in = (const unsigned short *) input_items[0];

  int i = 0;
  while (i < noutput_items) {
    d_current_word = in[i++] & 0x3FF;
    d_word_num++;

    switch (d_word_num) {
    case 7:
      process_id();
      break;

    case 9:
      process_day_count();
      break;

    case 10:
      process_part_of_ms_of_day_count();
      break;

    case 11:
      process_part_of_ms();
      break;

    case 12:
      process_remainder_of_ms();
      break;

    default:
      break;
    }

    if(d_word_num == FY1_HRPT_MINOR_FRAME_WORDS) {
       fprintf(stderr, "\n");

       if(d_frame_error)
          d_seq_errs++;
 
       d_frame_error = false;
       d_word_num = 0;
       d_frames_seen++;
    }
  }

  return i;
}

void
poesweather_fy1_hrpt_decoder::process_id()
{ 
  char id;

  d_id = (d_current_word & 0x03C0) >> 6;

  if(d_id == 0x000C)
     id = 'C';
  else if(d_id == 0x000D)
     id = 'D';
  else {
     d_frame_error = true;
     id = '?';
  }

  if(d_verbose)
     fprintf(stderr, "%cFeng-Yun 1%c: ", id == '?' ? '*':' ', id);
}

void
poesweather_fy1_hrpt_decoder::process_day_count()
{
  d_day_count = d_current_word >> 1;

  if(d_verbose)
     fprintf(stderr, "Day count: %03d ", d_day_count);
}

void
poesweather_fy1_hrpt_decoder::process_part_of_ms_of_day_count()
{
  if(d_current_word & 0x0280) 
     d_part_of_ms_of_day_count = d_current_word ^ 0x0280;
  else {
     d_frame_error = true; 
     d_part_of_ms_of_day_count = 0x02FF;
  }

  if(d_verbose)
     fprintf(stderr, "%cMS: %03d, ", 
             d_part_of_ms_of_day_count == 0x02FF ? '*':' ',
             d_part_of_ms_of_day_count);
}

void
poesweather_fy1_hrpt_decoder::process_part_of_ms()
{
  d_milliseconds = d_current_word << 10;
}

void
poesweather_fy1_hrpt_decoder::process_remainder_of_ms()
{
  int delta;

  d_milliseconds |= d_current_word;

  delta = d_milliseconds - d_last_time;
  d_last_time = d_milliseconds;

  if(d_verbose)
     fprintf(stderr, "MS: %08d delta: %08d", d_milliseconds, delta);
}

poesweather_fy1_hrpt_decoder::~poesweather_fy1_hrpt_decoder()
{
  if(d_verbose) {
     fprintf(stderr, "Frames seen:     %10i\n", d_frames_seen);
     fprintf(stderr, "Sequence errors: %10i\n", d_seq_errs);
  }
}
