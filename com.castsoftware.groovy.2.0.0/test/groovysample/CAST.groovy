package com.infy.idp.customtools

import com.infy.idp.utils.*
import com.infy.idp.utils.fs.*


abstract class CAST{

	public static void invokeTool(context, jsonData, envVar) {
		
		def moveCommand;
		moveCommand = 'XCOPY /Y "%IDP_WS%/*" "' + jsonData.buildInfo.castAnalysis.srcPath + '" /E /I'
		
		def runCommand;
		runCommand = 'cast_automation.bat %CURRENT_DATE_TIME% %OLD_VERSION% %NEW_VERSION%'
		
		prepareCastBat(jsonData, envVar)
		
		ExecuteCmd.invokeCmd(context, moveCommand, jsonData.basicInfo.buildServerOS)
		ExecuteCmd.invokeCmd(context, runCommand, jsonData.basicInfo.buildServerOS)
	}
	
	private static void prepareCastBat(jsonData,envVar) {
		
		String fileContent = ReadFile.run('/ant_templates/cast_analysis_automation_script.bat')
		String basepath = jsonData.basicInfo.applicationName  + '_' + jsonData.basicInfo.pipelineName
		String schemaName = jsonData.buildInfo.castAnalysis.schemaName
		
		//fileContent = fileContent.replace('$AppScanCLIScriptPath', basepath + '/' + projectName + '_cliscript.txt')
		//fileContent = fileContent.replace('$AppScanOutputLogFilePath',projectName + '_outputlog.txt')
		fileContent = fileContent.replace('$AppName',jsonData.buildInfo.castAnalysis.applicationName)
		fileContent = fileContent.replace('$ConnProfile',jsonData.buildInfo.castAnalysis.connectionProfile)
		
		if (schemaName.endsWith("_central")) {
			fileContent = fileContent.replace('$SchemaName', schemaName)
		
		} else {
			fileContent = fileContent.replace('$SchemaName',schemaName + "_central");
		}
	
		if (schemaName.endsWith("_central")) {			
			String[] splitWithColen = schemaName.split("_central");
			String backupSchema = splitWithColen[0];
			
			fileContent = fileContent.replace('$BackupSchemaName',backupSchema);
		}
		else {
			fileContent = fileContent.replace('$BackupSchemaName',schemaName);
		}
			
		fileContent = fileContent.replace('$SchemaBackupPath','%IDP_WS%');
						
		def jHome = envVar.JENKINS_HOME
		WriteFile.run(jHome + '/jobs/' + basepath + '/jobs/' + basepath + Constants.BUILDJOBNAMEPOSTFIX + '/cast_automation.bat', fileContent)
	}
}