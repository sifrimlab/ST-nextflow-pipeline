nextflow.enable.dsl=2


import java.nio.file.Paths

moduleName="utils"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")

process add_parent_dir_to_file_name {
        echo = true

        script:
        """
        python $binDir/modules/addRoundToFileNames.py $params.dataDir $params.round_prefix
        """

}


