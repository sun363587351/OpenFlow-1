/* Copyright (c) 2012, Applistar, Vietnam
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
 *
 * Author: Thanh Le Dinh, Khai Nguyen Dinh <thanhld, khaind@applistar.com>
 */

#include <sys/types.h>
#include "compiler.h"
#include "meter_table.h"
#include "datapath.h"
#include "dp_actions.h"
#include "hmap.h"
#include "list.h"
#include "packet.h"
#include "util.h"
#include "openflow/openflow.h"
#include "oflib/ofl.h"
#include "oflib/ofl-messages.h"

#include "vlog.h"
#define LOG_MODULE VLM_meter_t

static struct vlog_rate_limit rl = VLOG_RATE_LIMIT_INIT(60, 60);

int alta_policer_entry_remove(int policer_id);
int alta_policer_entry_modify(struct datapath *dp,int policer_id);

/* Creates a meter table. */
struct meter_table *
meter_table_create(struct datapath *dp) {
    struct meter_table *table;

    table = xmalloc(sizeof(struct meter_table));
    table->dp = dp;
    table->entries_num = 0;
    hmap_init(&table->meter_entries);

    table->features = xmalloc(sizeof(struct ofl_meter_features));
    table->features->max_meter = DEFAULT_MAX_METER;
    table->features->max_bands = DEFAULT_MAX_BAND_PER_METER;
    table->features->max_color = DEFAULT_MAX_METER_COLOR;
    table->features->capabilities = OFPMF_KBPS ;  /* Rate value in kb/s (kilo-bit per second).
                                                                Do burst size. Collect statistics.*/
    table->features->band_types = 1;

    table->features->band_types = OFPMBT_DROP | OFPMBT_DSCP_REMARK;
    return table;
}

void
meter_table_destroy(struct meter_table *table) {
    struct meter_entry *entry, *next;

    HMAP_FOR_EACH_SAFE(entry, next, struct meter_entry, node, &table->meter_entries) {
        meter_entry_destroy(entry);
    }

    free(table);
}

struct meter_entry *
meter_table_find(struct meter_table *table, unsigned int meter_id) {
    struct hmap_node *hnode;
    if(0 == table->entries_num)
    {
    	return NULL;
    }

    hnode = hmap_first_with_hash(&table->meter_entries, meter_id);

    if (hnode == NULL) {
        return NULL;
    }

    return CONTAINER_OF(hnode, struct meter_entry, node);
}



void
meter_table_apply(struct meter_table *table, struct packet **packet, unsigned int meter_id) {
    struct meter_entry *entry;

    entry = meter_table_find(table, meter_id);
    table->dp->m_entry = entry;

    if (entry == NULL)
    {
        return;
    }

    meter_entry_apply(entry, packet);
}


static ofl_err
meter_table_add(struct meter_table *table, struct ofl_msg_meter_mod *mod) {

    struct meter_entry *entry;
    size_t i;

    if (hmap_first_with_hash(&table->meter_entries, mod->meter_id) != NULL) {
        return ofl_error(OFPET_METER_MOD_FAILED, OFPMMFC_METER_EXISTS);
    }

    if (table->entries_num >= DEFAULT_MAX_METER) {
        return ofl_error(OFPET_METER_MOD_FAILED, OFPMMFC_OUT_OF_METERS);
    }

    if (table->bands_num + mod->meter_bands_num > METER_TABLE_MAX_BANDS) {
        return ofl_error(OFPET_METER_MOD_FAILED, OFPMMFC_OUT_OF_BANDS);
    }
    for(i = 0; i < mod->meter_bands_num; i++)
    {
        if(((mod->flags & OFPMF_KBPS) || (mod->flags & OFPMF_PKTPS)) && !(mod->bands[i]->rate))
        {
            return ofl_error(OFPET_METER_MOD_FAILED, OFPMMFC_BAD_RATE);
        }
        if((mod->flags & OFPMF_BURST) && !(mod->bands[i]->burst_size))
        {
            return ofl_error(OFPET_METER_MOD_FAILED, OFPMMFC_BAD_BURST);
        }
    }

    entry = meter_entry_create(table->dp, table, mod);

    hmap_insert(&table->meter_entries, &entry->node, entry->stats->meter_id);

    table->entries_num++;
    table->bands_num += entry->stats->meter_bands_num;
    ofl_msg_free_meter_mod(mod, false);
    return 0;
}

static ofl_err
meter_table_modify(struct meter_table *table, struct ofl_msg_meter_mod *mod) {
    struct meter_entry *entry, *new_entry;

    entry = meter_table_find(table, mod->meter_id);
    if (entry == NULL) {
        return ofl_error(OFPET_METER_MOD_FAILED, OFPMMFC_UNKNOWN_METER);
    }

    if (table->bands_num - entry->config->meter_bands_num + mod->meter_bands_num > METER_TABLE_MAX_BANDS) {
        return ofl_error(OFPET_METER_MOD_FAILED, OFPMMFC_OUT_OF_BANDS);
    }

    new_entry = meter_entry_create(table->dp, table, mod);

    hmap_remove(&table->meter_entries, &entry->node);
    hmap_insert_fast(&table->meter_entries, &new_entry->node, mod->meter_id);

    table->bands_num = table->bands_num - entry->config->meter_bands_num + new_entry->stats->meter_bands_num;


    new_entry->modify_time = time_now_msec();

    list_replace(&new_entry->flow_refs, &entry->flow_refs);
    list_init(&entry->flow_refs);

    memset(&new_entry->dp->pol_config,0,sizeof(struct policer_config));
    alta_policer_entry_modify(table->dp,mod->meter_id);

    meter_entry_destroy2(entry,new_entry);
    ofl_msg_free_meter_mod(mod, false);
    return 0;
}

static ofl_err
meter_table_delete(struct meter_table *table, struct ofl_msg_meter_mod *mod) {
    if (mod->meter_id == OFPM_ALL) {
        struct meter_entry *entry, *next;

        HMAP_FOR_EACH_SAFE(entry, next, struct meter_entry, node, &table->meter_entries)
        {
            alta_policer_entry_remove(entry->stats->meter_id);
            meter_entry_destroy(entry);
        }
        hmap_destroy(&table->meter_entries);
        hmap_init(&table->meter_entries);

        table->entries_num = 0;
        table->bands_num = 0;
        ofl_msg_free_meter_mod(mod, false);
        return 0;

    } else {
        struct meter_entry *entry;

        entry = meter_table_find(table, mod->meter_id);

        if (entry != NULL)
        {
            table->entries_num--;
            table->bands_num -= entry->stats->meter_bands_num;

            alta_policer_entry_remove(entry->stats->meter_id);

            hmap_remove(&table->meter_entries, &entry->node);

            meter_entry_destroy(entry);
        }
        ofl_msg_free_meter_mod(mod, false);
        return 0;
    }
}

ofl_err
meter_table_handle_meter_mod(struct meter_table *table, struct ofl_msg_meter_mod *mod,
                                                          const struct sender *sender) {
    if(sender->remote->role == OFPCR_ROLE_SLAVE)
        return ofl_error(OFPET_BAD_REQUEST, OFPBRC_IS_SLAVE);

    switch (mod->command) {
        case (OFPMC_ADD): {
            return meter_table_add(table, mod);
        }
        case (OFPMC_MODIFY): {
            return meter_table_modify(table, mod);
        }
        case (OFPMC_DELETE): {
            return meter_table_delete(table, mod);
        }
        default: {
            return ofl_error(OFPET_BAD_REQUEST, OFPBRC_BAD_TYPE);
        }
    }
}

ofl_err
meter_table_handle_stats_request_meter(struct meter_table *table,
                                  struct ofl_msg_multipart_meter_request *msg,
                                  const struct sender *sender UNUSED) {
    struct meter_entry *entry;
    size_t i = 0;

    if (msg->meter_id == OFPM_ALL) {
        entry = NULL;
    } else {
        entry = meter_table_find(table, msg->meter_id);

        if (entry == NULL) {
            return ofl_error(OFPET_METER_MOD_FAILED, OFPMMFC_UNKNOWN_METER);
        }
    }

    {
        struct ofl_msg_multipart_reply_meter reply =
                {{{.type = OFPT_MULTIPART_REPLY},
                  .type = OFPMP_METER, .flags = 0x0000},
                 .stats_num = msg->meter_id == OFPM_ALL ? table->entries_num : 1,
                 .stats     = xmalloc(sizeof(struct ofl_meter_stats *) * (msg->meter_id == OFPM_ALL ? table->entries_num : 1))
                };

        if (msg->meter_id == OFPM_ALL) {
            struct meter_entry *e;

            HMAP_FOR_EACH(e, struct meter_entry, node, &table->meter_entries) {
                 meter_entry_update(e);
                 alta_meter_entry_count(e);
                 if(e->stats->packet_in_count < 3000  && e->packet_count_bak>=3000 )
                 {
                     e->stats->packet_in_count = e->packet_count_bak;
                     e->stats->byte_in_count = e->byte_count_bak;
                 }
                 reply.stats[i] = e->stats;
                 i++;
             }

        } else {
            meter_entry_update(entry);
            alta_meter_entry_count(entry);
            if(entry->stats->packet_in_count < 3000 && entry->packet_count_bak >= 3000)
             {
                 entry->stats->packet_in_count = entry->packet_count_bak;
                 entry->stats->byte_in_count = entry->byte_count_bak;
                 for(i = 0;i < entry->stats->meter_bands_num;i++)
                {
                    entry->stats->band_stats[i]->packet_band_count = entry->stats->packet_in_count;
                    entry->stats->band_stats[i]->byte_band_count = entry->stats->byte_in_count;
                }
             }
            reply.stats[0] = entry->stats;
        }

        dp_send_message(table->dp, (struct ofl_msg_header *)&reply, sender);

        free(reply.stats);
        ofl_msg_free((struct ofl_msg_header *)msg, table->dp->exp);
        return 0;
    }
}

ofl_err
meter_table_handle_stats_request_meter_conf(struct meter_table *table,
                                  struct ofl_msg_multipart_meter_request *msg UNUSED,
                                  const struct sender *sender) {
    struct meter_entry *entry;

    if (msg->meter_id == OFPM_ALL)
    {
        entry = NULL;
    }
    else
    {
        entry = meter_table_find(table, msg->meter_id);

        if (entry == NULL)
        {
            return ofl_error(OFPET_METER_MOD_FAILED, OFPMMFC_UNKNOWN_METER);
        }
    }

    struct ofl_msg_multipart_reply_meter_conf reply =
            {{{.type = OFPT_MULTIPART_REPLY},
              .type = OFPMP_METER_CONFIG, .flags = 0x0000},
             .stats_num = table->entries_num,
             .stats     = xmalloc(sizeof(struct ofl_meter_config *) * (msg->meter_id == OFPM_ALL ? table->entries_num : 1))
            };

    if (msg->meter_id == OFPM_ALL)
    {
        struct meter_entry *e;
        size_t i = 0;

        HMAP_FOR_EACH(e, struct meter_entry, node, &table->meter_entries) {
            reply.stats[i] = e->config;
            i++;
        }

    } else {
        reply.stats[0] = entry->config;
    }

    dp_send_message(table->dp, (struct ofl_msg_header *)&reply, sender);

    free(reply.stats);
    ofl_msg_free((struct ofl_msg_header *)msg, table->dp->exp);
    return 0;
}

ofl_err
meter_table_handle_features_request(struct meter_table *table,
                                   struct ofl_msg_multipart_request_header *msg UNUSED,
                                  const struct sender *sender) {

    struct ofl_msg_multipart_reply_meter_features reply =
                                         {{{.type = OFPT_MULTIPART_REPLY},
                                             .type = OFPMP_METER_FEATURES, .flags = 0x0000},
                                             .features = table->features
                                         };
    dp_send_message(table->dp, (struct ofl_msg_header *)&reply, sender);
    ofl_msg_free((struct ofl_msg_header *)msg, table->dp->exp);
    return 0;

}

void
meter_table_add_tokens(struct meter_table *table){

    struct meter_entry *entry;
    HMAP_FOR_EACH(entry, struct meter_entry, node, &table->meter_entries){
        refill_bucket(entry);
    }

}

int alta_policer_entry_remove(int policer_id)
{
    return 0;
}

int alta_policer_entry_modify(struct datapath *dp,int policer_id)
{
    return 0;
}

