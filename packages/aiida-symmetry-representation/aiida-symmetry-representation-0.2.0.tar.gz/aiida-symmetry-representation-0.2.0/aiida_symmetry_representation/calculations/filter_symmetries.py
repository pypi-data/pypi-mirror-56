# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

from fsc.export import export
from pymatgen.io.cif import CifWriter

from aiida.engine import CalcJob
from aiida.plugins import DataFactory
from aiida.common import CalcInfo, CodeInfo


@export
class FilterSymmetriesCalculation(CalcJob):
    """
    Calculation class to run the ``symmetry-repr filter_symmetries`` command.
    """

    _OUTPUT_FILE_NAME = 'symmetries_out.hdf5'

    @classmethod
    def define(cls, spec):
        super(FilterSymmetriesCalculation, cls).define(spec)

        spec.input(
            'symmetries',
            valid_type=DataFactory('singlefile'),
            help="File containing the symmetries (in HDF5 format)."
        )
        spec.input(
            'structure',
            valid_type=DataFactory('structure'),
            help=
            "Structure with which the filtered symmetries should be compatible."
        )

        spec.input(
            'metadata.options.parser_name',
            valid_type=str,
            default='symmetry_representation.symmetry'
        )

        spec.output(
            'symmetries',
            valid_type=DataFactory('singlefile'),
            help=
            'The HDF5 file containing the symmetries which are compatible with the structure.'
        )

    def prepare_for_submission(self, tempfolder):  # pylint: disable=arguments-differ

        struc_filename = 'lattice.cif'

        with tempfolder.open(struc_filename, 'w') as handle:
            handle.write(
                str(CifWriter(struct=self.inputs.structure.get_pymatgen()))
            )
        symmetries_filename = 'symmetries.hdf5'
        local_symmetries_file = self.inputs.symmetries

        calcinfo = CalcInfo()
        calcinfo.uuid = self.uuid
        calcinfo.remote_copy_list = []
        calcinfo.local_copy_list = [(
            local_symmetries_file.uuid, local_symmetries_file.filename,
            symmetries_filename
        )]
        calcinfo.retrieve_list = [self._OUTPUT_FILE_NAME]

        codeinfo = CodeInfo()
        codeinfo.cmdline_params = [
            'filter-symmetries', '-s', symmetries_filename, '-l',
            struc_filename, '-o', self._OUTPUT_FILE_NAME
        ]
        codeinfo.stdout_name = self._OUTPUT_FILE_NAME
        codeinfo.code_uuid = self.inputs.code.uuid
        calcinfo.codes_info = [codeinfo]

        return calcinfo
