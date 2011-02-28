Evolved Quick Highlight Mode
=====

This plugin provides a faster and easier way to switch the current document syntax 
highlighting mode in the gedit text editor (GNOME default text editor). Just press
`Ctrl+Shift+H`, type the language and press `Enter`.

### Homepage

For more information about this plugin, consider visiting: <http://gedit.evolved.com.br/>.

Installation
-----

1. Download this repository using `$ git clone git://github.com/nagaozen/gedit-plugin-quickhighlightmode.git` in your *nix terminal or by clicking at the Download button at top selecting the master branch.
1. Copy `quickhighlightmode.gedit-plugin` file and `quickhighlightmode` folder into your `~/.gnome2/gedit/plugins/` folder.
1. Open gedit and click `Edit -> Preferences -> Plugins`.
1. Check the `Evolved Code Browser` and hit `Close`.
1. That's it! Now you should be able to change the document syntax highlighting mode by pressing `Ctrl+Shift+H`.

License
-----

Copyright (C) 2009-2011 [Fabio Zendhi Nagao](http://zend.lojcomm.com.br/)

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA

Credits
-----

- Original concept by Nando Vieira @ <http://simplesideias.com.br/quick-highlight-mode/>.
- Current build by [Fabio Zendhi Nagao](http://zend.lojcomm.com.br/).

Changes
-----

> @2011-02-28  
> - _update_: Plugin entirely rebuilt. Works also in Windows and Mac OSX.

> @2009-05-15  
> - _fix_: Working in gnome 2.26.#  
> - _new_: Implemented ascending order to the options  
> - _new_: Minor optimizations which made the plugin more robust and small

> @2009-04-10  
> I'm currently working to rewrite the entire plugin following the PythonPluginHowTo
> suggested structure for an easier and better open source contribution. Also I'm fixing the bugs wherever I found them.
