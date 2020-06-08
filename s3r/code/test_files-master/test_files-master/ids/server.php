<?php
// receive data passed to the script
$val = $_GET["data"];
$fileContent=$val."\n";
$filename = "datastorage.txt";
// append data to datastorage.txt
$fileStatus=file_put_contents($filename,$fileContent,FILE_APPEND);
if($fileStatus != false)
{
                echo  "SUCCESS. Data written in file.";
		$file = file($filename);
		// remove first value (to control file size)
  		unset($file[0]);
  		file_put_contents($filename, $file);
}
else
{
                echo  "FAIL. Could not connect to file.";
}