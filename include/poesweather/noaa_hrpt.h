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

#ifndef INCLUDED_POESWEATHER_NOAA_HRPT_H
#define INCLUDED_POESWEATHER_NOAA_HRPT_H

#define NOAA_HRPT_SYNC1 0x0284
#define NOAA_HRPT_SYNC2 0x016F
#define NOAA_HRPT_SYNC3 0x035C
#define NOAA_HRPT_SYNC4 0x019D
#define NOAA_HRPT_SYNC5 0x020F
#define NOAA_HRPT_SYNC6 0x0095

#define NOAA_HRPT_MINOR_FRAME_SYNC  0x0A116FD719D83C95LL

#define NOAA_HRPT_BITS_PER_WORD     10
#define NOAA_HRPT_SYNC_WORDS        6
#define NOAA_HRPT_SYNC_BITS         (NOAA_HRPT_BITS_PER_WORD * NOAA_HRPT_SYNC_WORDS)
#define NOAA_HRPT_MINOR_FRAME_WORDS 11090

#define IS_NOAA_HRPT_SYNC(sync) ( ((sync & 0x0FFFFFFFFFFFFFFFLL) == NOAA_HRPT_MINOR_FRAME_SYNC) ? 1:0 )

#endif /* INCLUDED_POESWEATHER_NOAA_HRPT_H */
