# CWAPasswordExtractor
Utility for Extracting all passwords from ConnectWise Automate (E.g. while migrating to a new system). Outputs a csv file with all fields displayed in CWA for stored credentials.

ConnectWise don't seem to be fond of giving you an unencrypted dump of your passwords stored in CW Automate so I dug into Developer Tools in Chrome with the CWA web client open and discovered the following:

Passwords are retrieved and stored in memory as plaintext when you right-click on a credential in the passwords area. You can combine the parameters of that request with the one that retrieves the list of credentials to make a request for retreiving all credentials for a client using that client's ID. Then all you need to do is grab all client IDs and iterate over them. There's probably an even simpler way to get all credentials for all clients but I didn't really have time to look into that.

Usage: `python CW_Automate_PW_Extractor.py --clientid '00000000-0000-0000-0000-000000000000' --bearer_token 'bearer asdf1234asdf1234asdf1234==' --base_url 'https://myorgname.hostedrmm.com' --output_file 'cwa_passwords.csv'`

You can get your clientid and bearer token from the developer tools while you have the web client open (it might also work if you've got an existing API key and auth/token flow elsewhere but I haven't tried that, this is just quick and dirty). I tend to get these parameters from the "deploymentlogins?" request like so:
![image](https://user-images.githubusercontent.com/16311787/145383318-88f6fbf6-2d3f-4302-b45d-7ab9791de4e7.png)

# Requirements
- pandas (for exporting to csv)
- requests (for making API calls)
