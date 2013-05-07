/* -*- c++ -*- */
/* 
 * Copyright 2013 POES-Weather Ab Ltd
 * info@poes-weather.com
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gr_io_signature.h>
#include <cstring>
#include <cstdio>
#include "noaa_hrpt_deframer_impl.h"

#define ST_IDLE   0
#define ST_SYNCED 1


namespace gr {
  namespace poesweather {

    noaa_hrpt_deframer::sptr
    noaa_hrpt_deframer::make(bool sync_check)
    {
      return gnuradio::get_initial_sptr (new noaa_hrpt_deframer_impl(sync_check));
    }

    /*
     * The private constructor
     */
    noaa_hrpt_deframer_impl::noaa_hrpt_deframer_impl(bool sync_check)    
      : gr_block("noaa_hrpt_deframer",
                 gr_make_io_signature(1, 1, sizeof(unsigned char)),
                 gr_make_io_signature(1, 1, sizeof(unsigned short))),
        d_sync_check(sync_check)
    {
        set_output_multiple(NOAA_HRPT_SYNC_WORDS); // room for writing full sync when received
        d_mid_bit = true;
        d_last_bit = 0;

        enter_idle();
    }

    /*
     * Our virtual destructor.
     */
    noaa_hrpt_deframer_impl::~noaa_hrpt_deframer_impl(void)
    {
    }

    void
    noaa_hrpt_deframer_impl::enter_idle(void)
    {
        d_state = ST_IDLE;
    }

    void
    noaa_hrpt_deframer_impl::enter_synced(void)
    {
        d_state = ST_SYNCED;
        d_bit_count = NOAA_HRPT_BITS_PER_WORD;
        d_word_count = NOAA_HRPT_MINOR_FRAME_WORDS - NOAA_HRPT_SYNC_WORDS;
        d_word = 0;
    }

    void
    noaa_hrpt_deframer_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
        /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
    }

    int
    noaa_hrpt_deframer_impl::general_work(int noutput_items,
                                          gr_vector_int &ninput_items,
                                          gr_vector_const_void_star &input_items,
                                          gr_vector_void_star &output_items)
    {
        char bit, diff;

        int ninputs = ninput_items[0];
        const char *in = (const char *)input_items[0];
        unsigned short *out = (unsigned short *)output_items[0];

        int i = 0, j = 0;
        while(i < ninputs && j < noutput_items) {
            bit = in[i++];
            diff = bit ^ d_last_bit;
            d_last_bit = bit;

            // Wait for transition if not synced, otherwise, alternate bits
            if(d_mid_bit && (diff | (d_state == ST_SYNCED))) {
                switch(d_state) {

                case ST_IDLE:
                    d_shifter = (d_shifter << 1) | bit; // MSB transmitted first

                    if((d_shifter & 0x0FFFFFFFFFFFFFFFLL) == NOAA_HRPT_MINOR_FRAME_SYNC) {
                        out[j++] = NOAA_HRPT_SYNC1;
                        out[j++] = NOAA_HRPT_SYNC2;
                        out[j++] = NOAA_HRPT_SYNC3;
                        out[j++] = NOAA_HRPT_SYNC4;
                        out[j++] = NOAA_HRPT_SYNC5;
                        out[j++] = NOAA_HRPT_SYNC6;

                        enter_synced();
                    }

                    break;

                case ST_SYNCED:
                    d_word = (d_word << 1) | bit; // MSB transmitted first
                    if(--d_bit_count == 0) {
                        out[j++] = d_word;
                        d_word = 0;
                        d_bit_count = NOAA_HRPT_BITS_PER_WORD;

                        if(--d_word_count == 0) {
                            if(d_sync_check)
                                enter_idle();
                            else
                                d_word_count = NOAA_HRPT_MINOR_FRAME_WORDS;
                        }
                    }

                    break;

                default:
                    throw std::runtime_error("poesweather_noaa_hrpt_deframer: bad state\n");
                }

                d_mid_bit = false;
            }
            else
                d_mid_bit = true;

        }

        // Tell runtime system how many input items we consumed on
        // each input stream.
        consume_each(i);

        // Tell runtime system how many output items we produced.
        return j;
    }

  } /* namespace poesweather */
} /* namespace gr */

