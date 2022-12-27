$| = 1; $i = 1;
while(1){
	 sysread(STDIN,$ch,1) or exit;
	 printf "%02x\n",ord($ch)
}
