<?php
// API to use with xbar plugin 
// Actually only for wireguard :-(
//
// NOTE: I tried to reuse scripts used into pivpn to be less invasive with the project
//
// Alexandre Espinosa Menor - aemenor@gmail.com
//

//
// 1) copy this file to /usr/local/src/pivpn/scripts:
//
//  pi@raspberrypi:/var/www/html/admin (master) $ sudo ln -s /usr/local/src/pivpn 
//
// 2) to use with lighttpd installed by pihole, you need to create link into /var/www/html/admin/:
// 
//  pi@raspberrypi:/var/www/html/admin (master) $ sudo ln -s /usr/local/src/pivpn/scripts/api.php api-pivpn.php
//  pi@raspberrypi:/var/www/html/admin (master) $
//
// 3) also you need to add to sudoers clientSTAT.sh script:
//
//  root@raspberrypi:/etc/sudoers.d# cat /etc/sudoers.d/clientSTAT
//  www-data ALL=NOPASSWD: /usr/local/src/pivpn/scripts/wireguard/clientSTAT.sh
//  root@raspberrypi:/etc/sudoers.d#
//



ini_set('display_errors', 0);
error_reporting(0);

$service = 'wireguard'; // $argv[1];

if($service !== 'wireguard' && $service !== 'openvpn') {
    die("Usage: {$argv[0]} (wireguard|openvpn)\n");
}


$path_scripts = '/usr/local/src/pivpn/scripts/';

$commands = [
    'wireguard' => [
        'clients' => 'sudo '.$path_scripts.'wireguard/clientSTAT.sh',
        'status' => 'systemctl is-active wg-quick@wg0',
    ],
    'openvpn' => [
        'clients' => null,
        'status' => 'systemctl is-active openvpn',
    ]
];


$status = false;

foreach($commands[$service] as $k => $c) {
    if($c == null) continue;

    $output = shell_exec($c." 2>&1");

    if($k === 'clients') {
        $arr_connected = $arr_disabled = [];
        $connected = $disabled = false;
        foreach(explode("\n", trim($output)) as $l) {
            if(strpos($l, '::: Connected') !== false) {
                $connected = true;
                $disabled = false;
                continue;
            }

            if(strpos($l, '::: Disabled') !== false) {
                $connected = false;
                $disabled = true;
                continue;
            }

            if($connected) {
                $arr_connected[] = preg_split("/\s{2,}+/", $l);
            }

            if($disabled) {
                $arr_disabled[] = preg_split("/\s{2,}+/", $l);
            }
        }
    }


    if($k === 'status') {
        $status = trim($output);
    }
}


// remove first element from connected, just name fields and with specials chars to look fine in bash, not fine for JSON
array_shift($arr_connected);


$data = [
    'connected' => $arr_connected,
    'disabled' => $arr_disabled,
    'status' => $status,
];

echo json_encode($data, 1);





