/* -*- c++ -*- */
/* 
 * Copyright 2013:
 *      POES-Weather Ab Ltd             info@poes-weather.com
 *      Martin Blaho
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
#include "noaa_hrpt_deframer2_impl.h"

#define ST_IDLE         0
#define ST_SYNCED       1


namespace gr {
  namespace poesweather {

    noaa_hrpt_deframer2::sptr
    noaa_hrpt_deframer2::make(int idle_after_n_sync_not_found)
    {
      return gnuradio::get_initial_sptr (new noaa_hrpt_deframer2_impl(idle_after_n_sync_not_found));
    }

    /*
     * The private constructor
     */
    noaa_hrpt_deframer2_impl::noaa_hrpt_deframer2_impl(int idle_after_n_sync_not_found)
      : gr_block("noaa_hrpt_deframer2",
                 gr_make_io_signature(1, 1, sizeof(unsigned char)),
                 gr_make_io_signature(1, 1, sizeof(unsigned short))),
        d_idle_after_n_sync_fail(idle_after_n_sync_not_found)
    {
        set_output_multiple(NOAA_HRPT_SYNC_WORDS);

        d_mid_bit = true;
        d_last_bit = 0;
        d_sync_marker_count = 0;

        enter_idle();
    }

    /*
     * Our virtual destructor.
     */
    noaa_hrpt_deframer2_impl::~noaa_hrpt_deframer2_impl()
    {
    }

#if 0
    void
    noaa_hrpt_deframer2_impl::forecast(int noutput_items, gr_vector_int &ninput_items_required)
    {

       ninput_items_required[0] = noutput_items * NOAA_HRPT_BITS_PER_WORD * 2;
    }
#endif

    void
    noaa_hrpt_deframer2_impl::enter_idle(void)
    {
        d_state = ST_IDLE;
        d_bit_count = 0;
    }

    void
    noaa_hrpt_deframer2_impl::enter_synced(void)
    {
        d_state = ST_SYNCED;
        d_bit_count = NOAA_HRPT_BITS_PER_WORD;
        d_word_count = NOAA_HRPT_MINOR_FRAME_WORDS - NOAA_HRPT_SYNC_WORDS;
        d_word = 0;
    }

    int
    noaa_hrpt_deframer2_impl::general_work(int noutput_items,
                                           gr_vector_int &ninput_items,
                                           gr_vector_const_void_star &input_items,
                                           gr_vector_void_star &output_items)
    {
        const unsigned char *in = (const unsigned char *) input_items[0];
        unsigned short *out = (unsigned short *) output_items[0];
        int ninputs = ninput_items[0];
        unsigned char bit, diff;
        int i, j;

        i = j = 0;
        while(i < ninputs && j < noutput_items) {

            bit = in[i++];
            diff = bit ^ d_last_bit;
            d_last_bit = bit;

            if(d_mid_bit && (diff | (d_state == ST_SYNCED))) {

                switch (d_state) {

                case ST_IDLE:
                    d_shifter = (d_shifter << 1) | bit;
                    d_bit_count++;

                    if(IS_NOAA_HRPT_SYNC(d_shifter)) {
                        // perfect sync marker found

                        write_sync(out, &j);
                        d_bad_sync_marker_count = 0;
                    }
                    else if(d_sync_marker_count && d_bit_count == NOAA_HRPT_SYNC_BITS) {
                        // we have a bad sync marker

                        if(++d_bad_sync_marker_count < d_idle_after_n_sync_fail)
                            write_sync(out, &j); // hope it was some temporary interference...
                    }

                    break;

                case ST_SYNCED:

                    d_word = (d_word << 1) | bit;

                    if(--d_bit_count == 0) {
                        out[j++] = d_word;
                        d_word = 0;
                        d_bit_count = NOAA_HRPT_BITS_PER_WORD;

                        if(--d_word_count == 0)
                            enter_idle();
                    }

                    break;

                default:
                    throw std::runtime_error("noaa_hrpt_deframer2_impl: bad state\n");
                }

                d_mid_bit = false;
            }
            else
                d_mid_bit = true;
        }


        consume_each(i);
        return j;
    }

    void
    noaa_hrpt_deframer2_impl::write_sync(unsigned short *out, int *index)
    {
        out[*index++] = NOAA_HRPT_SYNC1;
        out[*index++] = NOAA_HRPT_SYNC2;
        out[*index++] = NOAA_HRPT_SYNC3;
        out[*index++] = NOAA_HRPT_SYNC4;
        out[*index++] = NOAA_HRPT_SYNC5;
        out[*index++] = NOAA_HRPT_SYNC6;

        d_sync_marker_count++;
        enter_synced();
    }

  } /* namespace poesweather */
} /* namespace gr */

