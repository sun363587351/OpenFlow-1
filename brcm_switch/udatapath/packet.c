/* Copyright (c) 2011, TrafficLab, Ericsson Research, Hungary
 * Copyright (c) 2012, CPqD, Brazil
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 *   * Redistributions of source code must retain the above copyright notice,
 *     this list of conditions and the following disclaimer.
 *   * Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *   * Neither the name of the Ericsson Research nor the names of its
 *     contributors may be used to endorse or promote products derived from
 *     this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 */

#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <sys/types.h>
#include "datapath.h"
#include "dp_buffers.h"
#include "packet.h"
#include "packets.h"
#include "action_set.h"
#include "ofpbuf.h"
#include "oflib/ofl-structs.h"
#include "oflib/ofl-print.h"
#include "util.h"


struct packet *
packet_create(struct datapath *dp, unsigned int in_port,
    struct ofpbuf *buf, bool packet_out) {
    struct packet *pkt;

    pkt = xmalloc(sizeof(struct packet));

    pkt->dp         = dp;
    pkt->buffer     = buf;
    pkt->in_port    = in_port;
    pkt->action_set = action_set_create(dp->exp);
    pkt->action_set_apply= action_set_create(dp->exp);
    pkt->alta_supported = true;

    pkt->packet_out       = packet_out;
    pkt->out_group        = OFPG_ANY;
    pkt->out_port         = OFPP_ANY;
    pkt->out_port_max_len = 0;
    pkt->out_queue        = 0;
    pkt->buffer_id        = OFP_NO_BUFFER;
    pkt->table_id         = 0;
    pkt->reason           = 0;

    pkt->mis_match_entry_hited = false;
    pkt->l3_options = L3_OPTION_NONE;

    pkt->handle_std = packet_handle_std_create(pkt);
    return pkt;
}

struct packet *
packet_clone(struct packet *pkt) {
    struct packet *clone;

    clone = xmalloc(sizeof(struct packet));
    if (NULL == clone) {
        return NULL;
    }

    clone->dp         = pkt->dp;
    clone->buffer     = ofpbuf_clone(pkt->buffer);
    clone->in_port    = pkt->in_port;
    clone->action_set = action_set_clone(pkt->action_set);
    clone->action_set_apply = action_set_clone(pkt->action_set_apply);
    clone->alta_supported = pkt->alta_supported;

    clone->packet_out       = pkt->packet_out;
    clone->out_group        = OFPG_ANY;
    clone->out_port         = OFPP_ANY;
    clone->out_port_max_len = pkt->out_port_max_len;
    clone->out_queue        = 0;
    clone->buffer_id        = OFP_NO_BUFFER; // the original is saved in buffer,
                                             // but this buffer is a copy of that,
                                             // and might be altered later
    clone->table_id         = pkt->table_id;

    clone->handle_std = packet_handle_std_clone(clone, pkt->handle_std);

    return clone;
}

void
packet_destroy(struct packet *pkt) {
    /* If packet is saved in a buffer, do not destroy it,
     * if buffer is still valid */
     
    if (pkt->buffer_id != OFP_NO_BUFFER) {
        if (dp_buffers_is_alive(pkt->dp->buffers, pkt->buffer_id)) {
            return;
        } else {
            dp_buffers_discard(pkt->dp->buffers, pkt->buffer_id, false);
        }
    }

    action_set_destroy(pkt->action_set);
    action_set_destroy(pkt->action_set_apply);
    ofpbuf_delete(pkt->buffer);
    packet_handle_std_destroy(pkt->handle_std);
    free(pkt);
    pkt = NULL;
}


void
packet_match_reset(struct packet *pkt)
{
	packet_handle_std_destroy(pkt->handle_std);
	pkt->handle_std = packet_handle_std_create(pkt);
}


char *
packet_to_string(struct packet *pkt) {
    char *str;
    size_t str_size;
    FILE *stream = open_memstream(&str, &str_size);

    fprintf(stream, "pkt{in=\"");
    ofl_port_print(stream, pkt->in_port);
    fprintf(stream, "\", actset=");
    action_set_print(stream, pkt->action_set);
    fprintf(stream, ", pktout=\"%u\", ogrp=\"", pkt->packet_out);
    ofl_group_print(stream, pkt->out_group);
    fprintf(stream, "\", oprt=\"");
    ofl_port_print(stream, pkt->out_port);
    fprintf(stream, "\", buffer=\"");
    ofl_buffer_print(stream, pkt->buffer_id);
    fprintf(stream, "\", std=");
    //packet_handle_std_print(stream, pkt->handle_std);
    fprintf(stream, "}");

    fclose(stream);
    return str;
}
