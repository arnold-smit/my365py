# my365py

The my365py cli program is written to provide have programetic access to a small set of functions within the Microsoft 365 service that is not readily available under Linux. This is done by using the Microsoft Graph API.

In first instance this will be about
* Outlook
  * Search emails
  * Send emails
  * Store attachments
* OneDrive
  * Search files
  * Download files
  * Upload files

## Design
The main idea is that each call to the cli returns a list of object dictionaries.
These can then be chained into more elaborate functionality, for instance:
search_emails > \
save_email
At a later stage a for_each operator will be implemented that takes a script as argument and loops over the output list and calls the script for each entry. For instance parsing pdf attachments or storing some information in a database.
search_attachment > \
save_attachment % > \
for_each % process_attachment.py

