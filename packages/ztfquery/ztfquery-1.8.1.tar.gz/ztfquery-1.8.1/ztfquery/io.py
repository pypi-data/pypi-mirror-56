#!/usr/bin/env python
#

import os
import sys
import requests
import warnings
LOGIN_URL = "https://irsa.ipac.caltech.edu/account/signon/login.do"

import base64
if sys.version_info > (3,0):
    from configparser import ConfigParser
    _PYTHON3 = True
else:
    from ConfigParser import ConfigParser
    _PYTHON3 = False
    
_SOURCEDIR = os.path.dirname(os.path.realpath(__file__))


_ENCRYPT_FILE = os.path.expanduser("~")+"/.ztfquery"
_ENCRYPTING_FILE = os.path.expanduser("~")+"/.queryirsa"


LOCALSOURCE   = os.getenv('ZTFDATA',"./Data/")
# ================= #
#  Crypting         #
# ================= #

def _load_id_(which, askit=True):
    """ returns login information for the requested enty"""
    import base64
    config = ConfigParser()
    config.read( _ENCRYPT_FILE )
    if which not in config.sections():
        if not askit:
            raise AttributeError("No %s account setup. Add then in ~/.ztfquery or run ztfquery.io.set_account(%s)"%(which,which))
        else:
            print("No %s account setup, please provide it"%which)
            set_account(which)
            config = ConfigParser()
            config.read( _ENCRYPT_FILE )

    if _PYTHON3:
        return config[which.lower()]["username"], base64.b64decode(config[which.lower()]["password"][2:-1]).decode("utf-8")
    else:
        return config.get(which.lower(),"username"), base64.b64decode(config.get(which.lower(),"password"))

def set_account(which, username=None, password=None, test=True, force=False):
    """ Setup the username and password (simply encrypted!) for the given `which` account. 
    Saved in ~/.ztfquery
    """
    import base64
    import getpass
    config = ConfigParser()
    config.read( _ENCRYPT_FILE )
    # - Name & Password
    if username is None:
        if _PYTHON3:
            username = input('Enter your %s login: '%which)
        else:
            username = raw_input('Enter your %s login: '%which)
            
    if password is None:
        password = getpass.getpass()
        
    # - Check inputs
    if test:
        wrong_ = False
        if which == "irsa":
            if not test_irsa_account([username, password]):
                warnings.warn("The irsa_test for you account returns False. Most likely you provided incorrect logins")
                wrong_ = True
        else:
            warnings.warn("No test designed for %s. Cannot test if logins are correct."%which)
        if wrong_ and not force:
            raise ValueError("Bad username/passworg for %s. force=False so the logins are not stored. "%which)
            
    password_ = base64.b64encode( password.encode("utf-8") )
    if _PYTHON3:
        config[which.lower()] = {"username":username, "password": password_ }        
    else:
        section = which.lower()
        if section not in config.sections():
            config.add_section(section)
        config.set(section,"username",username)
        config.set(section,"password",password_)

        
    with open( _ENCRYPT_FILE , 'w') as configfile:
        config.write(configfile)
        

#
# TEST
# 
def test_irsa_account(auth=None):
    """  returns True if the IRSA account is correctly set. """
    if auth is None:
        auth = _load_id_("irsa")
    return ".ipac.caltech.edu" in get_cookie(*auth)._cookies


# ================= #
#   Logging Tools   #
# ================= #
def get_cookie(username, password):
    """Get a cookie from the IPAC login service

    Parameters
    ----------
    username: [str]
        The IPAC account username
    password: [str]
        The IPAC account password
    """
    url = "%s?josso_cmd=login&josso_username=%s&josso_password=%s" % (LOGIN_URL, username, password)
    return requests.get(url).cookies


def _download_(args):
    """ To be used within _ZTFDownloader_.download_data() 
    url, fileout,overwrite,verbose = args
    """
    url, fileout,  overwrite, verbose = args
    download_single_url(url, fileout=fileout, overwrite=overwrite, verbose=verbose)

def download_url(to_download_urls, download_location,
                show_progress = True, notebook=False, verbose=True,
                overwrite=False, nprocess=None,cookies=None, **kwargs):
    """ """
    if nprocess is None:
        nprocess = 1
    elif nprocess<1:
        raise ValueError("nprocess must 1 or higher (None means 1)")

    if nprocess == 1:
        # Single processing
        if verbose: print("No parallel downloading")
        for url, fileout in zip(to_download_urls, download_location):
            download_single_url(url,fileout=fileout, show_progress=show_progress,
                                    notebook=notebook, 
                                    overwrite=overwrite, verbose=verbose, cookies=cookies, **kwargs)
    else:
        # Multi processing
        import multiprocessing
        if show_progress:
            from astropy.utils.console import ProgressBar
            bar = ProgressBar( len(to_download_urls), ipython_widget=notebook)
        else:
            bar = None
                
        if verbose:
            print("parallel downloading ; asking for %d processes"%nprocess)

        # Passing arguments
        overwrite_ = [overwrite]*len(to_download_urls)
        verbose_   = [verbose]*len(to_download_urls)
        with multiprocessing.Pool(nprocess) as p:
            # Da Loop
            for j, result in enumerate( p.imap_unordered(_download_, zip(to_download_urls,
                                                                    download_location,
                                                                 overwrite_, verbose_))):
                if bar is not None:
                    bar.update(j)
                    
            if bar is not None:
                bar.update( len(to_download_urls) )
            
def download_single_url(url, fileout=None, 
                        overwrite=False, verbose=True, cookies=None,
                        show_progress=True, notebook=False, chunk=1024, **kwargs):
    """ Download the url target using requests.get.
    the data is returned (if fileout is None) or stored in `fileout`
    Pa
    """
    if fileout is not None and not overwrite and os.path.isfile( fileout ):
        if verbose:
            print("%s already exists: skipped"%fileout)
        return
    else:
        if verbose and fileout:
            print("downloading %s to %s"%(url,fileout))

    # = Password and Username
    if cookies is None: cookies = get_cookie(*_load_id_("irsa"))

        
    # - requests options 
    download_prop = dict(cookies=cookies, stream=True)
    for k,v in kwargs.items(): download_prop[k] = v
    if cookies in ["no_cookies"]: _ = download_prop.pop("cookies")

    request_fnc = "get" if not "data" in download_prop else "post"
    # = Where should the data be saved?
    if fileout is not None:
        directory = os.path.dirname(fileout)
        if not os.path.exists(directory):
            os.makedirs(directory)

    else:
        download_prop["stream"] = False
        return getattr(requests,request_fnc)(url, **download_prop)

    # With Progress bar?
    if not show_progress:
        response = getattr(requests,request_fnc)(url, **download_prop)
        if response.status_code == 200:
            with open(fileout, 'wb') as f:
                for data in response.iter_content(chunk):
                    f.write(data)
    
    else:
        from astropy.utils.console import ProgressBar
        response = getattr(requests,request_fnc)(url, **download_prop)
        if response.status_code == 200:
            chunk_barstep = 500
            f = open(fileout, 'wb')
            with ProgressBar(int(response.headers.get('content-length'))/(chunk_barstep*chunk),
                             ipython_widget=notebook) as bar:
                for i,data in enumerate(response.iter_content(chunk_size=chunk)):
                    if i%chunk_barstep==0:
                        bar.update()
                    f.write(data)
            f.close()
