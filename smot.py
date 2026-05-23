from getpass import getpass
import json, typer, os

from smotfuncs import sha, baseify, attr, encrypt, get, byte, inpute, getepass, update,remotocrypt

app = typer.Typer()
add = typer.Typer()

remove = typer.Typer()

app.add_typer(remove, name="remove")

app.add_typer(add, name="add")


@add.command("user")
def add_user():
    username = inpute("Username for new user: ")
    password = getepass()
    combohash = remotocrypt(username + password)
    data= {
        "combohash": combohash
    }
    file=baseify(sha(username))
    if os.path.exists(file):
        print("User already exists. Please choose a different username.")
    else:
        with open(baseify(sha(username)), "w") as f:
            json.dump(data, f, indent=4)
    update(username, "users",action="add")
@remove.command("user")
def remove_user():
    
    username = inpute("Username to remove: ").encode('utf-8')
    
    password = getepass().encode('utf-8')
    
    combohash = remotocrypt(username + password)
    
    try:
    
        with open(baseify(sha(username)), "r") as f:
    
            data = json.load(f)
    
            if data.get("combohash") == combohash:
                    delete=True
            else:
                delete=False
        if delete==True:
            import os
            os.remove(baseify(sha(username)))
            update(username, action="remove")
            print("User removed successfully.")
        else:
            print("Incorrect password. User not removed.")
    except FileNotFoundError:
        print("User not found.")
if __name__ == "__main__":
    app()