#!/usr/bin/env bash
cmd="./sumologic-ishi.py" 
credentials="-p pass -u user"
sourcesystem="-s localhost -t splunk"
baseurl="https://collectors.jp.sumologic.com/receiver/v1/http"
collector="ZaVnC4dhaV0MnCOwJ5fk69I5ucUjRTnUfAqKCW7TJpvHHk37oR8b5BAK76tIWb7OKmXgbQ9CZxziLSfhI9RkH5oIDZMU859ekRe1UlGDHN9WEYd6v9JwRA=="

declare -a filelist
filelist[1]="/var/log/CylanceSvc.log"
filelist[2]="/var/log/alf.log"
filelist[3]="/var/log/appfirewall.log"
filelist[4]="/var/log/corecaptured.log"
filelist[5]="/var/log/displaypolicyd.stdout.log"
filelist[6]="/var/log/fsck_apfs.log"
filelist[7]="/var/log/fsck_apfs_error.log"
filelist[8]="/var/log/fsck_hfs.log"
filelist[9]="/var/log/install.log"
filelist[10]="/var/log/shutdown_monitor.log"
filelist[11]="/var/log/system.log"
filelist[12]="/var/log/wifi-07-28-2019__17:50:02.796.log"
filelist[13]="/var/log/wifi.log"
printf -v filelist_d ' -f %s ' "${filelist[@]}" 
filelist_d=${filelist_d:1}

echo "$cmd ${credentials} ${sourcesystem} -w $baseurl/$collector ${filelist_d}"
