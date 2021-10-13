nextflow.enable.dsl=2

import java.nio.file.Paths

moduleName="utils"
binDir = Paths.get(workflow.projectDir.toString(), "src/$moduleName/bin/")


process clean_work_dir {

    script:
    """
    bash $binDir/clean_work.sh $params.outDir $params.workDir
    """
}
