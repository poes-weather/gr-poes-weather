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

#ifndef INCLUDED_POESWEATHER_FY1_HRPT_H
#define INCLUDED_POESWEATHER_FY1_HRPT_H

#define FY1_HRPT_SYNC1 0x0284
#define FY1_HRPT_SYNC2 0x016F
#define FY1_HRPT_SYNC3 0x035C
#define FY1_HRPT_SYNC4 0x019D
#define FY1_HRPT_SYNC5 0x020F
#define FY1_HRPT_SYNC6 0x0095

#define FY1_HRPT_MINOR_FRAME_SYNC  0x0A116FD719D83C95LL

#define FY1_HRPT_SYNC_WORDS        6
#define FY1_HRPT_MINOR_FRAME_WORDS 22180
#define FY1_HRPT_BITS_PER_WORD     10

#endif /* INCLUDED_POESWEATHER_FY1_HRPT_H */
