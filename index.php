<?php
$command = escapeshellcmd('python3 fetch_pubmed.py > /var/www/pubmed/output.txt');
shell_exec($command);
$pub_data=file_get_contents('output.txt');
echo '<textarea id="all" name="w3review" style="width:90%; height:70%">'.$pub_data.'</textarea>';

?>