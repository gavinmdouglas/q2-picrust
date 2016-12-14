from subprocess import run

def run_system_cmds( cmd ):

        print( "Running command-line program outside of QIIME 2." , end="\n" ,  flush= True )
        print( "You wont be able to access the input and output filenames referred to since they are temporary files." , end="\n")
        print( "The below command is being run:", end="\n" )
        print( cmd )

        run( cmd.split() , check=True )
