# mksystemdsvc.py

A python script for generating and installing systemd service files.

I use a template approach for this and you maybe not agreeing with my template.
In that case just modify template.service or the script if the changes are more complex.

I'm also eager for improvements and extensions, systemd is huge and there is a lot that I don't know yet. So if you are a cool person and have some improvements open a issue or send me a pull request!

## Dependencies

You will need
    - Python 3.6 or higher
    - prompt-toolkit
    - elevate

The easiest way to get all dependencies is by running `python3 -m pip install -r requirements.txt`. If your package manager can provide all dependencies download them that way.

## Usage

```sh
mksystemdsvc.py [-h] [--install INSTALL]
```

### Optional arguments

```sh
  --install INSTALL  Install the generated systemd file. You need root rights
                     or sudo to use this option.
```