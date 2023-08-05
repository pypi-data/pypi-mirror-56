# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

from fsc.export import export

from aiida.plugins import DataFactory
from aiida.parsers.parser import Parser

from ..calculations.filter_symmetries import FilterSymmetriesCalculation


@export
class SymmetriesParser(Parser):
    """
    Parses a symmetries file to an output file in ``symmetry-representation`` HDF5 format.

    Returns
    -------
    symmetries : aiida.orm.nodes.data.singlefile.SinglefileData
        Output symmetries file.
    """
    def parse(self, **kwargs):
        try:
            out_folder = self.retrieved
        except KeyError as e:
            self.logger.error("No retrieved folder found")
            raise e

        # Note: If we want to extend this to other calculations which might not
        # use the same output file name, it might be better to pass the filename
        # through the 'options' inputs.
        with (
            out_folder.open(
                FilterSymmetriesCalculation._OUTPUT_FILE_NAME,  # pylint: disable=protected-access
                'rb'
            )
        ) as handle:
            sym_file = DataFactory('singlefile')(file=handle)
        self.out('symmetries', sym_file)
