import qiime.plugin
import q2_picrust

from q2_types.feature_table import FeatureTable , Frequency

plugin = qiime.plugin.Plugin(
    name='picrust',
    version=q2_picrust.__version__,
    website='http://picrust.github.io/picrust/',
    package='q2_picrust',

    user_support_text=( "If you have any questions you can check out the "
                        "PICRUSt users google group: "
                        "https://groups.google.com/forum/#!forum/picrust-users" ) ,

    citation_text=("Langille and Zaneveld et al. 2013. Predictive functional "
                  "profiling of microbial communities using 16S rRNA marker "
                  "gene sequences. Nature Biotechnology 31:814-821. "
                  "doi: 10.1038/nbt.2676") 
)

plugin.methods.register_function(

    function=q2_picrust.normalize_by_copy_number,

    inputs={   'otu_table' : FeatureTable[ Frequency ]   } ,

    parameters={
        'gg_version' : qiime.plugin.Str ,
        #'version' : qiime.plugin.Bool ,
        #'help' : qiime.plugin.Bool ,
        #'input_count_fp' : qiime.plugin.Str ,
        #'metadata_identifier' : qiime.plugin.Str , 
        #'load_precalc_file_in_biom' : qiime.plugin.Bool 
  },
	
    outputs=[  ( 'output' , FeatureTable[ Frequency ]  )  ],
    name='Normalize by copy number',
    description='This method normalizes an OTU table by dividing each OTU\'s' + 
                'frequency by the known or predicted 16S rRNA copy number abundance'
)


plugin.methods.register_function(

    function=q2_picrust.predict_metagenomes,

    inputs={   'norm_otu_table' : FeatureTable[ Frequency ]   } ,

    parameters={
        'gg_version' : qiime.plugin.Str ,
        'type_of_prediction' : qiime.plugin.Str ,
        'normalize_by_function' : qiime.plugin.Bool ,
        'normalize_by_otu' : qiime.plugin.Bool ,
        'suppress_subset_loading' : qiime.plugin.Bool ,
  },
    
    outputs=[  ( 'output' , FeatureTable[ Frequency ]  )  ],
    name='Predict metagenomes',
    description='This method multiplies each OTU abundance by each functional trait abundance ' +
                'to produce a table of functions (rows) by samples (columns)'
)


plugin.methods.register_function(

    function=q2_picrust.categorize_by_function,

    inputs={   'predicted_table' : FeatureTable[ Frequency ]  } ,

    parameters={
        'metadata_category' : qiime.plugin.Str , 
        'level' : qiime.plugin.Int ,
        'ignore' : qiime.plugin.Bool 
  },
    
    outputs=[  ( 'output' , FeatureTable[ Frequency ]  )  ],
    name='Categorize by function',
    description='This script collapses hierarchical data to a specified level.' + 
                'For instance, often it is useful to examine KEGG results from a higher level within the pathway hierarchy. ' +
                'Many genes are sometimes involved in multiple pathways, and in these circumstances ' + 
                '(also know as a one-to-many relationship), the gene is counted for each pathway.' +
                'This has a side effect of increasing the total count of genes in the table.'
)


plugin.visualizers.register_function(

    function=q2_picrust.metagenome_contributions,

    inputs={   'norm_otu_table' : FeatureTable[ Frequency ]  } ,

    parameters={
        'outfile' : qiime.plugin.Str , 
        'type_of_prediction' : qiime.plugin.Str ,
        'gg_version' : qiime.plugin.Str ,
        'limit_to_function' : qiime.plugin.Bool ,
        'suppress_subset_loading' : qiime.plugin.Bool  
  },
    
   #outputs=[  None ],

    name='Metagenome contributions',
    description='This script partitions metagenome functional contributions according' +
                ' to function, OTU, and sample, for a given OTU table.'
)
