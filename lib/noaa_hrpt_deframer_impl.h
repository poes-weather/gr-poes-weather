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

#ifndef INCLUDED_POESWEATHER_NOAA_HRPT_DEFRAMER_IMPL_H
#define INCLUDED_POESWEATHER_NOAA_HRPT_DEFRAMER_IMPL_H

#include <poesweather/noaa_hrpt_deframer.h>


namespace gr {
  namespace poesweather {

  class noaa_hrpt_deframer_impl : public noaa_hrpt_deframer
  {
  public:
      noaa_hrpt_deframer_impl(bool sync_check);
      ~noaa_hrpt_deframer_impl(void);


      // Where all the action really happens
      void forecast(int noutput_items, gr_vector_int &ninput_items_required);
      int general_work(int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items);

  protected:
      void enter_idle(void);
      void enter_synced(void);

  private:
      bool               d_sync_check;

      unsigned int       d_state;
      bool               d_mid_bit;
      unsigned char      d_last_bit;
      unsigned int       d_bit_count;
      unsigned int       d_word_count;
      unsigned long long d_shifter;     // 60 bit sync word
      unsigned short     d_word;        // 10 bit HRPT word

  };

  } // namespace poesweather
} // namespace gr

#endif /* INCLUDED_POESWEATHER_NOAA_HRPT_DEFRAMER_IMPL_H */

