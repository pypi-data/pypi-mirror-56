#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import sys
import os
import click
from src.click_context import cli
import time
from src.pairwise.virtualQs_class import virtualQs

# TODO use logging instead of normal prints.
# TODO check best practices for sqlite for enhancements
# TODO refactor the whole code to multiple classes
# TODO add validation callbacks for click


@cli.command(name = "pairwise", help_priority=2)
@click.option('-m','--min-q', 'min_q', required=False, type=click.INT, default = 5, show_default=True, help="minimum virtualQ")
@click.option('-M','--max-q', 'max_q', required=False, type=click.INT, default = -1, help="maximum virtualQ")
@click.option('-s','--step-q', 'step_q', required=False, type=click.INT, default = 2, show_default=True,  help="virtualQs range step")
@click.option('-i', '--index-prefix', required=True, type=click.STRING, help="kProcessor index file prefix")
@click.option('-o', '--output-prefix', required=False, type=click.STRING, default=None, help="virtualQs output file(s) prefix")
@click.option('--force','force_write', is_flag=True, help="Overwrite the already proessed virtualQs")
@click.option('--backup', is_flag=True, help="Back up old virtualQs")
@click.option('--export-colors', required=False, type=click.Choice(['json', 'pickle']), default=None, help="export supercolors data [debugging purposes]")
@click.pass_context
def main(ctx, min_q, max_q, step_q, index_prefix, output_prefix, force_write, backup, export_colors):
    """
    Generating pairwise  matrices for single/multiple virtualQs.
    """
    if not os.path.isfile(index_prefix + ".map") and not os.path.isfile(index_prefix + ".mqf"):
        print(f"Index prefix {index_prefix} Does not exist!", file = sys.stderr)
        sys.exit(1)

    if not output_prefix:
        output_prefix = os.path.basename(index_prefix)

    t1 = time.time()
    VQ = virtualQs(logger_obj = ctx.obj, index_prefix=index_prefix)
    index_loading_time = time.time() - t1
    ctx.obj.INFO(f"index_loading_time : {index_loading_time} sec")

    VQ.set_params(minQ=min_q, maxQ=max_q, stepQ=step_q)
    VQ.sqlite_initiate(output_prefix, force_write, backup)

    iteration_time = time.time()

    it = VQ.kf.begin()
    prev_kmer = it.getHashedKmer()
    prev_kmer_color = it.getKmerCount()

    super_color_time = 0
    matching_mask_time = 0
    list_appending_time = 0
    dict_updating_time = 0
    dict_inserting_time = 0
    colors_remove_time = 0

    next_kmer_time = 0
    applying_xor_time = 0

    get_it_data = 0

    # Iterate over all kmers.
    while it != VQ.kf.end():
        t1 = time.time()
        it.next()
        next_kmer_time += time.time() - t1

        t1 = time.time()
        curr_kmer = it.getHashedKmer()
        curr_kmer_color = it.getKmerCount()
        get_it_data += time.time() - t1

        # Apply XOR to kmer1 and kmer2 (single time per iteration)
        t1 = time.time()
        xor = prev_kmer ^ curr_kmer
        applying_xor_time += time.time() - t1

        # Apply all masks with all Qs
        for Q, MASK in VQ.masks.items():

            # True if there's match, False if not
            t1 = time.time()
            matched = not bool(xor & MASK)
            matching_mask_time += time.time() - t1

            if matched:
                t1 = time.time()
                VQ.temp_superColors[Q] += [prev_kmer_color, curr_kmer_color]
                dict_updating_time += time.time() - t1

            else:
                t1 = time.time()
                VQ.temp_superColors[Q].append(prev_kmer_color)
                list_appending_time += time.time() - t1
                t1 = time.time()
                super_color_id = VQ.create_super_color(VQ.temp_superColors[Q])
                super_color_time += time.time() - t1

                # print("Matching Q%d %s & %s | FALSE | [prevC:%d, currC=%d]" % (Q, VQ.int_to_str(
                #     prev_kmer, VQ.kSize), VQ.int_to_str(curr_kmer, VQ.kSize),  prev_kmer_color, curr_kmer_color))


                # Check if the superColor already exist
                # If yes: increment the count to one
                # If No:  Insert the new superColor and set the count to 1
                if super_color_id not in VQ.superColors[Q]:
                    t1 = time.time()
                    VQ.superColors[Q][super_color_id] = list(set(VQ.temp_superColors[Q]))
                    VQ.superColorsCount[Q][super_color_id] = 1
                    dict_inserting_time += time.time() - t1

                else:
                    # IF the supercolor already exist, just increment it
                    t1 = time.time()
                    VQ.superColorsCount[Q][super_color_id] += 1
                    dict_updating_time += time.time() - t1

                t1 = time.time()
                VQ.temp_superColors[Q] = [curr_kmer_color]
                dict_inserting_time += time.time() - t1

        prev_kmer = curr_kmer
        prev_kmer_color = curr_kmer_color

    # If the last iteration got a match, push it to the superColors

    for Q, colors in VQ.temp_superColors.items():
        t1 = time.time()
        colors.remove(curr_kmer_color)
        colors_remove_time += time.time() - t1

        if not len(colors):
            continue

        t1 = time.time()
        super_color_id = VQ.create_super_color(colors)
        super_color_time += time.time() - t1

        if super_color_id not in VQ.superColors[Q]:
            t1 = time.time()
            VQ.superColors[Q][super_color_id] = list(set(colors))
            VQ.superColorsCount[Q][super_color_id] = 1
            dict_inserting_time += time.time() - t1

        else:
            # IF the supercolor already exist, just increment it
            t1 = time.time()
            VQ.superColorsCount[Q][super_color_id] += 1
            dict_updating_time += time.time() - t1

    ctx.obj.INFO(f"Main Iteration {time.time() - iteration_time} seq")

    # Save all Qs to files.
    if export_colors:
        _dir_name = os.path.dirname(output_prefix) 
        if not os.path.isdir(_dir_name):
            os.mkdir(_dir_name)

        for Q in VQ.mainQs:
            VQ.export_superColors(output_prefix, Q, export_colors)

    # Construct pairwise matrices
    pairwise_time = time.time()
    VQ.pairwise()
    ctx.obj.INFO(f"Pairwise {time.time() - pairwise_time} sec")
    # export pairwise matrices
    VQ.export_pairwise()

    ctx.obj.INFO(f"create_super_class : {super_color_time} sec")
    ctx.obj.INFO(f"dict_inserting_time : {dict_inserting_time} sec")
    ctx.obj.INFO(f"colors_remove_time : {colors_remove_time} sec")
    ctx.obj.INFO(f"dict_updating_time : {dict_updating_time} sec")
    ctx.obj.INFO(f"list_appending_time : {list_appending_time} sec")
    ctx.obj.INFO(f"matching_mask_time : {matching_mask_time} sec")
    ctx.obj.INFO(f"next_kmer_time : {next_kmer_time} sec")
    ctx.obj.INFO(f"applying_xor_time : {applying_xor_time} sec")