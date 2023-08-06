#!/usr/bin/env python
"""
Module containing the tools for plotting of results
"""
from __future__ import division, print_function

import matplotlib

matplotlib.use("agg")  # noqa
from bilby.gw.result import CBCResult

from .utils import DataDump, parse_args, get_command_line_arguments, logger
from .bilbyargparser import BilbyArgParser


def create_parser():
    """ Generate a parser for the plot script

    Returns
    -------
    parser: BilbyArgParser
        A parser with all the default options already added

    """
    parser = BilbyArgParser(ignore_unknown_config_file_keys=True)
    parser.add("--result", type=str, required=True, help="The result file")
    parser.add("--skymap", action="store_true", help="Generate skymap")
    parser.add("--waveform", action="store_true", help="Generate waveform")
    return parser


def main():
    """ Top-level interface for bilby_pipe """
    args, unknown_args = parse_args(get_command_line_arguments(), create_parser())

    logger.info("Generating plots for results file {}".format(args.result))

    result = CBCResult.from_json(args.result)
    data_dump = DataDump.from_pickle(result.meta_data["data_dump"])
    outdir = result.outdir
    label = result.label

    if args.skymap:
        logger.info("Generating skymap")
        try:
            result.plot_skymap(maxpts=2000)
        except Exception as e:
            logger.info("Unable to generate skymap: error {}".format(e))

    logger.info("Plotting 1d posteriors")
    result.plot_marginals(priors=True)
    logger.info("Generating intrinsic parameter corner")
    result.plot_corner(
        [
            "mass_1_source",
            "mass_2_source",
            "chirp_mass_source",
            "mass_ratio",
            "chi_eff",
            "chi_p",
        ],
        filename="{}/{}_intrinsic_corner.png".format(outdir, label),
    )
    logger.info("Generating distance sky time corner")
    result.plot_corner(
        ["luminosity_distance", "redshift", "theta_jn", "ra", "dec", "geocent_time"],
        filename="{}/{}_extrinsic_corner.png".format(outdir, label),
    )
    logger.info("Generating calibration posterior")
    result.plot_calibration_posterior()
    if args.waveform:
        logger.info("Generating waveform posterior")
        result.plot_waveform_posterior(
            interferometers=data_dump.interferometers, n_samples=500, format="pdf"
        )
