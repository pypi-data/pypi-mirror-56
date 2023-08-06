"""toil_caveman commands."""

from glob import glob
from os.path import join
import os
import subprocess
import tempfile
from copy import deepcopy

from toil.common import Toil
from toil_container import ContainerArgumentParser
from toil_container import ContainerJob
from toil_cvflag.commands import CavemanFlagging
from toil_cvflag.commands import ConcatVcfs
from toil_cvflag.commands import split_vcf

from toil_caveman import __version__

ARGUMENTS = [
    "annot-bed-files",
    "species-assembly",
    "flag-bed-files",
    "flagConfig",
    "flagToVcfConfig",
    "germline-indel",
    "ignore-file",
    "norm-cn-default",
    "normal-bam",
    "normal-cn",
    "normal-contamination",
    "normal-protocol",
    "outdir",
    "reference",
    "seqType",
    "species",
    "tum-cn-default",
    "tumour-bam",
    "tumour-cn",
    "tumour-protocol",
    "unmatched-vcf",
]


class CavemanCommand(ContainerJob):
    def __init__(self, options, memory="5G", **kwargs):
        """All steps are short low memory jobs unless otherwise specified."""
        super(CavemanCommand, self).__init__(
            memory=options.max_memory_usage or memory,
            options=options,
            cores=kwargs.pop("cores", 1),
            runtime=kwargs.pop("runtime", options.short_job),
            **kwargs
        )


class StepRunner(CavemanCommand):
    def __init__(self, process, options, index=1, **kwargs):
        """
        Add the caveman process and index as attributes.

        Arguments:
            kwargs (dict): extra ContainerJob key word arguments.
            process (str): see caveman.pl --help.
            index (int): caveman process index.
            options (object): caveman process index.
        """
        self.process = process
        self.index = index
        super(StepRunner, self).__init__(
            unitName="Caveman%s %s" % (process.capitalize(), index),
            displayName="Caveman%s" % process.capitalize(),
            options=options,
            **kwargs
        )

    def run(self, fileStore):
        cmd = [
            "caveman.pl",
            "-process",
            self.process,
            "-index",
            self.index,
            "-threads",
            self.cores,
            "-logs",
            join(self.options.outdir, "clogs"),
        ]

        for i in ARGUMENTS:
            value = getattr(self.options, i.replace("-", "_"), None)
            if value:
                cmd += ["-" + i, value]

        # run the command and allow file system to register output files
        cmd = list(map(str, cmd))
        self.call(cmd, cwd=self.options.outdir)

        if self.process == "add_ids":
            vcf = glob(join(self.options.outdir, "tmpCaveman", "*.muts.ids.vcf"))
            assert (
                len(vcf) == 1
            )  # check if only one {tumor_id}_vs_{normal_id}.muts.ids.vcf
            vcf = vcf[0]

            bgzip_cmd = ["bgzip", vcf]
            self.call(bgzip_cmd)


class Flag(CavemanCommand):
    def run(self, fileStore):
        self.options.vcf = glob(
            join(self.options.outdir, "tmpCaveman", "*muts.ids.vcf.gz")
        )[0]
        splitted_vcfs, expected_num_file = split_vcf(self.options)

        fileStore.logToMaster(
            "Split into {} vcfs, temp_dir is {}".format(
                expected_num_file, self.options.working_dir
            )
        )

        for vcf in splitted_vcfs:
            options = deepcopy(self.options) # change vcf on a copy of the self.options
            options.vcf = vcf
            options.reference = self.options.reference.replace(".fai", "")
            self.addChild(CavemanFlagging(options=options))

        self.options.vcfs = splitted_vcfs
        concat_vcf = ConcatVcfs(options=self.options)
        self.addFollowOn(concat_vcf)


class Split(CavemanCommand):
    def run(self, fileStore):
        with open(self.options.reference) as f:
            for ix, i in enumerate(f):
                if i.strip():
                    self.addChild(
                        StepRunner(process="split", index=ix + 1, options=self.options)
                    )


class RemoveContigs(CavemanCommand):
    def run(self, fileStore):
        tmpdir = join(self.options.outdir, "tmpCaveman")
        delete = list(glob(join(tmpdir, "splitList.GL*")))
        delete.extend(glob(join(tmpdir, "splitList.hs*")))
        delete.extend(glob(join(tmpdir, "splitList.MT")))
        delete.extend(glob(join(tmpdir, "splitList.NC*")))

        for i in delete:
            try:
                os.remove(i)
            except:  # pylint: disable=W0702
                pass


class SplitRunner(CavemanCommand):
    def __init__(self, process, **kwargs):
        self.process = process
        super(SplitRunner, self).__init__(**kwargs)

    def split_list_range(self):
        with open(join(self.options.outdir, "tmpCaveman", "splitList")) as f:
            count = 0
            for i in f:
                if i.strip():
                    count += 1
                    yield count

    def run(self, fileStore):
        for i in self.split_list_range():
            self.addChild(
                StepRunner(process=self.process, index=i, options=self.options)
            )


def run_toil(options):
    """Toil implementation for cgpCaveman."""
    cvflag_options = add_cvflag_options(options)

    setup = StepRunner(process="setup", options=options)
    split = Split(options=options)
    remove = RemoveContigs(options=options)
    concat = StepRunner(process="split_concat", options=options)
    mstep = SplitRunner(process="mstep", options=options)
    merge = StepRunner(process="merge", options=options)
    estep = SplitRunner(process="estep", options=options)
    results = StepRunner(process="merge_results", options=options)
    add_ids = StepRunner(process="add_ids", options=options)
    flag = Flag(options=cvflag_options)

    # build dag
    setup.addFollowOn(split)
    split.addFollowOn(remove)
    remove.addFollowOn(concat)
    concat.addFollowOn(mstep)
    mstep.addFollowOn(merge)
    merge.addFollowOn(estep)
    estep.addFollowOn(results)
    results.addFollowOn(add_ids)
    add_ids.addFollowOn(flag)

    with Toil(options) as pipe:
        if not pipe.options.restart:
            pipe.start(setup)
        else:
            pipe.restart()


def add_cvflag_options(options):
    """Add the toil_cvflag specific options to existing options."""
    tumor_id = os.path.basename(options.tumour_bam).strip(".bam")
    normal_id = os.path.basename(options.normal_bam).strip(".bam")
    toil_cvflag_args = {
        'out': join(
            options.outdir, '%s_vs_%s.flagged.muts.vcf.gz' % (tumor_id, normal_id)
        ),
        'tumor_bam': options.tumour_bam,
        'bedFileLoc': options.flag_bed_files,
        'indelBed': options.germline_indel,
        'unmatchedVCFLoc': options.unmatched_vcf,
        'annoBedLoc': options.annot_bed_files,
        'sequencing_method': "TGD" if options.seqType in "pulldown" else "WGS",
        'bin_size': options.bin_size
    }

    for key, value in toil_cvflag_args.items():
        setattr(options, key, value)

    return options


def get_parser():
    """Get pipeline configuration using toil's argparse."""
    parser = ContainerArgumentParser(version=__version__)
    parser.description = "Run toil_caveman pipeline."
    settings = parser.add_argument_group("See caveman.pl --help.")

    for i in ARGUMENTS:
        settings.add_argument("--" + i, required=False, default=None)

    settings.add_argument(
        "--max_memory_usage", help="max ram usage e.g. 1G, 1000M", default=None
    )

    settings.add_argument(
        "--short_job", help="runtime of short jobs", default=90, required=False
    )

    settings.add_argument(
        "--tgd", help="request less resources for targeted data", action="store_true"
    )

    settings.add_argument(
        "--bin-size",
        help=(
            "Number of variants in a splitted vcf file in caveman flagging."
            "if bin_size > variants in input vcf, no parallization is applied."
        ),
        default=100000,
        type=int,
        required=False,
    )

    return parser


def process_parsed_options(options):
    """Process parsed options."""
    options.working_dir = temp = tempfile.mkdtemp()
    if not os.path.isdir(temp):
        subprocess.check_call(["mkdir", "-p", temp])

    validate_bam(options.tumour_bam)
    validate_bam(options.normal_bam)
    validate_reference(options.reference)

    if options.writeLogs is not None:
        subprocess.check_call(["mkdir", "-p", options.writeLogs])

    return options


def main():
    """Parse options and run toil."""
    options = get_parser().parse_args()
    options = process_parsed_options(options=options)
    run_toil(options)


def validate_reference(value):
    """Make sure the passed reference has an index file."""
    value = os.path.abspath(value)

    if not value.endswith(".fai"):
        raise Exception(value + " must end in .fai.")

    return value


def validate_bam(value):
    """Make sure the passed bam has an index file."""
    value = os.path.abspath(value)
    index = str(value) + ".bai"

    if not os.path.isfile(index):
        raise Exception(index + " should be an existing file.")

    return value
