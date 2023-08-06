#!/usr/bin/env python
"""Unit tests for the CNVkit library, cnvlib."""
import unittest
from glob import glob

import logging
logging.basicConfig(level=logging.ERROR, format="%(message)s")

# unittest/pomegranate 0.10.0: ImportWarning: can't resolve package from
# __spec__ or __package__, falling back on __name__ and __path__
import warnings
warnings.filterwarnings('ignore', category=ImportWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

import numpy as np
from skgenome import tabio

import cnvlib
# Import all modules as a smoke test
from cnvlib import (access, antitarget, autobin, batch, bintest, cnary,
                    commands, core, coverage, diagram, export, fix, import_rna,
                    importers, metrics, params, plots, reference, reports,
                    segmentation, segmetrics, smoothing, vary)


class CommandTests(unittest.TestCase):
    """Tests for top-level commands."""

    def test_rna_counts(self):
        """The 'import-rna' command."""
        corr_fname = "../data/tcga-skcm.cnv-expr-corr.tsv"
        gene_info_fname = "../data/ensembl-gene-info.hg38.tsv"
        count_fnames = glob("../../cnvkit-examples/rna/tcga-rna-counts/*.txt")
        # Gene count inputs
        all_data, cnrs = commands.do_import_rna(
            count_fnames,
            "counts",
            gene_info_fname,
            correlations_fname=corr_fname,
            #normal_fnames=(),
            #do_gc=True, do_txlen=True, max_log2=3,
        )
        cnrs = list(cnrs)
        self.assertGreater(len(all_data), 0)
        self.assertEqual(len(count_fnames), len(cnrs))
        c = cnrs[0]
        self.assertGreater(c.log2.std(), 0.1)

    def test_rna(self):
        """The 'import-rna' command."""
        corr_fname = "../data/tcga-skcm.cnv-expr-corr.tsv"
        gene_info_fname = "../data/ensembl-gene-info.hg38.tsv"
        count_fnames = glob("../../cnvkit-examples/rna/tcga-rna-counts/*.txt")
        # Gene count inputs
        all_data, cnrs = commands.do_import_rna(
            count_fnames,
            "counts",
            gene_info_fname,
            correlations_fname=corr_fname,
            #normal_fnames=(),
            #do_gc=True, do_txlen=True, max_log2=3,
        )
        cnrs = list(cnrs)
        self.assertGreater(len(all_data), 0)
        self.assertEqual(len(count_fnames), len(cnrs))
        c = cnrs[0]
        self.assertGreater(c.log2.std(), 0.1)

        # RSEM inputs
        # TODO



def linecount(filename):
    i = -1
    with open(filename) as handle:
        for i, _line in enumerate(handle):
            pass
        return i + 1


if __name__ == '__main__':
    unittest.main(verbosity=2)
