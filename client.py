from getpass import getpass
import json, typer, os

from remotefuncs import sha, baseify, attr, encrypt, get, byte, inpute, getepass

app = typer.Typer()
add = typer.Typer()

remove = typer.Typer()

app.add_typer(remove, name="remove")

app.add_typer(add, name="add")


@add.command("user")
def add_user():
    username = inpute("Username for new user: ")
    password = getepass()
    combohash = baseify(sha(username + password)).decode()
    data= {
        "combohash": combohash
    }
    file=baseify(sha(username))
    if os.path.exists(file):
        print("User already exists. Please choose a different username.")
    else:
        with open(baseify(sha(username)), "w") as f:
            json.dump(data, f, indent=4)
@remove.command("user")
def remove_user():
    
    username = inpute("Username to remove: ")
    
    password = getepass()
    
    combohash = baseify(sha(username + password)).decode()
    
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
            print("User removed successfully.")
        else:
            print("Incorrect password. User not removed.")
    except FileNotFoundError:
        print("User not found.")
if __name__ == "__main__":
    app()