# -*- coding: utf-8 -*-

#    Copyright (C) 2016-2018 Mathew Topper
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from polite.paths import Directory
from dtocean_app.utils.config import (get_install_paths,
                                      init_config,
                                      init_config_parser,
                                      init_config_interface)


def test_get_install_paths(mocker, tmpdir):
    
    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_app.utils.config.UserDataDirectory',
                 return_value=mock_dir)
                 
    init_config(install=True)
    test_dict = get_install_paths()
    
    assert "man_user_path" in test_dict


def test_init_config(mocker, tmpdir):

    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_app.utils.config.UserDataDirectory',
                 return_value=mock_dir)
                 
    init_config(logging=True, files=True)
        
    assert len(config_tmpdir.listdir()) == 2
              
    init_config(logging=True, files=True)
    
    assert len(config_tmpdir.listdir()) == 4
              

def test_init_config_overwrite(mocker, tmpdir):

    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_app.utils.config.UserDataDirectory',
                 return_value=mock_dir)
                 
    init_config(logging=True, files=True)
        
    assert len(config_tmpdir.listdir()) == 2
              
    init_config(logging=True, files=True, overwrite=True)
    
    assert len(config_tmpdir.listdir()) == 2
              
              
def test_init_config_install(mocker, tmpdir):

    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_app.utils.config.UserDataDirectory',
                 return_value=mock_dir)
                 
    init_config(logging=True, files=True, install=True)
        
    assert len(config_tmpdir.listdir()) == 3

    
def test_init_config_parser():
    
    args = init_config_parser([])
    
    assert not any(args)


def test_init_config_parser_overwrite():
    
    args = init_config_parser(["--overwrite"])
    
    assert args[-1]
    assert not any(args[:-1])
    
    
def test_init_config_parser_install():
    
    logging, files, install, overwrite = init_config_parser(["--install"])
    
    assert not any([logging, files, overwrite])
    assert install
    
    
def test_init_config_interface(mocker, tmpdir):

    # Make a source directory with some files
    config_tmpdir = tmpdir.mkdir("config")
    mock_dir = Directory(str(config_tmpdir))
        
    mocker.patch('dtocean_app.utils.config.UserDataDirectory',
                 return_value=mock_dir)
    mocker.patch('dtocean_app.utils.config.init_config_parser',
                 return_value=(True, True, False, False))
                 
    init_config_interface()
        
    assert len(config_tmpdir.listdir()) == 2
