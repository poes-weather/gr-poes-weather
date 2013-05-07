/* -*- c++ -*- */

#define POESWEATHER_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "poesweather_swig_doc.i"

%{
#include "poesweather/noaa_hrpt_deframer.h"
#include "poesweather/noaa_hrpt_deframer2.h"
%}


%include "poesweather/noaa_hrpt_deframer.h"
GR_SWIG_BLOCK_MAGIC2(poesweather, noaa_hrpt_deframer);
%include "poesweather/noaa_hrpt_deframer2.h"
GR_SWIG_BLOCK_MAGIC2(poesweather, noaa_hrpt_deframer2);
