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

#ifndef INCLUDED_POES_WEATHER_MN1_HRPT_H
#define INCLUDED_POES_WEATHER_MN1_HRPT_H

// Standard 32 bit CCSDS ASM sync marker
#define MN1_HRPT_FRAME_SYNC  0x1ACFFC1DL

#define MN1_HRPT_SYNC_WORDS      2
#define MN1_HRPT_FRAME_WORDS   256
#define MN1_HRPT_BITS_PER_WORD  16

#endif /* INCLUDED_POES_WEATHER_MN1_HRPT_H */
