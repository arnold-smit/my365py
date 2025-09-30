import click

from lib.my365py_auth import M365Auth
from lib.my365py_logger import logger

from lib.my365py_outlook  import commands as m365_outlook
from lib.my365py_onedrive import commands as m365_onedrive


#------------------------------------------------------------------------------------------------
# Main CLI entry point
#------------------------------------------------------------------------------------------------
@click.group()
def cli():
    """Main entry point for the CLI application."""
    print("Hello!!!")
    pass


#------------------------------------------------------------------------------------------------
# OneDrive commands
#------------------------------------------------------------------------------------------------
@cli.group()
def onedrive() -> None:
    """Group of onedrive related commands."""
    pass

onedrive.add_command(m365_onedrive.create_folder)
onedrive.add_command(m365_onedrive.find_files)
onedrive.add_command(m365_onedrive.upload_files)
onedrive.add_command(m365_onedrive.download_files)
onedrive.add_command(m365_onedrive.delete_files)


#------------------------------------------------------------------------------------------------
# Outlook commands
#------------------------------------------------------------------------------------------------
@cli.group()
def outlook() -> None:
    """Group of outlook related commands."""
    pass

outlook.add_command(m365_outlook.send_email)
outlook.add_command(m365_outlook.reply_email)
outlook.add_command(m365_outlook.forward_email)
outlook.add_command(m365_outlook.search_emails)
outlook.add_command(m365_outlook.save_emails)
outlook.add_command(m365_outlook.search_attachments)
outlook.add_command(m365_outlook.save_attachments)


#------------------------------------------------------------------------------------------------
# Main - Better to use entry point for CLI as set-up in pyproject.toml -> [project.scripts]
#------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    ##-------------------------------------------
    ## Currently use this block for quick testing
    ##-------------------------------------------
    print("Starting My365Py CLI...")
    bearer_token = M365Auth()
    print("After call to M365Auth() ...")
    ##-------------------------------------------
    cli()
