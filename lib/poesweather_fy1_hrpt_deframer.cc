/* -*- c++ -*- */
/*
 * Copyright 2010 Free Software Foundation, Inc.
 * 
 * This file is part of gr-poes-weather high resolution
 * satellite imagery signal processing package.
 * 
 * This signal procressing block is derived from GNU Radio
 * gr-noaa hrpt_deframer.
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

#include <poesweather_fy1_hrpt_deframer.h>
#include <poesweather_fy1_hrpt.h>
#include <gr_io_signature.h>
#include <cstring>
#include <cstdio>

#define ST_IDLE   0
#define ST_SYNCED 1

poesweather_fy1_hrpt_deframer_sptr
poesweather_make_fy1_hrpt_deframer(bool sync_check)
{
  return gnuradio::get_initial_sptr(new poesweather_fy1_hrpt_deframer(sync_check));
}

poesweather_fy1_hrpt_deframer::poesweather_fy1_hrpt_deframer(bool sync_check)
  : gr_block("fy1_hrpt_deframer",
	     gr_make_io_signature(1, 1, sizeof(char)),
             gr_make_io_signature(1, 1, sizeof(short))),
  d_sync_check(sync_check)
{
  set_output_multiple(FY1_HRPT_SYNC_WORDS); // room for writing full sync when received
  d_mid_bit = true;
  d_last_bit = 0;
  enter_idle();
}

void
poesweather_fy1_hrpt_deframer::enter_idle()
{
  d_state = ST_IDLE;
}

void
poesweather_fy1_hrpt_deframer::enter_synced()
{
  d_state = ST_SYNCED;
  d_bit_count = FY1_HRPT_BITS_PER_WORD;
  d_word_count = FY1_HRPT_MINOR_FRAME_WORDS - FY1_HRPT_SYNC_WORDS;
  d_word = 0;
}

int
poesweather_fy1_hrpt_deframer::general_work(int noutput_items,
				 gr_vector_int &ninput_items,
				 gr_vector_const_void_star &input_items,
				 gr_vector_void_star &output_items)
{
  int ninputs = ninput_items[0];
  const char *in = (const char *)input_items[0];
  unsigned short *out = (unsigned short *)output_items[0];

  int i = 0, j = 0;
  while (i < ninputs && j < noutput_items) {
    char bit = in[i++];
    char diff = bit^d_last_bit;
    d_last_bit = bit;

    // Wait for transition if not synced, otherwise, alternate bits
    if (d_mid_bit && (diff | (d_state == ST_SYNCED))) {
      switch (d_state) {
      case ST_IDLE:
	d_shifter = (d_shifter << 1) | bit; // MSB transmitted first
	
        if ((d_shifter & 0x0FFFFFFFFFFFFFFFLL) == FY1_HRPT_MINOR_FRAME_SYNC) {
          out[j++] = FY1_HRPT_SYNC1;
          out[j++] = FY1_HRPT_SYNC2;
          out[j++] = FY1_HRPT_SYNC3;
          out[j++] = FY1_HRPT_SYNC4;
          out[j++] = FY1_HRPT_SYNC5;
          out[j++] = FY1_HRPT_SYNC6;
	  enter_synced();
	}
	break;
	
      case ST_SYNCED:
	d_word = (d_word << 1) | bit; // MSB transmitted first
	if (--d_bit_count == 0) {
	  out[j++] = d_word;
	  d_word = 0;
          d_bit_count = FY1_HRPT_BITS_PER_WORD;
	  if (--d_word_count == 0) {
              if (d_sync_check)
                  enter_idle();
              else 
                  d_word_count = FY1_HRPT_MINOR_FRAME_WORDS;
	  }
	}
	break;
	
      default:
        throw std::runtime_error("poesweather_fy1_hrpt_deframer: bad state\n");
      }

      d_mid_bit = false;
    }
    else {
      d_mid_bit = true;
    }
  }

  consume_each(i);
  return j;
}
