/*
 Copyright (C) 2016-2017 Alexander Borisov
 
 This library is free software; you can redistribute it and/or
 modify it under the terms of the GNU Lesser General Public
 License as published by the Free Software Foundation; either
 version 2.1 of the License, or (at your option) any later version.
 
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 Lesser General Public License for more details.
 
 You should have received a copy of the GNU Lesser General Public
 License along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 
 Author: lex.borisov@gmail.com (Alexander Borisov)
*/

#ifndef MyHTML_MyCSS_VALUES_UNITS_RESOURCES_H
#define MyHTML_MyCSS_VALUES_UNITS_RESOURCES_H
#pragma once

#define MyCSS_UNITS_STATIC_INDEX_FOR_SEARCH_SIZE 199

static const char * mycss_units_index_name[31] = {
    "", "deg", "grad", "rad", "turn", "Hz", "kHz", "cm", "in", "mm", "pc",
    "pt", "px", "q", "ch", "em", "ex", "ic", "rem", "vb", "vh",
    "vi", "vmax", "vmin", "vw", "dpcm", "dpi", "dppx", "ms", "s", NULL
};

static const mycss_units_index_static_entry_t mycss_units_index_static_for_search[] =
{
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"grad", 4, MyCSS_UNIT_TYPE_GRAD, 0, 8},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"px", 2, MyCSS_UNIT_TYPE_PX, 0, 16},
    {"in", 2, MyCSS_UNIT_TYPE_IN, 0, 17},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"dpcm", 4, MyCSS_UNIT_TYPE_DPCM, 0, 20},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"vw", 2, MyCSS_UNIT_TYPE_VW, 0, 26},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"q", 1, MyCSS_UNIT_TYPE_Q, 0, 34},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"dppx", 4, MyCSS_UNIT_TYPE_DPPX, 0, 42},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"vb", 2, MyCSS_UNIT_TYPE_VB, 0, 45},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"deg", 3, MyCSS_UNIT_TYPE_DEG, 0, 56},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"dpi", 3, MyCSS_UNIT_TYPE_DPI, 0, 59},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"rem", 3, MyCSS_UNIT_TYPE_REM, 0, 66},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"vh", 2, MyCSS_UNIT_TYPE_VH, 0, 68},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"mm", 2, MyCSS_UNIT_TYPE_MM, 0, 82},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"pc", 2, MyCSS_UNIT_TYPE_PC, 0, 88},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"cm", 2, MyCSS_UNIT_TYPE_CM, 0, 91},
    {"s", 1, MyCSS_UNIT_TYPE_S, 0, 92},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"ic", 2, MyCSS_UNIT_TYPE_IC, 0, 95},
    {"ch", 2, MyCSS_UNIT_TYPE_CH, 0, 96},
    {"turn", 4, MyCSS_UNIT_TYPE_TURN, 0, 97},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"Hz", 2, MyCSS_UNIT_TYPE_HZ, 0, 104},
    {"vi", 2, MyCSS_UNIT_TYPE_VI, 0, 105},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"pt", 2, MyCSS_UNIT_TYPE_PT, 0, 115},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"vmax", 4, MyCSS_UNIT_TYPE_VMAX, 0, 125},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"em", 2, MyCSS_UNIT_TYPE_EM, 0, 129},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"kHz", 3, MyCSS_UNIT_TYPE_KHZ, 0, 159},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"ex", 2, MyCSS_UNIT_TYPE_EX, 0, 162},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"rad", 3, MyCSS_UNIT_TYPE_RAD, 0, 172},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"vmin", 4, MyCSS_UNIT_TYPE_VMIN, 0, 181},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {"ms", 2, MyCSS_UNIT_TYPE_MS, 0, 196},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
    {NULL, 0, MyCSS_UNIT_TYPE_UNDEF, 0, 0},
};

#endif /* MyHTML_MyCSS_VALUES_UNITS_RESOURCES_H */
