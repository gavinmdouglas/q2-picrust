import qiime
import biom
from tempfile import TemporaryDirectory
from os import path
from q2_types.feature_table import FeatureTable , Frequency
from subprocess import run

def normalize_by_copy_number( otu_table : biom.Table , 
                             gg_version : str=None ) -> biom.Table :               

    tmp = otu_table.metadata( id="58CMK8KO", axis="sample")
    print( tmp )

    cmd = "normalize_by_copy_number.py --input_otu_fp --INPUT--"\
    " --output_otu_fp --OUTPUT--"
    
    if gg_version:
        cmd += " --gg_version " + gg_version

    norm_biom = run_picrust_cmds( cmd , otu_table )

    return norm_biom 



def predict_metagenomes( norm_otu_table : biom.Table ,
                          gg_version : str=None , 
                          type_of_prediction = "ko",
                          normalize_by_function : bool=False ,
                          normalize_by_otu : bool=False ,
                          suppress_subset_loading : bool=False ) -> biom.Table:

    cmd = "predict_metagenomes.py -i " + "--INPUT--" + \
    " -o " + "--OUTPUT--" + " -t " + type_of_prediction

    if normalize_by_function:
        cmd += " --normalize_by_function"
    elif normalize_by_otu:
        cmd += " --normalize_by_otu"

    if suppress_subset_loading:
        cmd += " --suppress_subset_loading"

    meta_predict_table = run_picrust_cmds( cmd , norm_otu_table )

    return meta_predict_table 



def categorize_by_function( predicted_table : biom.Table ,
                            metadata_category : str="KEGG_Pathways",
                            level : int=3, 
                            ignore : bool=False ) -> biom.Table :

    cmd = "categorize_by_function.py -i --INPUT--"+ \
    " -o --OUTPUT--" + " --metadata_category " + metadata_category + \
    " --level " + str(level)

    if ignore:
        cmd += " --ignore"

    category_function_table = run_picrust_cmds( cmd , predicted_table )

    return category_function_table    



def metagenome_contributions( output_dir: str, norm_otu_table : biom.Table ,
                            outfile : str ,
                            type_of_prediction = "ko",
                            gg_version : str=None ,
                            limit_to_function : str=None , 
                            suppress_subset_loading : bool=False ) -> None:

    cmd = "metagenome_contributions.py -i --INPUT--"+ \
    " -o " + outfile + " --type_of_prediction " + type_of_prediction 

    if gg_version:
        cmd += " --gg_version " + gg_version

    if suppress_subset_loading:
        cmd += " --suppress_subset_loading " + suppress_subset_loading

    if limit_to_function:
        cmd += " --limit_to_function " + limit_to_function

    print( "\nRunning command-line program outside of QIIME 2." , end="\n\n"  )
    print( "The below command is being run:", end="\n" )
    print( cmd )

    run( cmd.split() , check=True )

    return None   


def run_picrust_cmds( cmd , biom2input ):

     # open temporary directories
    with TemporaryDirectory() as temp_dir_name:

        # get temporary BIOM input and output filenames
        tmp_input = path.join( temp_dir_name , 'input.biom' )
        tmp_output = path.join( temp_dir_name , 'output.biom' )

        # write out temporary input BIOM file
        with biom.util.biom_open( tmp_input , 'w' ) as tmp_input_stream:
            biom2input.to_hdf5( generated_by="qiime2 artifact" , h5grp=tmp_input_stream )
        #tmp_input_stream = open(tmp_input, 'w')
        #biom2input.to_json( "qiime2 artifact" , tmp_input_stream )
        #tmp_input_stream.close()

        # replace dummy strings with actual tmp filenames
        cmd = cmd.replace( "--INPUT--" , tmp_input )
        cmd = cmd.replace( "--OUTPUT--" , tmp_output )

        print( "\nRunning command-line program outside of QIIME 2." , end="\n\n"  )
        print( "You wont be able to access the input and output filenames referred",
            "to since they are temporary files." , end="\n\n" )

        print( "The below command is being run:", end="\n" )
        print( cmd, end="\n\n\n" )

        run( cmd.split() , check=True )

        # read in temporary biom output file and return so that an artifact file can be written ("output")
        with biom.util.biom_open( tmp_output , 'r' ) as tmp_hdf5_biom:
            output = biom.Table.from_hdf5( tmp_hdf5_biom )

    return output 
