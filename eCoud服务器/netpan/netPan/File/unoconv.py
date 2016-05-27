#!/usr/bin/env python

### This program is free software; you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation; version 2 only
###
### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.
###
### You should have received a copy of the GNU General Public License
### along with this program; if not, write to the Free Software
### Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
### Copyright 2007-2010 Dag Wieers <dag@wieers.com>

from __future__ import print_function

from distutils.version import LooseVersion
import getopt
import glob
import os
import subprocess
import sys
import time

__version__ = "$Revision$"
# $Source$

VERSION = '0.6'


doctypes = ('document', 'graphics', 'presentation', 'spreadsheet')

global convertor, office, ooproc, product,inputfn
ooproc = None
exitcode = 0


class Office:
    def __init__(self, basepath, urepath, unopath, pyuno, binary, python, pythonhome):
        self.basepath = basepath
        self.urepath = urepath
        self.unopath = unopath
        self.pyuno = pyuno
        self.binary = binary
        self.python = python
        self.pythonhome = pythonhome

    def __str__(self):
        return self.basepath

    def __repr__(self):
        return self.basepath

### Implement a path normalizer in order to make unoconv work on MacOS X
### (on which 'program' is a symlink to 'MacOSX' which seems to break unoconv)

def realpath(*args):
    ''' Implement a combination of os.path.join(), os.path.abspath() and
        os.path.realpath() in order to normalize path constructions '''
    ret = ''
    for arg in args:
        ret = os.path.join(ret, arg)
    return os.path.realpath(os.path.abspath(ret))

### The first thing we ought to do is find a suitable Office installation
### with a compatible pyuno library that we can import.
###
### See: http://user.services.openoffice.org/en/forum/viewtopic.php?f=45&t=36370&p=166783

def find_offices():
    ret = []
    extrapaths = []

    ### Try using UNO_PATH first (in many incarnations, we'll see what sticks)
    if 'UNO_PATH' in os.environ:
        extrapaths += [ os.environ['UNO_PATH'],
                        os.path.dirname(os.environ['UNO_PATH']),
                        os.path.dirname(os.path.dirname(os.environ['UNO_PATH'])) ]

    else:

        if os.name in ( 'nt', 'os2' ):
            if 'PROGRAMFILES' in list(os.environ.keys()):
                extrapaths += glob.glob(os.environ['PROGRAMFILES']+'\\LibreOffice*') + \
                              glob.glob(os.environ['PROGRAMFILES']+'\\OpenOffice.org*')

            if 'PROGRAMFILES(X86)' in list(os.environ.keys()):
                extrapaths += glob.glob(os.environ['PROGRAMFILES(X86)']+'\\LibreOffice*') + \
                              glob.glob(os.environ['PROGRAMFILES(X86)']+'\\OpenOffice.org*')

        elif os.name in ( 'mac', ) or sys.platform in ( 'darwin', ):
            extrapaths += [ '/Applications/LibreOffice.app/Contents',
                            '/Applications/NeoOffice.app/Contents',
                            '/Applications/OpenOffice.org.app/Contents' ]

        else:
            extrapaths += glob.glob('/usr/lib*/libreoffice*') + \
                          glob.glob('/usr/lib*/openoffice*') + \
                          glob.glob('/usr/lib*/ooo*') + \
                          glob.glob('/opt/libreoffice*') + \
                          glob.glob('/opt/openoffice*') + \
                          glob.glob('/opt/ooo*') + \
                          glob.glob('/usr/local/libreoffice*') + \
                          glob.glob('/usr/local/openoffice*') + \
                          glob.glob('/usr/local/ooo*') + \
                          glob.glob('/usr/local/lib/libreoffice*')

    ### Find a working set for python UNO bindings
    for basepath in extrapaths:
        if os.name in ( 'nt', 'os2' ):
            officelibraries = ( 'pyuno.pyd', )
            officebinaries = ( 'soffice.exe' ,)
            pythonbinaries = ( 'python.exe', )
            pythonhomes = ()
        elif os.name in ( 'mac', ) or sys.platform in ( 'darwin', ):
            officelibraries = ( 'pyuno.so', 'libpyuno.dylib' )
            officebinaries = ( 'soffice.bin', 'soffice')
            pythonbinaries = ( 'python.bin', 'python' )
            pythonhomes = ( 'OOoPython.framework/Versions/*/lib/python*', )
        else:
            officelibraries = ( 'pyuno.so', )
            officebinaries = ( 'soffice.bin', )
            pythonbinaries = ( 'python.bin', 'python', )
            pythonhomes = ( 'python-core-*', )

        ### Older LibreOffice/OpenOffice and Windows use basis-link/ or basis/
        libpath = 'error'
        for basis in ( 'basis-link', 'basis', '' ):
            for lib in officelibraries:
                if os.path.isfile(realpath(basepath, basis, 'program', lib)):
                    libpath = realpath(basepath, basis, 'program')
                    officelibrary = realpath(libpath, lib)
                    info(3, "Found %s in %s" % (lib, libpath))
                    # Break the inner loop...
                    break
            # Continue if the inner loop wasn't broken.
            else:
                continue
            # Inner loop was broken, break the outer.
            break
        else:
            continue

        ### MacOSX have soffice binaries installed in MacOS subdirectory, not program
        unopath = 'error'
        for basis in ( 'basis-link', 'basis', '' ):
            for bin in officebinaries:
                if os.path.isfile(realpath(basepath, basis, 'program', bin)):
                    unopath = realpath(basepath, basis, 'program')
                    officebinary = realpath(unopath, bin)
                    info(3, "Found %s in %s" % (bin, unopath))
                    # Break the inner loop...
                    break
            # Continue if the inner loop wasn't broken.
            else:
                continue
            # Inner loop was broken, break the outer.
            break
        else:
            continue

        ### Windows does not provide or need a URE/lib directory ?
        urepath = ''
        for basis in ( 'basis-link', 'basis', '' ):
            for ure in ( 'ure-link', 'ure', 'URE', '' ):
                if os.path.isfile(realpath(basepath, basis, ure, 'lib', 'unorc')):
                    urepath = realpath(basepath, basis, ure)
                    info(3, "Found %s in %s" % ('unorc', realpath(urepath, 'lib')))
                    # Break the inner loop...
                    break
            # Continue if the inner loop wasn't broken.
            else:
                continue
            # Inner loop was broken, break the outer.
            break

        pythonhome = None
        for home in pythonhomes:
            if glob.glob(realpath(libpath, home)):
                pythonhome = glob.glob(realpath(libpath, home))[0]
                info(3, "Found %s in %s" % (home, pythonhome))
                break

#        if not os.path.isfile(realpath(basepath, program, officebinary)):
#            continue
#        info(3, "Found %s in %s" % (officebinary, realpath(basepath, program)))

#        if not glob.glob(realpath(basepath, basis, program, 'python-core-*')):
#            continue

        for pythonbinary in pythonbinaries:
            if os.path.isfile(realpath(unopath, pythonbinary)):
                info(3, "Found %s in %s" % (pythonbinary, unopath))
                ret.append(Office(basepath, urepath, unopath, officelibrary, officebinary,
                                  realpath(unopath, pythonbinary), pythonhome))
        else:
            info(3, "Considering %s" % basepath)
            ret.append(Office(basepath, urepath, unopath, officelibrary, officebinary,
                              sys.executable, None))
    return ret

def office_environ(office):
    ### Set PATH so that crash_report is found
    os.environ['PATH'] = realpath(office.basepath, 'program') + os.pathsep + os.environ['PATH']

    ### Set UNO_PATH so that "officehelper.bootstrap()" can find soffice executable:
    os.environ['UNO_PATH'] = office.unopath

    ### Set URE_BOOTSTRAP so that "uno.getComponentContext()" bootstraps a complete
    ### UNO environment
    if os.name in ( 'nt', 'os2' ):
        os.environ['URE_BOOTSTRAP'] = 'vnd.sun.star.pathname:' + realpath(office.basepath, 'program', 'fundamental.ini')
    else:
        os.environ['URE_BOOTSTRAP'] = 'vnd.sun.star.pathname:' + realpath(office.basepath, 'program', 'fundamentalrc')

        ### Set LD_LIBRARY_PATH so that "import pyuno" finds libpyuno.so:
        if 'LD_LIBRARY_PATH' in os.environ:
            os.environ['LD_LIBRARY_PATH'] = office.unopath + os.pathsep + \
                                            realpath(office.urepath, 'lib') + os.pathsep + \
                                            os.environ['LD_LIBRARY_PATH']
        else:
            os.environ['LD_LIBRARY_PATH'] = office.unopath + os.pathsep + \
                                            realpath(office.urepath, 'lib')

    if office.pythonhome:
        for libpath in ( realpath(office.pythonhome, 'lib'),
                         realpath(office.pythonhome, 'lib', 'lib-dynload'),
                         realpath(office.pythonhome, 'lib', 'lib-tk'),
                         realpath(office.pythonhome, 'lib', 'site-packages'),
                         office.unopath):
            sys.path.insert(0, libpath)
    else:
        ### Still needed for system python using LibreOffice UNO bindings
        ### Although we prefer to use a system UNO binding in this case
        sys.path.append(office.unopath)

def debug_office():
    if 'URE_BOOTSTRAP' in os.environ:
        print('URE_BOOTSTRAP=%s' % os.environ['URE_BOOTSTRAP'], file=sys.stderr)
    if 'UNO_PATH' in os.environ:
        print('UNO_PATH=%s' % os.environ['UNO_PATH'], file=sys.stderr)
    if 'UNO_TYPES' in os.environ:
        print('UNO_TYPES=%s' % os.environ['UNO_TYPES'], file=sys.stderr)
    print('PATH=%s' % os.environ['PATH'])
    if 'PYTHONHOME' in os.environ:
        print('PYTHONHOME=%s' % os.environ['PYTHONHOME'], file=sys.stderr)
    if 'PYTHONPATH' in os.environ:
        print('PYTHONPATH=%s' % os.environ['PYTHONPATH'], file=sys.stderr)
    if 'LD_LIBRARY_PATH' in os.environ:
        print('LD_LIBRARY_PATH=%s' % os.environ['LD_LIBRARY_PATH'], file=sys.stderr)

def python_switch(office):
    if office.pythonhome:
        os.environ['PYTHONHOME'] = office.pythonhome
        os.environ['PYTHONPATH'] = realpath(office.pythonhome, 'lib') + os.pathsep + \
                                   realpath(office.pythonhome, 'lib', 'lib-dynload') + os.pathsep + \
                                   realpath(office.pythonhome, 'lib', 'lib-tk') + os.pathsep + \
                                   realpath(office.pythonhome, 'lib', 'site-packages') + os.pathsep + \
                                   office.unopath

    os.environ['UNO_PATH'] = office.unopath

    info(3, "-> Switching from %s to %s" % (sys.executable, office.python))
    if os.name in ('nt', 'os2'):
        ### os.execv is broken on Windows and can't properly parse command line
        ### arguments and executable name if they contain whitespaces. subprocess
        ### fixes that behavior.
        ret = subprocess.call([office.python] + sys.argv[0:])
        sys.exit(ret)
    else:

        ### Set LD_LIBRARY_PATH so that "import pyuno" finds libpyuno.so:
        if 'LD_LIBRARY_PATH' in os.environ:
            os.environ['LD_LIBRARY_PATH'] = office.unopath + os.pathsep + \
                                            realpath(office.urepath, 'lib') + os.pathsep + \
                                            os.environ['LD_LIBRARY_PATH']
        else:
            os.environ['LD_LIBRARY_PATH'] = office.unopath + os.pathsep + \
                                            realpath(office.urepath, 'lib')

        try:
            os.execvpe(office.python, [office.python, ] + sys.argv[0:], os.environ)
        except OSError:
            ### Mac OS X versions prior to 10.6 do not support execv in
            ### a process that contains multiple threads.  Instead of
            ### re-executing in the current process, start a new one
            ### and cause the current process to exit.  This isn't
            ### ideal since the new process is detached from the parent
            ### terminal and thus cannot easily be killed with ctrl-C,
            ### but it's better than not being able to autoreload at
            ### all.
            ### Unfortunately the errno returned in this case does not
            ### appear to be consistent, so we can't easily check for
            ### this error specifically.
            ret = os.spawnvpe(os.P_WAIT, office.python, [office.python, ] + sys.argv[0:], os.environ)
            sys.exit(ret)

class Fmt:
    def __init__(self, doctype, name, extension, summary, filter):
        self.doctype = doctype
        self.name = name
        self.extension = extension
        self.summary = summary
        self.filter = filter

    def __str__(self):
        return "%s [.%s]" % (self.summary, self.extension)

    def __repr__(self):
        return "%s/%s" % (self.name, self.doctype)

class FmtList:
    def __init__(self):
        self.list = []

    def add(self, doctype, name, extension, summary, filter):
        self.list.append(Fmt(doctype, name, extension, summary, filter))

    def byname(self, name):
        ret = []
        for fmt in self.list:
            if fmt.name == name:
                ret.append(fmt)
        return ret

    def byextension(self, extension):
        ret = []
        for fmt in self.list:
            if os.extsep + fmt.extension == extension:
                ret.append(fmt)
        return ret

    def bydoctype(self, doctype, name):
        ret = []
        for fmt in self.list:
            if fmt.name == name and fmt.doctype == doctype:
                ret.append(fmt)
        return ret

    def display(self, doctype):
        print("The following list of %s formats are currently available:\n" % doctype, file=sys.stderr)
        for fmt in self.list:
            if fmt.doctype == doctype:
                print("  %-8s - %s" % (fmt.name, fmt), file=sys.stderr)
        print(file=sys.stderr)

fmts = FmtList()

### TextDocument
fmts.add('document', 'docx', 'docx', 'Microsoft Office Open XML', 'Office Open XML Text')
fmts.add('document', 'html', 'html', 'HTML Document (OpenOffice.org Writer)', 'HTML (StarWriter)') ### 3
fmts.add('spreadsheet', 'html', 'html', 'HTML Document (OpenOffice.org Calc)', 'HTML (StarCalc)') ### 7
fmts.add('spreadsheet', 'xls', 'xls', 'Microsoft Excel 97/2000/XP', 'MS Excel 97') ### 12
fmts.add('spreadsheet', 'xlsx', 'xlsx', 'Microsoft Excel 2007/2010 XML', 'Calc MS Excel 2007 XML')
fmts.add('document', 'doc', 'doc', 'Microsoft Word 97/2000/XP', 'MS Word 97') ### 29
### Graphics
fmts.add('graphics', 'gif', 'gif', 'Graphics Interchange Format', 'draw_gif_Export') ### 30
fmts.add('graphics', 'jpg', 'jpg', 'Joint Photographic Experts Group', 'draw_jpg_Export') ### 3
fmts.add('graphics', 'png', 'png', 'Portable Network Graphic', 'draw_png_Export') ### 2
### Presentation
fmts.add('presentation', 'gif', 'gif', 'Graphics Interchange Format', 'impress_gif_Export') ### 18
fmts.add('presentation', 'html', 'html', 'HTML Document (OpenOffice.org Impress)', 'impress_html_Export') ### 43
fmts.add('presentation', 'jpg', 'jpg', 'Joint Photographic Experts Group', 'impress_jpg_Export') ### 19'''
fmts.add('presentation', 'pdf', 'pdf', 'Portable Document Format', 'impress_pdf_Export') ### 23
fmts.add('presentation', 'pptx', 'pptx', 'Microsoft PowerPoint 2007/2010 XML', 'Impress MS PowerPoint 2007 XML') ### 36
fmts.add('presentation', 'ppt', 'ppt', 'Microsoft PowerPoint 97/2000/XP', 'MS PowerPoint 97') ### 36'''

class Options:
    def __init__(self, args):
        self.connection = None
        self.debug = False
        self.doctype = None
        self.exportfilter = []
        self.exportfilteroptions = ""
        self.filenames = []
        self.format = None
        self.importfilter = []
        self.importfilteroptions = ""
        self.listener = False
        self.nolaunch = False
        self.output = None
        self.password = None
        self.pipe = None
        self.port = '2002'
        self.server = '127.0.0.1'
        self.showlist = False
        self.stdout = False
        self.template = None
        self.timeout = 6
        self.verbose = 0
        self.filenames = args
        self.result = None

        ### Enable verbosity
        if self.verbose >= 2:
            self.result = ('Verbosity set to level %d' % self.verbose)

        

        if not self.listener and not self.showlist and self.doctype != 'list' and not self.filenames:
            self.result = ('unoconv: you have to provide a filename as argument')
            self.result = ('Try `unoconv -h\' for more information.')
            sys.exit(255)

        ### Set connection string
        if not self.connection:
            if not self.pipe:
                self.connection = "socket,host=%s,port=%s;urp;StarOffice.ComponentContext" % (self.server, self.port)
#               self.connection = "socket,host=%s,port=%s;urp;" % (self.server, self.port)
            else:
                self.connection = "pipe,name=%s;urp;StarOffice.ComponentContext" % (self.pipe)

        ### Make it easier for people to use a doctype (first letter is enough)
        if self.doctype:
            for doctype in doctypes:
                if doctype.startswith(self.doctype):
                    self.doctype = doctype

        ### Check if the user request to see the list of formats
        if self.showlist or self.format == 'list':
            if self.doctype:
                fmts.display(self.doctype)
            else:
                for t in doctypes:
                    fmts.display(t)
            sys.exit(0)

        ### If no format was specified, probe it or provide it
        if not self.format:
            l = sys.argv[0].split('2')
            if len(l) == 2:
                self.format = l[1]
            else:
                self.format = 'pdf'

    def usage(self):
        print('usage: unoconv [options] file [file2 ..]', file=sys.stderr)


class Convertor:
    def __init__(self,op,office):
        global exitcode, ooproc,product
        unocontext = None
        self.result = None

        ### Do the LibreOffice component dance
        self.context = uno.getComponentContext()
        self.svcmgr = self.context.ServiceManager
        resolver = self.svcmgr.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", self.context)

        ### Test for an existing connection
        info(3, 'Connection type: %s' % op.connection)
        try:
            unocontext = resolver.resolve("uno:%s" % op.connection)
        except NoConnectException as e:
#            info(3, "Existing listener not found.\n%s" % e)
            info(3, "Existing listener not found.")

            if op.nolaunch:
                die(113,op,"Existing listener not found. Unable start listener by parameters. Aborting.")

            ### Start our own OpenOffice instance
            info(3, "Launching our own listener using %s." % office.binary)
            try:
                product = self.svcmgr.createInstance("com.sun.star.configuration.ConfigurationProvider").createInstanceWithArguments("com.sun.star.configuration.ConfigurationAccess", UnoProps(nodepath="/org.openoffice.Setup/Product"))
                if product.ooName not in ('LibreOffice', 'LOdev') or LooseVersion(product.ooSetupVersion) <= LooseVersion('3.3'):
                    ooproc = subprocess.Popen([office.binary, "-headless", "-invisible", "-nocrashreport", "-nodefault", "-nofirststartwizard", "-nologo", "-norestore", "-accept=%s" % op.connection], env=os.environ)
                else:
                    ooproc = subprocess.Popen([office.binary, "--headless", "--invisible", "--nocrashreport", "--nodefault", "--nofirststartwizard", "--nologo", "--norestore", "--accept=%s" % op.connection], env=os.environ)
                info(2, '%s listener successfully started. (pid=%s)' % (product.ooName, ooproc.pid))

                ### Try connection to it for op.timeout seconds (flakky OpenOffice)
                timeout = 0
                while timeout <= op.timeout:
                    ### Is it already/still running ?
                    retcode = ooproc.poll()
                    if retcode != None:
                        info(3, "Process %s (pid=%s) exited with %s." % (office.binary, ooproc.pid, retcode))
                        break
                    try:
                        unocontext = resolver.resolve("uno:%s" % op.connection)
                        break
                    except NoConnectException:
                        time.sleep(0.5)
                        timeout += 0.5
                    except:
                        raise
                else:
                    error("Failed to connect to %s (pid=%s) in %d seconds.\n%s" % (office.binary, ooproc.pid, op.timeout, e))
                    self.result = '6'
            except Exception as e:
                raise
                error("Launch of %s failed.\n%s" % (office.binary, e))
                self.result = '6'

        if not unocontext:
            die(251,op,"Unable to connect or start own listener. Aborting.")
            self.result = '6'
            return 

        ### And some more LibreOffice magic
        unosvcmgr = unocontext.ServiceManager
        self.desktop = unosvcmgr.createInstanceWithContext("com.sun.star.frame.Desktop", unocontext)
        self.cwd = unohelper.systemPathToFileUrl( os.getcwd() )

        ### List all filters
#        self.filters = unosvcmgr.createInstanceWithContext( "com.sun.star.document.FilterFactory", unocontext)
#        for filter in self.filters.getElementNames():
#            print filter
#            #print dir(filter), dir(filter.format)
    def getformat(self, inputfn,op):
        doctype = None

        ### Get the output format from mapping
        if op.doctype:
            outputfmt = fmts.bydoctype(op.doctype, op.format)
        else:
            outputfmt = fmts.byname(op.format)

            if not outputfmt:
                outputfmt = fmts.byextension(os.extsep + op.format)

        ### If no doctype given, check list of acceptable formats for input file ext doctype
        ### FIXME: This should go into the for-loop to match each individual input filename
        if outputfmt:
            inputext = os.path.splitext(inputfn)[1]
            inputfmt = fmts.byextension(inputext)
            if inputfmt:
                for fmt in outputfmt:
                    if inputfmt[0].doctype == fmt.doctype:
                        doctype = inputfmt[0].doctype
                        outputfmt = fmt
                        break
                else:
                    outputfmt = outputfmt[0]
    #       print >>sys.stderr, 'unoconv: format `%s\' is part of multiple doctypes %s, selecting `%s\'.' % (format, [fmt.doctype for fmt in outputfmt], outputfmt[0].doctype)
            else:
                outputfmt = outputfmt[0]

        ### No format found, throw error
        if not outputfmt:
            if doctype:
                print('unoconv: format [%s/%s] is not known to unoconv.' % (op.doctype, op.format), file=sys.stderr)
            else:
                print('unoconv: format [%s] is not known to unoconv.' % op.format, file=sys.stderr)
            die(1,op)

        return outputfmt

    def convert(self, inputfn,op):
        global exitcode

        document = None
        outputfmt = self.getformat(inputfn,op)

        if op.verbose > 0:
            print('Input file:', inputfn, file=sys.stderr)

        if not os.path.exists(inputfn):
            print('unoconv: file `%s\' does not exist.' % inputfn, file=sys.stderr)
            exitcode = 1

        try:
            ### Import phase
            phase = "import"

            ### Load inputfile
            inputprops = UnoProps(Hidden=True, ReadOnly=True, UpdateDocMode=QUIET_UPDATE)

#            if op.password:
#                info = UnoProps(algorithm-name="PBKDF2", salt="salt", iteration-count=1024, hash="hash")
#                inputprops += UnoProps(ModifyPasswordInfo=info)

            ### Cannot use UnoProps for FilterData property
            if op.importfilteroptions:
#                print "Import filter options: %s" % op.importfilteroptions
                inputprops += UnoProps(FilterOptions=op.importfilteroptions)

            ### Cannot use UnoProps for FilterData property
            if op.importfilter:
                inputprops += ( PropertyValue( "FilterData", 0, uno.Any("[]com.sun.star.beans.PropertyValue", tuple( op.importfilter ), ), 0 ), )

            inputurl = unohelper.absolutize(self.cwd, unohelper.systemPathToFileUrl(inputfn))
            document = self.desktop.loadComponentFromURL( inputurl , "_blank", 0, inputprops )

            if not document:
                raise UnoException("The document '%s' could not be opened." % inputurl, None)

            ### Import style template
            phase = "import-style"
            if op.template:
                if os.path.exists(op.template):
                    info(1, "Template file: %s" % op.template)
                    templateprops = UnoProps(OverwriteStyles=True)
                    templateurl = unohelper.absolutize(self.cwd, unohelper.systemPathToFileUrl(op.template))
                    document.StyleFamilies.loadStylesFromURL(templateurl, templateprops)
                else:
                    print('unoconv: template file `%s\' does not exist.' % op.template, file=sys.stderr)
                    exitcode = 1

            ### Update document links
            phase = "update-links"
            try:
                document.updateLinks()
            except AttributeError:
                # the document doesn't implement the XLinkUpdate interface
                pass

            ### Update document indexes
            phase = "update-indexes"
            for ii in range(2):
                # At first update Table-of-Contents.
                # ToC grows, so page numbers grows too.
                # On second turn update page numbers in ToC.
                try:
                    document.refresh()
                    indexes = document.getDocumentIndexes()
                except AttributeError:
                    # the document doesn't implement the XRefreshable and/or
                    # XDocumentIndexesSupplier interfaces
                    break
                else:
                    for i in range(0, indexes.getCount()):
                        indexes.getByIndex(i).update()

            info(1, "Selected output format: %s" % outputfmt)
            info(2, "Selected office filter: %s" % outputfmt.filter)
            info(2, "Used doctype: %s" % outputfmt.doctype)

            ### Export phase
            phase = "export"

            outputprops = UnoProps(FilterName=outputfmt.filter, OutputStream=OutputStream(), Overwrite=True)

            ### Set default filter options
            if op.exportfilteroptions:
     #           print "Export filter options: %s" % op.exportfilteroptions
                outputprops += UnoProps(FilterOptions=op.exportfilteroptions)
            else:
                if outputfmt.filter == 'Text (encoded)':
                    outputprops += UnoProps(FilterOptions="76,LF")

                elif outputfmt.filter == 'Text':
                    outputprops += UnoProps(FilterOptions="76")

                elif outputfmt.filter == 'Text - txt - csv (StarCalc)':
                    outputprops += UnoProps(FilterOptions="44,34,76")

            ### Cannot use UnoProps for FilterData property
            if op.exportfilter:
                outputprops += ( PropertyValue( "FilterData", 0, uno.Any("[]com.sun.star.beans.PropertyValue", tuple( op.exportfilter ), ), 0 ), )

            if not op.stdout:
                (outputfn, ext) = os.path.splitext(inputfn)
                if not op.output:
                    outputfn = outputfn + os.extsep + outputfmt.extension
                elif os.path.isdir(op.output):
                    outputfn = realpath(op.output, os.path.basename(outputfn) + os.extsep + outputfmt.extension)
                elif len(op.filenames) > 1:
                    outputfn = op.output + os.extsep + outputfmt.extension
                else:
                    outputfn = op.output

                outputurl = unohelper.absolutize( self.cwd, unohelper.systemPathToFileUrl(outputfn) )
                info(1, "Output file: %s" % outputfn)
            else:
                outputurl = "private:stream"

            try:
                document.storeToURL(outputurl, tuple(outputprops) )
            except IOException as e:
                raise UnoException("Unable to store document to %s (ErrCode %d)\n\nProperties: %s" % (outputurl, e.ErrCode, outputprops), None)

            phase = "dispose"
            document.dispose()
            document.close(True)

        except SystemError as e:
            error("unoconv: SystemError during %s phase:\n%s" % (phase, e))
            exitcode = 1

        except RuntimeException as e:
            error("unoconv: RuntimeException during %s phase:\nOffice probably died. %s" % (phase, e))
            exitcode = 6

        except DisposedException as e:
            error("unoconv: DisposedException during %s phase:\nOffice probably died. %s" % (phase, e))
            exitcode = 7

        except IllegalArgumentException as e:
            error("UNO IllegalArgument during %s phase:\nSource file cannot be read. %s" % (phase, e))
            exitcode = 8

        except IOException as e:
#            for attr in dir(e): print '%s: %s', (attr, getattr(e, attr))
            error("unoconv: IOException during %s phase:\n%s" % (phase, e.Message))
            exitcode = 3

        except CannotConvertException as e:
#            for attr in dir(e): print '%s: %s', (attr, getattr(e, attr))
            error("unoconv: CannotConvertException during %s phase:\n%s" % (phase, e.Message))
            exitcode = 4

        except UnoException as e:
            if hasattr(e, 'ErrCode'):
                error("unoconv: UnoException during %s phase in %s (ErrCode %d)" % (phase, repr(e.__class__), e.ErrCode))
                exitcode = e.ErrCode
                pass
            if hasattr(e, 'Message'):
                error("unoconv: UnoException during %s phase:\n%s" % (phase, e.Message))
                exitcode = 5
            else:
                error("unoconv: UnoException during %s phase in %s" % (phase, repr(e.__class__)))
                exitcode = 2
                pass

class Listener:
    def __init__(self):
        global product

        info(1, "Start listener on %s:%s" % (op.server, op.port))
        self.context = uno.getComponentContext()
        self.svcmgr = self.context.ServiceManager
        try:
            resolver = self.svcmgr.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", self.context)
            product = self.svcmgr.createInstance("com.sun.star.configuration.ConfigurationProvider").createInstanceWithArguments("com.sun.star.configuration.ConfigurationAccess", UnoProps(nodepath="/org.openoffice.Setup/Product"))
            try:
                unocontext = resolver.resolve("uno:%s" % op.connection)
            except NoConnectException as e:
                pass
            else:
                info(1, "Existing %s listener found, nothing to do." % product.ooName)
                return
            if product.ooName != "LibreOffice" or LooseVersion(product.ooSetupVersion) <= LooseVersion('3.3'):
                subprocess.call([office.binary, "-headless", "-invisible", "-nocrashreport", "-nodefault", "-nologo", "-nofirststartwizard", "-norestore", "-accept=%s" % op.connection], env=os.environ)
            else:
                subprocess.call([office.binary, "--headless", "--invisible", "--nocrashreport", "--nodefault", "--nologo", "--nofirststartwizard", "--norestore", "--accept=%s" % op.connection], env=os.environ)
        except Exception as e:
            error("Launch of %s failed.\n%s" % (office.binary, e))
        else:
            info(1, "Existing %s listener found, nothing to do." % product.ooName)

def error(msg):
    "Output error message"
    print(msg, file=sys.stderr)

def info(level, msg):
    "Output info message"
    if 'op' not in globals():
        pass
    elif op.verbose >= 3 and level >= 3:
        print("DEBUG:", msg, file=sys.stderr)
    elif not op.stdout and level <= op.verbose:
        print(msg, file=sys.stdout)
    elif level <= op.verbose:
        print(msg, file=sys.stderr)

def die(ret, op,msg=None):
    "Print optional error and exit with errorcode"
    global convertor, ooproc, office

    if msg:
        error('Error: %s' % msg)

    ### Did we start our own listener instance ?
    if not op.listener and ooproc and convertor:
        try:
            is_ok = convert.desktop.getCurrentFrame()
        except:
            return 
        ### If there is a GUI now attached to the instance, disable listener
        if is_ok:
            info(2, 'Trying to stop %s GUI listener.' % product.ooName)
            try:
                if product.ooName != "LibreOffice" or product.ooSetupVersion <= 3.3:
                    subprocess.Popen([office.binary, "-headless", "-invisible", "-nocrashreport", "-nodefault", "-nofirststartwizard", "-nologo", "-norestore", "-unaccept=%s" % op.connection], env=os.environ)
                else:
                    subprocess.Popen([office.binary, "--headless", "--invisible", "--nocrashreport", "--nodefault", "--nofirststartwizard", "--nologo", "--norestore", "--unaccept=%s" % op.connection], env=os.environ)
                ooproc.wait()
                info(2, '%s listener successfully disabled.' % product.ooName)
            except Exception as e:
                error("Terminate using %s failed.\n%s" % (office.binary, e))

        ### If there is no GUI attached to the instance, terminate instance
        else:
            info(3, 'Terminating %s instance.' % product.ooName)
            try:
                convertor.desktop.terminate()
            except DisposedException:
                info(2, '%s instance unsuccessfully closed, sending TERM signal.' % product.ooName)
                try:
                    ooproc.terminate()
                except AttributeError:
                    os.kill(ooproc.pid, 15)
            info(3, 'Waiting for %s instance to exit.' % product.ooName)
            ooproc.wait()

        ### LibreOffice processes may get stuck and we have to kill them
        ### Is it still running ?
        if ooproc.poll() == None:
            info(1, '%s instance still running, please investigate...' % product.ooName)
            ooproc.wait()
            info(2, '%s instance unsuccessfully terminated, sending KILL signal.' % product.ooName)
            try:
                ooproc.kill()
            except AttributeError:
                os.kill(ooproc.pid, 9)
            info(3, 'Waiting for %s with pid %s to disappear.' % (ooproc.pid, product.ooName))
            ooproc.wait()

    # allow Python GC to garbage collect pyuno object *before* exit call
    # which avoids random segmentation faults --vpa
    convertor = None
    return ret
   # sys.exit(ret)

def main(op,office):
    global convertor, exitcode
    convertor = None

    try:
        if op.listener:
            listener = Listener()

        if op.filenames:
            convertor = Convertor(op,office)
            if convertor.result != None:
                return convertor.result
            for inputfn in op.filenames:
                convertor.convert(inputfn,op)

    except NoConnectException as e:
        error("unoconv: could not find an existing connection to LibreOffice at %s:%s." % (op.server, op.port))
        return '3'
        if op.connection:
            info(0, "Please start an LibreOffice instance on server '%s' by doing:\n\n    unoconv --listener --server %s --port %s\n\nor alternatively:\n\n    soffice -nologo -nodefault -accept=\"%s\"" % (op.server, op.server, op.port, op.connection))
        else:
            info(0, "Please start an LibreOffice instance on server '%s' by doing:\n\n    unoconv --listener --server %s --port %s\n\nor alternatively:\n\n    soffice -nologo -nodefault -accept=\"socket,host=%s,port=%s;urp;\"" % (op.server, op.server, op.port, op.server, op.port))
            info(0, "Please start an soffice instance on server '%s' by doing:\n\n    soffice -nologo -nodefault -accept=\"socket,host=127.0.0.1,port=%s;urp;\"" % (op.server, op.port))
        exitcode = 1
#    except UnboundLocalError:
#        die(252, "Failed to connect to remote listener.")
    except OSError:
        error("Warning: failed to launch Office suite. Aborting.")
        return '4'
    return True

### Now that we have found a working pyuno library, let's import some classes
import uno, unohelper
from com.sun.star.beans import PropertyValue
from com.sun.star.connection import NoConnectException
from com.sun.star.document.UpdateDocMode import QUIET_UPDATE
from com.sun.star.lang import DisposedException, IllegalArgumentException
from com.sun.star.io import IOException, XOutputStream
from com.sun.star.script import CannotConvertException
from com.sun.star.uno import Exception as UnoException
from com.sun.star.uno import RuntimeException

    ### And now that we have those classes, build on them
class OutputStream( unohelper.Base, XOutputStream ):
    def __init__( self ):
        self.closed = 0

    def closeOutput(self):
        self.closed = 1

    def writeBytes( self, seq ):
        sys.stdout.write( seq.value )

    def flush( self ):
        pass

def UnoProps(**args):
    props = []
    for key in args:
        prop = PropertyValue()
        prop.Name = key
        prop.Value = args[key]
        props.append(prop)
    return tuple(props)

### Main entrance
def output(filepath):
    exitcode = 0

    #info(3, 'sysname=%s, platform=%s, python=%s, python-version=%s' % (os.name, sys.platform, sys.executable, sys.version))

    for of in find_offices():
        if of.python != sys.executable and not sys.executable.startswith(of.basepath):
            python_switch(of)
            return '1'
        office_environ(of)
#        debug_office()
        try:
            import uno, unohelper
            office = of
          
            break
        except:
#            debug_office()
            #print("unoconv: Cannot find a suitable pyuno library and python binary combination in %s" % of, file=sys.stderr)
            #print("ERROR:", sys.exc_info()[1], file=sys.stderr)
            #print(file=sys.stderr)
            return '2'
    else:
#        debug_office()
        #print("unoconv: Cannot find a suitable office installation on your system.", file=sys.stderr)
        #print("ERROR: Please locate your office installation and send your feedback to:", file=sys.stderr)
        #print("       http://github.com/dagwieers/unoconv/issues", file=sys.stderr)
        return '1'
        sys.exit(1)
    File =[]
    File_add = filepath
    File.append(File_add)
    op = Options(File)

    if op.result !=None:
        return op.result

    '''
    info(2, "Using office base path: %s" % office.basepath)
    info(2, "Using office binary path: %s" % office.unopath)
    '''
    try:
        if main(op,office):
            pass
        else:
            return '4'
    except KeyboardInterrupt as e:
        die(6, op,'Exiting on user request')

    ans = die(exitcode,op)
    if ans!=0:
        return '5'
    return ans


    
