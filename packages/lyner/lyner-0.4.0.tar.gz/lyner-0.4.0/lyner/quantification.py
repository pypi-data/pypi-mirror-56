from functools import partial
from itertools import product
from string import Template
from subprocess import run, CompletedProcess
from sys import stderr
from typing import Tuple

LIBRARY_RELATIVE_ORIENTATION = ['I', 'O', 'M']  # inward, outward, matching
LIBRARY_STRANDEDNESS = ['S', 'U']  # stranded, unstranded
LIBRARY_STRAND_DIRECTION = ['F', 'R']  # forward, reverse

LIBRARY_TYPES = ["".join(p) for p in product(LIBRARY_RELATIVE_ORIENTATION, 'S', LIBRARY_STRAND_DIRECTION)] + \
                ["".join(p) for p in product(LIBRARY_RELATIVE_ORIENTATION, 'U')] + \
                ["U", "SF", "SR"]

INDEX = Template("$cmd index $input_option $input -k $k $output_option $output")
INDEX_CMDS = {
    'sailfish': Template(INDEX.safe_substitute(cmd="sailfish",
                                               input_option="-t",
                                               output_option="-o")),
    'salmon': Template(INDEX.safe_substitute(cmd="salmon",
                                             input_option="-t",
                                             output_option="-i")),
    # because i is for output-Index, apparently.
    'kallisto': Template(INDEX.safe_substitute(cmd="kallisto",
                                               input_option="",
                                               output_option="-i"))
}

QUANT = Template("$cmd quant -i $index $library_option $library $input1_option "
                 "$input1 $input2_option $input2 -o $output")
QUANT_CMDS = {
    'sailfish': Template(QUANT.safe_substitute(cmd="sailfish",
                                               input1_option="-1",
                                               input2_option="-2",
                                               library_option="-l")),
    'salmon': Template(QUANT.safe_substitute(cmd="salmon",
                                             input1_option="-1",
                                             input2_option="-2",
                                             library_option="-l")),
    'kallisto': Template(QUANT.safe_substitute(cmd="kallisto",
                                               input1_option="",
                                               input2_option="",
                                               library_option="",
                                               library=""))
}


def index(method: str, index_cmd: Template, reference_file: str, k: int = 31):
    output = f"{reference_file}.{method}.idx"
    from os.path import exists as path_exists
    if path_exists(output):
        return output
    cmd = index_cmd.substitute(input=reference_file, output=output, k=k)
    print(f"Indexing: `{cmd}`", file=stderr)
    cp: CompletedProcess = run([c for c in cmd.split(" ") if c])
    cp.check_returncode()
    return output


def quantify(method: str, quant_cmd: Template, index_file: str, r: Tuple[str, ...], library: str = ""):
    sample = guess_sample_name(r)
    if len(r) == 2:
        r1, r2 = r
    else:
        raise NotImplementedError(f"Single-end reads not yet supported. ({r})")
    output = f"{index_file}.{sample}"
    from os.path import exists as path_exists
    if not path_exists(output):
        cmd = quant_cmd.substitute(input1=' '.join(r1) if isinstance(r1, list) else r1,
                                   input2=' '.join(r2) if isinstance(r2, list) else r2,
                                   index=index_file,
                                   library=library,
                                   output=output)
        print(f"Quantification: `{cmd}`", file=stderr)
        cp: CompletedProcess = run([c for c in cmd.split(" ") if c])
        cp.check_returncode()

    abundance_dir = output
    quant_file = ""
    if method == "kallisto":
        quant_file = f"{abundance_dir}/abundance.tsv"
    elif method == "sailfish":
        raise NotImplementedError
    elif method == "salmon":
        raise NotImplementedError
    return quant_file, sample


def abundances(method: str, quant_file: str):
    from pandas import read_csv
    return read_csv(quant_file, sep='\t', index_col=0, header=0)


INDEX_QUANTIFY_ABUNDANCES = {method: (partial(index, method, INDEX_CMDS[method]),
                                      partial(quantify, method, QUANT_CMDS[method]),
                                      partial(abundances, method))
                             for method in ['kallisto', 'salmon', 'sailfish']}


def guess_sample_name(r: Tuple[str, ...]):
    if len(r) == 1:  # (r1,)
        return r[0].split('/')[-1].rstrip('.gz').rstrip('.fastq').rstrip('.fq')
    elif len(r) > 1:  # (r1, r2), (r1, r2, r3)
        rs = list(map(lambda x: guess_sample_name((x,)), r))
        sample = []
        if len({len(_) for _ in rs}) == 1:  # same length
            for x in zip(*rs):
                c = set(x)
                if len(c) != 1:
                    break
                sample.append(next(iter(c)))
        return ''.join(sample).rstrip('.') if sample else '_'.join(rs)
    else:
        raise ValueError(f"Unsupported read tuple: {r}.")

# from shutil import which
#
# QUANTIFICATION_METHODS = list(filter(which, ['kallisto', 'salmon', 'sailfish']))
#
#
# @rnax.command()
# @click.argument('reference', type=click.Path(exists=True, dir_okay=False, file_okay=True))
# @click.option('--reads1', '-r1', type=click.Path(exists=True, dir_okay=False, file_okay=True), multiple=True,
#               cls=MutexOption, mutually_exclusive=['samples'])
# @click.option('--reads2', '-r2', type=click.Path(exists=True, dir_okay=False, file_okay=True), multiple=True,
#               cls=MutexOption, mutually_exclusive=['samples'])
# @click.option('--samples', '-s', type=click.Path(exists=True, dir_okay=True, file_okay=False),
#               cls=MutexOption, mutually_exclusive=['reads1', 'reads2'])
# @click.option('--method', '-m',
#               type=click.Choice(QUANTIFICATION_METHODS),
#               default=None if not QUANTIFICATION_METHODS else QUANTIFICATION_METHODS[0])
# @click.option('--library', '-l', type=click.Choice(LIBRARY_TYPES + ['']), default='')
# @click.option('--jobs', '-j', type=click.INT, default=1)
# @pass_pipe
# @arggist
# def quantify(pipe: Pipe, reference, reads1, reads2, samples, method: str, library: str, jobs: int):
#     """Quantify abundances of transcripts from RNA-seq data."""
#     # groups1 = (group_1, group_2, ..., group_n)
#     #         = ([sample1.1, sample2.1, ...], [sampleA.1, sampleB.1, ...], ..., [sample!.1, sample§.1,...])
#     if samples:
#         from os import listdir
#         from os.path import isfile, join as pjoin
#         from re import match
#         from .quantification import guess_sample_name
#
#         # list fastq files only
#         samples = [pjoin(samples, s) for s in listdir(samples)
#                    if match(r'.*\.f(ast)?q(\.gz)?', s) and isfile(pjoin(samples, s))]
#
#         # build a {sample_name: sample_path} map
#         samples = {guess_sample_name((s,)): s for s in samples}
#
#         # sorting sample_names makes it easy to find corresponding ".1" and ".2" pairs for paired-end samples
#         sample_names = list(samples.keys())
#         sample_names.sort(key=lambda x: (len(x), x))
#         if len(set(map(lambda x: x[:-2], sample_names))) == len(sample_names) // 2:
#             paired_samples = list(zip(sample_names, sample_names[1:]))[::2]
#             for (s1, s2) in paired_samples:
#                 assert (s1[:-2] == s2[:-2])
#                 assert (s1[-2:] == '.1' and s2[-2:] == '.2')
#             reads1, reads2 = zip(*paired_samples)
#             reads1 = [samples[r] for r in reads1]
#             reads2 = [samples[r] for r in reads2]
#         else:
#             # single end
#             raise NotImplementedError("Single-end reads not yet supported.")
#         pass
#
#     from .quantification import INDEX_QUANTIFY_ABUNDANCES as IQA
#     index, quantify, abundances = IQA[method]
#     index_path = index(reference)
#     data = ExprMatrix()
#     from joblib import Parallel, delayed
#     results = Parallel(n_jobs=jobs)(delayed(quantify)(index_path, r, library=library) for r in zip(reads1, reads2))
#     for quant_path, sample_name in results:
#         data[[sample_name]] = abundances(quant_path)[['tpm']]
#     pipe.matrix = ExprMatrix(data)
#     pipe.supplement = None
#     pipe.is_clustered = False
#     pipe.is_grouped = False
#     pipe.selection = 'matrix'
