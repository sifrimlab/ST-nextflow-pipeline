nextflow.enable.dsl=2


import java.nio.file.Paths

moduleName="utils"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")
process add_parent_dir_to_file_name {
        echo = true
        input:
        val dataDir
        // round dir prefix should contain a wildcard element in there somewhere, 
        // As it will be used to create a glob pattern
        val round_dir_prefix

        script:
        if (round_dir_prefix.contains("*")){
                """
                echo 'contains'
                python $binDir/modules/addRoundToFileNames.py $dataDir $round_dir_prefix
                """
        }
        else {
                """
                echo 'does not contain'
                """
                println("Your prefix inserted prefix does not contain a wildcard!")
        }

}


