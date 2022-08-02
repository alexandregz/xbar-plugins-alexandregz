#!/usr/bin/env php 
<?php
/*
 * <bitbar.title>Dinahosting</bitbar.title>
 * <bitbar.version>v1.0</bitbar.version>
 * <bitbar.author>Alexandre Espinosa Menor</bitbar.author>
 * <bitbar.author.github>alexandregz</bitbar.author.github>
 * <bitbar.image>https://i.imgur.com/zEHwnvu.png</bitbar.image>
 * <bitbar.desc>Your Dinahosting services. ToDo add more utilies</bitbar.desc>
 * <bitbar.dependencies>php</bitbar.dependencies>
 */


$urlApi = 'https://dinahosting.com/special/api.php';
$username = 'xxxxxxxx';
$password = 'xxxxxxx';

$logo_dinahosting = "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";



$request = array(
    'method' => 'User_GetServices',
'params' => array(),
);
$request = json_encode( $request );

$opts = array ('http' => array (
'method'  => 'POST',
'header'  => 'Content-type: application/json'."\r\n".
sprintf( "Authorization: Basic %s\r\n", base64_encode( $username.':'.$password) )."\r\n",
'content' => $request
));
$streamContext  = stream_context_create( $opts );
if( $fp = fopen( $urlApi, 'r', false, $streamContext ) )
{
    $response = '';
    while( $row = fgets($fp) )
    {
        $response .= trim($row)."\n";
    }
    
    fclose( $fp );
    
    $response = json_decode( $response, true );
    
    $out = '';
    foreach($response['data'] as $s) {
	$out .= $s['family'].": ".$s['service']." (".$s['startDate']." - ".$s['endDate'].")\n";
    }
    echo " | image=".$logo_dinahosting."\n";
    echo "---\n";
    echo "$out\n";
}
else
{
    // error connecting or autentication error
    //stream_context_set_default ( $opts );
    //$headers = get_headers($urlApi); // check headers. look for 401 error


    echo "Error connecting dinahosting...";
}
