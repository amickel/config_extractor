This file extracts the configuration out of a .bin, support log, diagnostic log or config summary and exports it to a file in a format that can be directly pasted into a PUT request to a group in NCM.

To extract the config out of a file:
    1) Double click on the log_2_config file 
    2) Leave the API key boxes and group ID box blank.
    3) Click the "Browse" button to browse to the file you want to convert. 
    4) Click "Do The Thing!"
    5) The configuration will be written to a file named "Config.txt". 

To put the config on a group:
    1) Double click on the log_2_config file 
    2) Paste in your API keys.
    3) Paste in the group ID you want the config to be applied to. 
    4) Click the "Browse" button to browse to the file you want to convert. 
    5) Click "Do The Thing!"
    6) The configuration will be written to the group as well as a file named "Config.txt". 
    

Your keys file needs to look like this, but with your own keys pasted in-between the quotes on the right. 
"X-CP-API-ID": "00000000"
"X-CP-API-KEY": "00000000000000000000000000000000"
"X-ECM-API-ID": "00000000-0000-0000-0000-000000000000"
"X-ECM-API-KEY": "0000000000000000000000000000000000000000"

To avoid pasting in your API keys every time you run the program you can save the keys as environment variables. 

NOTE: this will remove the users section of the config and change all other passwords to "Welcome!". 
