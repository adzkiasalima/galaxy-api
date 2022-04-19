from bioblend.galaxy import GalaxyInstance


def run(name,
        fastq1,
        fastq1type,
        fastq2,
        fastq2type,
        reference=None,
        reftype=None):
    gi = GalaxyInstance('http://127.0.0.1:8080', key='3bdbbb547c6c30ba5663ddb8842ffb07')

    # get workflow
    workflow_id = 'f2db41e1fa331b3e'
    workflow = gi.workflows.get_workflows('f2db41e1fa331b3e')

    # create history
    # output_history_name = "Experimen 1"
    output_history_name = name
    outputhist_dict = gi.histories.create_history(output_history_name)
    outputhist = outputhist_dict['id']

    # create data library
    library_name = "Data Experimen 1"
    library_dict = gi.libraries.create_library(library_name)
    library = library_dict['id']

    # get inputs
    # file1= 'https://zenodo.org/record/2582555/files/SLGFSK-N_231335_r1_chr5_12_17.fastq.gz'
    # file2= 'https://zenodo.org/record/2582555/files/SLGFSK-N_231335_r2_chr5_12_17.fastq.gz'
    # referencefile = 'https://zenodo.org/record/2582555/files/hg19.chr5_12_17.fa.gz'

    # file1= 'https://zenodo.org/record/582600/files/mutant_R1.fastq'
    # file2= 'https://zenodo.org/record/582600/files/mutant_R2.fastq'
    # referencefile = 'https://zenodo.org/record/582600/files/wildtype.fna'
    file1 = fastq1
    file2 = fastq2
    if reference is None:
        referencefile = 'https://zenodo.org/record/582600/files/wildtype.fna'
    else:
        referencefile = reference

    dataset1 = gi.libraries.upload_file_from_url(library, file1, file_type=fastq1type)
    dataset2 = gi.libraries.upload_file_from_url(library, file2, file_type=fastq2type)
    dataset3 = gi.libraries.upload_file_from_url(library, referencefile, file_type=reftype)
    id1, id2, id3 = dataset1[0]['id'], dataset2[0]['id'], dataset3[0]['id']

    # Get the input step IDs from the workflow.
    # We use the BioBlend convenience function get_workflow_inputs to retrieve inputs by label.
    input1 = gi.workflows.get_workflow_inputs(workflow_id, label='Forward Reads')[0]
    input2 = gi.workflows.get_workflow_inputs(workflow_id, label='Reverse Reads')[0]
    input3 = gi.workflows.get_workflow_inputs(workflow_id, label='reference')[0]

    datamap = {
        input1: {'src': 'ld', 'id': id1},
        input2: {'src': 'ld', 'id': id2},
        input3: {'src': 'ld', 'id': id3},
    }

    # run workflow
    gi.workflows.invoke_workflow(workflow_id, inputs=datamap, history_id=outputhist,
                                 import_inputs_to_history=True)

    return "OK"
