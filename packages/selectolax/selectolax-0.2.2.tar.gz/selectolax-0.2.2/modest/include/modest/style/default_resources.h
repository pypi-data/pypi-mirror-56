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

#ifndef MODEST_STYLE_DEFAULT_RESOURCES_H
#define MODEST_STYLE_DEFAULT_RESOURCES_H
#pragma once

#include <modest/style/default_entries.h>

static const modest_style_default_by_html_node_f modest_style_default_function_of_declarations[MyHTML_TAG_LAST_ENTRY] = 
{
	modest_style_default_declaration_by_html_node__undef,
	modest_style_default_declaration_by_html_node__text,
	modest_style_default_declaration_by_html_node__comment,
	modest_style_default_declaration_by_html_node__doctype,
	modest_style_default_declaration_by_html_node_a,
	modest_style_default_declaration_by_html_node_abbr,
	modest_style_default_declaration_by_html_node_acronym,
	modest_style_default_declaration_by_html_node_address,
	modest_style_default_declaration_by_html_node_annotation_xml,
	modest_style_default_declaration_by_html_node_applet,
	modest_style_default_declaration_by_html_node_area,
	modest_style_default_declaration_by_html_node_article,
	modest_style_default_declaration_by_html_node_aside,
	modest_style_default_declaration_by_html_node_audio,
	modest_style_default_declaration_by_html_node_b,
	modest_style_default_declaration_by_html_node_base,
	modest_style_default_declaration_by_html_node_basefont,
	modest_style_default_declaration_by_html_node_bdi,
	modest_style_default_declaration_by_html_node_bdo,
	modest_style_default_declaration_by_html_node_bgsound,
	modest_style_default_declaration_by_html_node_big,
	modest_style_default_declaration_by_html_node_blink,
	modest_style_default_declaration_by_html_node_blockquote,
	modest_style_default_declaration_by_html_node_body,
	modest_style_default_declaration_by_html_node_br,
	modest_style_default_declaration_by_html_node_button,
	modest_style_default_declaration_by_html_node_canvas,
	modest_style_default_declaration_by_html_node_caption,
	modest_style_default_declaration_by_html_node_center,
	modest_style_default_declaration_by_html_node_cite,
	modest_style_default_declaration_by_html_node_code,
	modest_style_default_declaration_by_html_node_col,
	modest_style_default_declaration_by_html_node_colgroup,
	modest_style_default_declaration_by_html_node_command,
	modest_style_default_declaration_by_html_node_comment,
	modest_style_default_declaration_by_html_node_datalist,
	modest_style_default_declaration_by_html_node_dd,
	modest_style_default_declaration_by_html_node_del,
	modest_style_default_declaration_by_html_node_details,
	modest_style_default_declaration_by_html_node_dfn,
	modest_style_default_declaration_by_html_node_dialog,
	modest_style_default_declaration_by_html_node_dir,
	modest_style_default_declaration_by_html_node_div,
	modest_style_default_declaration_by_html_node_dl,
	modest_style_default_declaration_by_html_node_dt,
	modest_style_default_declaration_by_html_node_em,
	modest_style_default_declaration_by_html_node_embed,
	modest_style_default_declaration_by_html_node_fieldset,
	modest_style_default_declaration_by_html_node_figcaption,
	modest_style_default_declaration_by_html_node_figure,
	modest_style_default_declaration_by_html_node_font,
	modest_style_default_declaration_by_html_node_footer,
	modest_style_default_declaration_by_html_node_form,
	modest_style_default_declaration_by_html_node_frame,
	modest_style_default_declaration_by_html_node_frameset,
	modest_style_default_declaration_by_html_node_h1,
	modest_style_default_declaration_by_html_node_h2,
	modest_style_default_declaration_by_html_node_h3,
	modest_style_default_declaration_by_html_node_h4,
	modest_style_default_declaration_by_html_node_h5,
	modest_style_default_declaration_by_html_node_h6,
	modest_style_default_declaration_by_html_node_head,
	modest_style_default_declaration_by_html_node_header,
	modest_style_default_declaration_by_html_node_hgroup,
	modest_style_default_declaration_by_html_node_hr,
	modest_style_default_declaration_by_html_node_html,
	modest_style_default_declaration_by_html_node_i,
	modest_style_default_declaration_by_html_node_iframe,
	modest_style_default_declaration_by_html_node_image,
	modest_style_default_declaration_by_html_node_img,
	modest_style_default_declaration_by_html_node_input,
	modest_style_default_declaration_by_html_node_ins,
	modest_style_default_declaration_by_html_node_isindex,
	modest_style_default_declaration_by_html_node_kbd,
	modest_style_default_declaration_by_html_node_keygen,
	modest_style_default_declaration_by_html_node_label,
	modest_style_default_declaration_by_html_node_legend,
	modest_style_default_declaration_by_html_node_li,
	modest_style_default_declaration_by_html_node_link,
	modest_style_default_declaration_by_html_node_listing,
	modest_style_default_declaration_by_html_node_main,
	modest_style_default_declaration_by_html_node_map,
	modest_style_default_declaration_by_html_node_mark,
	modest_style_default_declaration_by_html_node_marquee,
	modest_style_default_declaration_by_html_node_menu,
	modest_style_default_declaration_by_html_node_menuitem,
	modest_style_default_declaration_by_html_node_meta,
	modest_style_default_declaration_by_html_node_meter,
	modest_style_default_declaration_by_html_node_mtext,
	modest_style_default_declaration_by_html_node_nav,
	modest_style_default_declaration_by_html_node_nobr,
	modest_style_default_declaration_by_html_node_noembed,
	modest_style_default_declaration_by_html_node_noframes,
	modest_style_default_declaration_by_html_node_noscript,
	modest_style_default_declaration_by_html_node_object,
	modest_style_default_declaration_by_html_node_ol,
	modest_style_default_declaration_by_html_node_optgroup,
	modest_style_default_declaration_by_html_node_option,
	modest_style_default_declaration_by_html_node_output,
	modest_style_default_declaration_by_html_node_p,
	modest_style_default_declaration_by_html_node_param,
	modest_style_default_declaration_by_html_node_plaintext,
	modest_style_default_declaration_by_html_node_pre,
	modest_style_default_declaration_by_html_node_progress,
	modest_style_default_declaration_by_html_node_q,
	modest_style_default_declaration_by_html_node_rb,
	modest_style_default_declaration_by_html_node_rp,
	modest_style_default_declaration_by_html_node_rt,
	modest_style_default_declaration_by_html_node_rtc,
	modest_style_default_declaration_by_html_node_ruby,
	modest_style_default_declaration_by_html_node_s,
	modest_style_default_declaration_by_html_node_samp,
	modest_style_default_declaration_by_html_node_script,
	modest_style_default_declaration_by_html_node_section,
	modest_style_default_declaration_by_html_node_select,
	modest_style_default_declaration_by_html_node_small,
	modest_style_default_declaration_by_html_node_source,
	modest_style_default_declaration_by_html_node_span,
	modest_style_default_declaration_by_html_node_strike,
	modest_style_default_declaration_by_html_node_strong,
	modest_style_default_declaration_by_html_node_style,
	modest_style_default_declaration_by_html_node_sub,
	modest_style_default_declaration_by_html_node_summary,
	modest_style_default_declaration_by_html_node_sup,
	modest_style_default_declaration_by_html_node_svg,
	modest_style_default_declaration_by_html_node_table,
	modest_style_default_declaration_by_html_node_tbody,
	modest_style_default_declaration_by_html_node_td,
	modest_style_default_declaration_by_html_node_template,
	modest_style_default_declaration_by_html_node_textarea,
	modest_style_default_declaration_by_html_node_tfoot,
	modest_style_default_declaration_by_html_node_th,
	modest_style_default_declaration_by_html_node_thead,
	modest_style_default_declaration_by_html_node_time,
	modest_style_default_declaration_by_html_node_title,
	modest_style_default_declaration_by_html_node_tr,
	modest_style_default_declaration_by_html_node_track,
	modest_style_default_declaration_by_html_node_tt,
	modest_style_default_declaration_by_html_node_u,
	modest_style_default_declaration_by_html_node_ul,
	modest_style_default_declaration_by_html_node_var,
	modest_style_default_declaration_by_html_node_video,
	modest_style_default_declaration_by_html_node_wbr,
	modest_style_default_declaration_by_html_node_xmp,
	modest_style_default_declaration_by_html_node_altGlyph,
	modest_style_default_declaration_by_html_node_altGlyphDef,
	modest_style_default_declaration_by_html_node_altGlyphItem,
	modest_style_default_declaration_by_html_node_animate,
	modest_style_default_declaration_by_html_node_animateColor,
	modest_style_default_declaration_by_html_node_animateMotion,
	modest_style_default_declaration_by_html_node_animateTransform,
	modest_style_default_declaration_by_html_node_circle,
	modest_style_default_declaration_by_html_node_clipPath,
	modest_style_default_declaration_by_html_node_color_profile,
	modest_style_default_declaration_by_html_node_cursor,
	modest_style_default_declaration_by_html_node_defs,
	modest_style_default_declaration_by_html_node_desc,
	modest_style_default_declaration_by_html_node_ellipse,
	modest_style_default_declaration_by_html_node_feBlend,
	modest_style_default_declaration_by_html_node_feColorMatrix,
	modest_style_default_declaration_by_html_node_feComponentTransfer,
	modest_style_default_declaration_by_html_node_feComposite,
	modest_style_default_declaration_by_html_node_feConvolveMatrix,
	modest_style_default_declaration_by_html_node_feDiffuseLighting,
	modest_style_default_declaration_by_html_node_feDisplacementMap,
	modest_style_default_declaration_by_html_node_feDistantLight,
	modest_style_default_declaration_by_html_node_feDropShadow,
	modest_style_default_declaration_by_html_node_feFlood,
	modest_style_default_declaration_by_html_node_feFuncA,
	modest_style_default_declaration_by_html_node_feFuncB,
	modest_style_default_declaration_by_html_node_feFuncG,
	modest_style_default_declaration_by_html_node_feFuncR,
	modest_style_default_declaration_by_html_node_feGaussianBlur,
	modest_style_default_declaration_by_html_node_feImage,
	modest_style_default_declaration_by_html_node_feMerge,
	modest_style_default_declaration_by_html_node_feMergeNode,
	modest_style_default_declaration_by_html_node_feMorphology,
	modest_style_default_declaration_by_html_node_feOffset,
	modest_style_default_declaration_by_html_node_fePointLight,
	modest_style_default_declaration_by_html_node_feSpecularLighting,
	modest_style_default_declaration_by_html_node_feSpotLight,
	modest_style_default_declaration_by_html_node_feTile,
	modest_style_default_declaration_by_html_node_feTurbulence,
	modest_style_default_declaration_by_html_node_filter,
	modest_style_default_declaration_by_html_node_font_face,
	modest_style_default_declaration_by_html_node_font_face_format,
	modest_style_default_declaration_by_html_node_font_face_name,
	modest_style_default_declaration_by_html_node_font_face_src,
	modest_style_default_declaration_by_html_node_font_face_uri,
	modest_style_default_declaration_by_html_node_foreignObject,
	modest_style_default_declaration_by_html_node_g,
	modest_style_default_declaration_by_html_node_glyph,
	modest_style_default_declaration_by_html_node_glyphRef,
	modest_style_default_declaration_by_html_node_hkern,
	modest_style_default_declaration_by_html_node_line,
	modest_style_default_declaration_by_html_node_linearGradient,
	modest_style_default_declaration_by_html_node_marker,
	modest_style_default_declaration_by_html_node_mask,
	modest_style_default_declaration_by_html_node_metadata,
	modest_style_default_declaration_by_html_node_missing_glyph,
	modest_style_default_declaration_by_html_node_mpath,
	modest_style_default_declaration_by_html_node_path,
	modest_style_default_declaration_by_html_node_pattern,
	modest_style_default_declaration_by_html_node_polygon,
	modest_style_default_declaration_by_html_node_polyline,
	modest_style_default_declaration_by_html_node_radialGradient,
	modest_style_default_declaration_by_html_node_rect,
	modest_style_default_declaration_by_html_node_set,
	modest_style_default_declaration_by_html_node_stop,
	modest_style_default_declaration_by_html_node_switch,
	modest_style_default_declaration_by_html_node_symbol,
	modest_style_default_declaration_by_html_node_text,
	modest_style_default_declaration_by_html_node_textPath,
	modest_style_default_declaration_by_html_node_tref,
	modest_style_default_declaration_by_html_node_tspan,
	modest_style_default_declaration_by_html_node_use,
	modest_style_default_declaration_by_html_node_view,
	modest_style_default_declaration_by_html_node_vkern,
	modest_style_default_declaration_by_html_node_math,
	modest_style_default_declaration_by_html_node_maction,
	modest_style_default_declaration_by_html_node_maligngroup,
	modest_style_default_declaration_by_html_node_malignmark,
	modest_style_default_declaration_by_html_node_menclose,
	modest_style_default_declaration_by_html_node_merror,
	modest_style_default_declaration_by_html_node_mfenced,
	modest_style_default_declaration_by_html_node_mfrac,
	modest_style_default_declaration_by_html_node_mglyph,
	modest_style_default_declaration_by_html_node_mi,
	modest_style_default_declaration_by_html_node_mlabeledtr,
	modest_style_default_declaration_by_html_node_mlongdiv,
	modest_style_default_declaration_by_html_node_mmultiscripts,
	modest_style_default_declaration_by_html_node_mn,
	modest_style_default_declaration_by_html_node_mo,
	modest_style_default_declaration_by_html_node_mover,
	modest_style_default_declaration_by_html_node_mpadded,
	modest_style_default_declaration_by_html_node_mphantom,
	modest_style_default_declaration_by_html_node_mroot,
	modest_style_default_declaration_by_html_node_mrow,
	modest_style_default_declaration_by_html_node_ms,
	modest_style_default_declaration_by_html_node_mscarries,
	modest_style_default_declaration_by_html_node_mscarry,
	modest_style_default_declaration_by_html_node_msgroup,
	modest_style_default_declaration_by_html_node_msline,
	modest_style_default_declaration_by_html_node_mspace,
	modest_style_default_declaration_by_html_node_msqrt,
	modest_style_default_declaration_by_html_node_msrow,
	modest_style_default_declaration_by_html_node_mstack,
	modest_style_default_declaration_by_html_node_mstyle,
	modest_style_default_declaration_by_html_node_msub,
	modest_style_default_declaration_by_html_node_msup,
	modest_style_default_declaration_by_html_node_msubsup
};



#endif /* MODEST_STYLE_DEFAULT_RESOURCES_H */
