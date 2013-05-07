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


#ifndef INCLUDED_POESWEATHER_NOAA_HRPT_DEFRAMER_H
#define INCLUDED_POESWEATHER_NOAA_HRPT_DEFRAMER_H

#include <poesweather/api.h>
#include <poesweather/noaa_hrpt.h>
#include <gr_block.h>

namespace gr {
  namespace poesweather {

    /*!
     * \brief <+description of block+>
     * \ingroup poesweather
     *
     */
    class POESWEATHER_API noaa_hrpt_deframer : virtual public gr_block
    {
     public:
      typedef boost::shared_ptr<noaa_hrpt_deframer> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of poesweather::noaa_hrpt_deframer.
       *
       * To avoid accidental use of raw pointers, poesweather::noaa_hrpt_deframer's
       * constructor is in a private implementation
       * class. poesweather::noaa_hrpt_deframer::make is the public interface for
       * creating new instances.
       */
      static sptr make(bool sync_check=false);
    };

  } // namespace poesweather
} // namespace gr

#endif /* INCLUDED_POESWEATHER_NOAA_HRPT_DEFRAMER_H */

