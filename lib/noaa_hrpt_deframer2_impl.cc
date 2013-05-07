/* -*- c++ -*- */
/* 
 * Copyright 2013 <+YOU OR YOUR COMPANY+>.
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
#define ST_SYNCING      1
#define ST_SYNCED       2
#define ST_CHECK_SYNC   3


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
        d_resync_after(idle_after_n_sync_not_found)
    {
        d_mid_bit = true;
        d_last_bit = 0;

        enter_idle();
    }

    /*
     * Our virtual destructor.
     */
    noaa_hrpt_deframer2_impl::~noaa_hrpt_deframer2_impl()
    {
    }

    void
    noaa_hrpt_deframer2_impl::forecast(int noutput_items, gr_vector_int &ninput_items_required)
    {

       ninput_items_required[0] = noutput_items * NOAA_HRPT_BITS_PER_WORD * 2;
    }

    void
    noaa_hrpt_deframer2_impl::enter_idle(void)
    {
        d_state = ST_IDLE;
        d_item_count = 0;
        d_sync_marker_count = 0;
        d_nosync_marker_count = 0;
    }


    int
    noaa_hrpt_deframer2_impl::work(int noutput_items,
			  gr_vector_const_void_star &input_items,
			  gr_vector_void_star &output_items)
    {
        const float *in = (const float *) input_items[0];
        float *out = (float *) output_items[0];

        // Do <+signal processing+>

        // Tell runtime system how many output items we produced.
        return noutput_items;
    }

  } /* namespace poesweather */
} /* namespace gr */

