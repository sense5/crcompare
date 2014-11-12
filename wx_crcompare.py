#!/usr/bin/env python
u'''
#App Name: crcompare.py
#Version: 1.0 
#Author: ray.h(torkuu@gmail.com)
#Compile_Env: python 3.3.2
#Last_Modify: 20140117.1201
'''

import re
import copy
from io import open
import wx
import wx.xrc
import wx.grid


class FileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window
    def OnDropFiles(self,  x,  y, fileNames):
        open1 = getallcontent()
        open1.txtfile(fileNames[0])
        self.window.SetValue('')
        for a in open1.result:
            self.window.AppendText(a)

class getallcontent:
    #Variable Defination Area

    def __init__(self):
        self.result = []
        pass

    def txtfile(self, filename):
        a = open(filename, 'rU')
        self.result = a.readlines()

    def wxtext(self, wxtext):
        clNumber = 0
        NoLine = wxtext.GetNumberOfLines()
        while clNumber < NoLine:
            self.result.append(wxtext.GetLineText(clNumber) + u'\n')
            clNumber = clNumber + 1
        

class crMain ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Cisco Routing Table Comparison Tool 1.0 (torkuu@gmail.com)", pos = wx.DefaultPosition, size = wx.Size( 800,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
        
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
        
        bSizer5 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Route1", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
        self.m_staticText1.Wrap( -1 )
        bSizer5.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.file1 = wx.TextCtrl( self, wx.ID_ANY, u"Paste 'show ip route', or drag your saved output file here.", wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_NOHIDESEL )
        self.file1.SetMaxLength( 0 ) 
        bSizer5.Add( self.file1, 1, wx.ALL|wx.EXPAND, 5 )
        
        #Ctrl+A function
        self.file1.Bind(wx.EVT_CHAR, self.OnSelectAll1)
        
        #drop funtion
        dropTarget = FileDropTarget(self.file1)
        self.file1.SetDropTarget( dropTarget )
        #----------------------
        
        bSizer11.Add( bSizer5, 1, wx.EXPAND, 5 )
        
        bSizer6 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Route2", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
        self.m_staticText2.Wrap( -1 )
        bSizer6.Add( self.m_staticText2, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.file2 = wx.TextCtrl( self, wx.ID_ANY, u"Paste 'show ip route', or drag your saved output file here.", wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_NOHIDESEL )
        self.file2.SetMaxLength( 0 ) 
        bSizer6.Add( self.file2, 1, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
        
        #Ctrl+A function
        self.file2.Bind(wx.EVT_CHAR, self.OnSelectAll2)
        
        #drop funtion
        dropTarget = FileDropTarget(self.file2)
        self.file2.SetDropTarget( dropTarget )
        #----------------------
        
        bSizer11.Add( bSizer6, 1, wx.EXPAND, 5 )
        
        
        bSizer1.Add( bSizer11, 1, wx.EXPAND, 5 )
        
        self.m_button2 = wx.Button( self, wx.ID_ANY, u"Compare", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.m_button2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        self.SetSizer( bSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.m_button2.Bind( wx.EVT_BUTTON, self.StartCompare )
    
    def __del__( self ):
        pass
    
    def OnSelectAll1(self, evt):
        keyInput = evt.GetKeyCode()
        if keyInput == 1:
            self.file1.SelectAll()
        evt.Skip()
    
    def OnSelectAll2(self, evt):
        keyInput = evt.GetKeyCode()
        if keyInput == 1:
            self.file2.SelectAll()
        evt.Skip()
        
    def StartCompare( self, event ):
        object1 = getallcontent()
        object1.wxtext(self.file1)
        parse1 = parseroute()
        parse1.main(object1.result)
        parse1.summary()
        print u'file1 summary\n', parse1.routecount, u'\n', parse1.rtypesummary
        object2 = getallcontent()
        object2.wxtext(self.file2)
        parse2 = parseroute()
        parse2.main(object2.result)
        parse2.summary()
        print u'file2 summary\n', parse2.routecount, u'\n', parse2.rtypesummary
    
    
        crroute = compareroute()
        crroute.main(parse1.result, parse2.result)
    
        print u'Different Route\n', crroute.dfroute
        print u'Disappeared Route\n', crroute.msroute
        print u'NewAdded Route\n', crroute.addroute
        
        app2 = wx.App(False)
        frame2 = crResult(wx.GetApp().TopWindow)
        frame2.showsummary(parse1.routecount, parse1.rtypesummary, parse2.routecount, parse2.rtypesummary)
        frame2.showroute(crroute.dfroute, crroute.msroute, crroute.addroute)
        frame2.setpanellabel(crroute.dfroute, crroute.msroute, crroute.addroute)
        frame2.autosizegrid()
        frame2.Show()
        app2.MainLoop()


class crResult ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Compare Result", pos = wx.DefaultPosition, size = wx.Size( 657,533 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
                
        bSizer12 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_notebook5 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        
        self.m_panel1 = wx.Panel( self.m_notebook5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer9 = wx.BoxSizer( wx.VERTICAL )
        
        self.rsummary = wx.grid.Grid( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        
        # Grid
        self.rsummary.CreateGrid( 0, 3 )
        self.rsummary.EnableEditing( False )
        self.rsummary.EnableGridLines( True )
        self.rsummary.EnableDragGridSize( True )
        self.rsummary.SetMargins( 0, 0 )
        self.setcollabel3(self.rsummary)
        
        # Columns
        self.rsummary.EnableDragColMove( False )
        self.rsummary.EnableDragColSize( True )
        self.rsummary.SetColLabelSize( 30 )
        self.rsummary.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        
        # Rows
        self.rsummary.EnableDragRowSize( True )
        self.rsummary.SetRowLabelSize( 80 )
        self.rsummary.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        
        # Label Appearance
        
        # Cell Defaults
        self.rsummary.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        bSizer9.Add( self.rsummary, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        self.m_panel1.SetSizer( bSizer9 )
        self.m_panel1.Layout()
        bSizer9.Fit( self.m_panel1 )
        self.m_notebook5.AddPage( self.m_panel1, u"Summary", True )
        
        
        self.m_panel2 = wx.Panel( self.m_notebook5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer16 = wx.BoxSizer( wx.VERTICAL )
        
        self.dfroute = wx.grid.Grid( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        
        # Grid
        self.dfroute.CreateGrid( 0, 8 )
        self.dfroute.EnableEditing( False )
        self.dfroute.EnableGridLines( True )
        self.dfroute.EnableDragGridSize( True )
        self.dfroute.SetMargins( 0, 0 )
        self.setcollabel2(self.dfroute)
        
        
        # Columns
        self.dfroute.EnableDragColMove( False )
        self.dfroute.EnableDragColSize( True )
        self.dfroute.SetColLabelSize( 30 )
        self.dfroute.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        
        # Rows
        self.dfroute.EnableDragRowSize( True )
        self.dfroute.SetRowLabelSize( 80 )
        self.dfroute.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        
        # Label Appearance
        
        # Cell Defaults
        self.dfroute.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        bSizer16.Add( self.dfroute, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        self.m_panel2.SetSizer( bSizer16 )
        self.m_panel2.Layout()
        bSizer16.Fit( self.m_panel2 )
        self.m_notebook5.AddPage( self.m_panel2, u"Changed Route", False )
        self.m_panel5 = wx.Panel( self.m_notebook5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer17 = wx.BoxSizer( wx.VERTICAL )
        
        self.msroute = wx.grid.Grid( self.m_panel5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        
        # Grid
        self.msroute.CreateGrid( 0, 7 )
        self.msroute.EnableEditing( False )
        self.msroute.EnableGridLines( True )
        self.msroute.EnableDragGridSize( True )
        self.msroute.SetMargins( 0, 0 )
        self.setcollabel(self.msroute)
        
        # Columns
        self.msroute.EnableDragColMove( False )
        self.msroute.EnableDragColSize( True )
        self.msroute.SetColLabelSize( 30 )
        self.msroute.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        
        # Rows
        self.msroute.EnableDragRowSize( True )
        self.msroute.SetRowLabelSize( 80 )
        self.msroute.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        
        # Label Appearance
        
        # Cell Defaults
        self.msroute.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        bSizer17.Add( self.msroute, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        self.m_panel5.SetSizer( bSizer17 )
        self.m_panel5.Layout()
        bSizer17.Fit( self.m_panel5 )
        self.m_notebook5.AddPage( self.m_panel5, u"Disappeared Route", False )
        self.m_panel6 = wx.Panel( self.m_notebook5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer18 = wx.BoxSizer( wx.VERTICAL )
        
        self.addroute = wx.grid.Grid( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        
        # Grid
        self.addroute.CreateGrid( 0, 7 )
        self.addroute.EnableEditing( False )
        self.addroute.EnableGridLines( True )
        self.addroute.EnableDragGridSize( True )
        self.addroute.SetMargins( 0, 0 )
        self.setcollabel(self.addroute)
        
        # Columns
        self.addroute.EnableDragColMove( False )
        self.addroute.EnableDragColSize( True )
        self.addroute.SetColLabelSize( 30 )
        self.addroute.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        
        # Rows
        self.addroute.EnableDragRowSize( True )
        self.addroute.SetRowLabelSize( 80 )
        self.addroute.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        
        # Label Appearance
        
        # Cell Defaults
        self.addroute.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        bSizer18.Add( self.addroute, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        self.m_panel6.SetSizer( bSizer18 )
        self.m_panel6.Layout()
        bSizer18.Fit( self.m_panel6 )
        self.m_notebook5.AddPage( self.m_panel6, u"New_Added Route", False )
        
        bSizer12.Add( self.m_notebook5, 1, wx.EXPAND |wx.ALL, 5 )
        
        
        self.SetSizer( bSizer12 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
    
    def __del__( self ):
        pass
    
    
    def setcollabel(self, LV_grid):
        #Variable Defination Area
        collabels = ['Protocol', 'Type', 'Subnet', 'AD', 'Cost', 'Nexthop', 'Interface']
        count = 0
        #Code Start Point
        for a in collabels:
            LV_grid.SetColLabelValue(count, a)
            count = count + 1
    
    def setcollabel2(self, LV_grid):
        '''Set colume label for self.dfroute'''
        #Variable Defination Area
        collabels = ['RouteLabel', 'Protocol', 'Type', 'Subnet', 'AD', 'Cost', 'Nexthop', 'Interface']
        count = 0
        #Code Start Point
        for a in collabels:
            LV_grid.SetColLabelValue(count, a)
            count = count + 1    
    
    def setcollabel3(self, LV_grid):
        '''Set colume label for self.rsummary'''
        #Variable Defination Area
        collabels = ['Protocol', 'Route1', 'Route2']
        count = 0
        #Code Start Point
        for a in collabels:
            LV_grid.SetColLabelValue(count, a)
            count = count + 1   
    
    def showsummary(self, route1amount, route1summary, route2amount, route2summary):
        #Variable Defination Area
        currentrow = 0  #define Grid current row number
        #Code Start Point
        #protocol summary
        for key1,value1 in route1summary.iteritems():
            self.rsummary.AppendRows(numRows=1)
            currentrow = self.rsummary.GetNumberRows() - 1
            self.rsummary.SetRowLabelValue(currentrow, str(self.rsummary.GetNumberRows()))
            self.rsummary.SetCellValue(currentrow, 0, key1)
            self.rsummary.SetCellValue(currentrow, 1, value1)
            if key1 in route2summary:
                self.rsummary.SetCellValue(currentrow, 2, route2summary[key1])
        
        for a in (set(route2summary) - set(route1summary)):
            self.rsummary.AppendRows(numRows=1)
            currentrow = self.rsummary.GetNumberRows() - 1
            self.rsummary.SetRowLabelValue(currentrow, str(self.rsummary.GetNumberRows()))
            self.rsummary.SetCellValue(currentrow, 0, a)
            self.rsummary.SetCellValue(currentrow, 2, route2summary[a])
        
        #route amount summary
        self.rsummary.AppendRows(numRows=1)
        currentrow = self.rsummary.GetNumberRows() - 1
        self.rsummary.SetRowLabelValue(currentrow, 'Summary')
        self.rsummary.SetCellValue(currentrow, 1, str(route1amount))
        self.rsummary.SetCellValue(currentrow, 2, str(route2amount))

    
        
    def setroutewcolour(self, gridobject, gridroute):
        #Variable Defination Area
        currentrow = 0  #define Grid current row number 
        currentline = 0 #define gridroute current processing line
        routelabel = 0
        #Code Start Point
        for b in gridroute:
            # create route label number
            currentline = currentline + 1
            if (currentline % 2) == 0:
                routelabel = 2
            else:
                routelabel = 1
            #--->set route start
            for c in range(1, int((len(b)-3)/4+1)):
                gridobject.AppendRows(numRows=1)
                currentrow = gridobject.GetNumberRows() - 1
                gridobject.SetRowLabelValue(currentrow, str(gridobject.GetNumberRows()))
                if c == 1:
                    gridobject.SetCellValue(currentrow, 0, 'Route{0}'.format(routelabel))
                    gridobject.SetCellValue(currentrow, 1, b['rtype'])
                    gridobject.SetCellValue(currentrow, 2, b['srtype'])
                    gridobject.SetCellValue(currentrow, 3, b['subnet'])
                gridobject.SetCellValue(currentrow, 4, b['ad{0}'.format(c)])
                gridobject.SetCellValue(currentrow, 5, b['cost{0}'.format(c)])
                gridobject.SetCellValue(currentrow, 6, b['nexthop{0}'.format(c)])
                gridobject.SetCellValue(currentrow, 7, b['interface{0}'.format(c)])  
                if routelabel == 2:
                    for d in range(0, 8):
                        gridobject.SetCellBackgroundColour(currentrow, d, 'red')  
 

    def setroute(self, gridobject, gridroute):
        #Variable Defination Area
        currentrow = 0
        #Code Start Point
        for b in gridroute:
            for c in range(1, int((len(b)-3)/4+1)):
                gridobject.AppendRows(numRows=1)
                currentrow = gridobject.GetNumberRows() - 1
                gridobject.SetRowLabelValue(currentrow, str(gridobject.GetNumberRows()))
                if c == 1:
                    gridobject.SetCellValue(currentrow, 0, b['rtype'])
                    gridobject.SetCellValue(currentrow, 1, b['srtype'])
                    gridobject.SetCellValue(currentrow, 2, b['subnet'])
                gridobject.SetCellValue(currentrow, 3, b['ad{0}'.format(c)])
                gridobject.SetCellValue(currentrow, 4, b['cost{0}'.format(c)])
                gridobject.SetCellValue(currentrow, 5, b['nexthop{0}'.format(c)])
                gridobject.SetCellValue(currentrow, 6, b['interface{0}'.format(c)])
                

        
    def showroute(self, LV_dfroute, LV_msroute, LV_addroute):
        self.setroutewcolour(self.dfroute, LV_dfroute)
        self.setroute(self.msroute, LV_msroute)
        self.setroute(self.addroute, LV_addroute)

    def setpanellabel(self, LV_dfroute, LV_msroute, LV_addroute):
        self.m_notebook5.SetPageText(1, 'Changed Route ({0})'.format(len(LV_dfroute)/2))
        self.m_notebook5.SetPageText(2, 'Disappeared Route ({0})'.format(len(LV_msroute)))
        self.m_notebook5.SetPageText(3, 'New_Added Route ({0})'.format(len(LV_addroute)))
        
    def autosizegrid(self):
        self.dfroute.AutoSize()
        self.msroute.AutoSize()
        self.addroute.AutoSize()
        self.rsummary.AutoSize()
        self.SetSizeWH(660, 540)
        
        

    

class parseroute(object):
    #Variable Defination Area
    CV_rtype = ur'^.{2}'
    CV_srtype = ur'(?<=^.{2}).{2}'
    CV_subnet = ur'(\d{1,3}\.){3}\d{1,3}/?\d{0,2}'
    CV_ad = ur'(?<=\[)\d+'
    CV_cost = ur'\d+(?=\])'
    CV_nexthop = ur'(?<=via\s)(\d{1,3}\.){3}\d{1,3}/?\d{0,2}'
    CV_interface = ur'(?<=, )\b[A-Z].*$'

    def __init__(self):
        #Variable Defination Area
        self.result = []    #save parsed result
        self.routecount = 0    #count routes amount
        self.rtypesummary = {}    #count rtype
        #Code Start Point
    
    def parse_element(self, rline):
        u'''parese route elements'''
        #Variable Defination Area
        LV_elements = {}    #save route elements (local variable)
        #Code Start Point
        # route type
        if re.search(parseroute.CV_rtype, rline):
            LV_elements[u'rtype'] = (re.search(parseroute.CV_rtype, rline).group()).strip(u' ')
        else:
            LV_elements[u'rtype'] = u'ERROR'
        # route sub type
        if re.search(parseroute.CV_srtype, rline):
            LV_elements[u'srtype'] = (re.search(parseroute.CV_srtype, rline).group()).strip(u' ')
        else:
            LV_elements[u'srtype'] = u'ERROR'
        # route subnet
        if re.search(parseroute.CV_subnet, rline):
            LV_elements[u'subnet'] = (re.search(parseroute.CV_subnet, rline).group().strip(u' '))
        else:
            LV_elements[u'subnet'] = u'ERROR'
        # route ad
        if re.search(parseroute.CV_ad, rline):
            LV_elements[u'ad1'] = (re.search(parseroute.CV_ad, rline).group().strip(u' '))
        else:
            LV_elements[u'ad1'] = u''
        # route cost
        if re.search(parseroute.CV_cost, rline):
            LV_elements[u'cost1'] = (re.search(parseroute.CV_cost, rline).group().strip(u' '))
        else:
            LV_elements[u'cost1'] = u''
        # route nexthop
        if re.search(parseroute.CV_nexthop, rline):
            LV_elements[u'nexthop1'] = (re.search(parseroute.CV_nexthop, rline).group().strip(u' '))
        else:
            LV_elements[u'nexthop1'] = u''
        # route interface
        if re.search(parseroute.CV_interface, rline):
            LV_elements[u'interface1'] = (re.search(parseroute.CV_interface, rline).group().strip(u' '))
        else:
            LV_elements[u'interface1'] = u''

        return LV_elements

    def summary(self):
        u'''Get route summary'''
        #Variable Defination Area
        LV_rtype = []
        #Code Start Point
        self.routecount = len(self.result)
        for a in self.result:
            if a[u'rtype'] != 'ERROR':
                if a[u'rtype'] in LV_rtype:
                    self.rtypesummary[a[u'rtype']] = unicode(int(self.rtypesummary[a[u'rtype']]) + 1)
                else:
                    self.rtypesummary[a[u'rtype']] = u'1'
                    LV_rtype.append(a[u'rtype'])

    def main(self, o_routes):
        u'''Class main funtion'''
        #Variable Defination Area
        routes = []        #save all parsed routes
        elements = {}    #save parsed route elements
        nlocation = 0    #save normal route location in routes[]
        mroutecount = 0    #new normal route start at 2, new wraped normal route (without nexthop and interface) start at 1, split route add count for addictive variable
        #Code Start Point
        
        for b in o_routes:
            if re.search(ur'^\b[a-zA-Z]{1}\b\*?', b):
                #parse route element
                elements = self.parse_element(b)
                if elements['rtype'] == 'ERROR' or elements['srtype'] == 'ERROR' or elements['subnet'] == 'ERROR':
                    continue
                routes = routes + [copy.deepcopy(elements)]
                nlocation = len(routes)-1
                if elements[u'nexthop1'] == u'' and elements[u'interface1'] == u'':
                    mroutecount = 1
                else:
                    mroutecount = 2
            elif re.search(ur'\s*\[.*', b):
                #parse route element
                elements = self.parse_element(b)
                #add wraped routes and ECMP routes element to first normal route
                routes[nlocation][u'ad{0}'.format(mroutecount)] = elements[u'ad1']
                routes[nlocation][u'cost{0}'.format(mroutecount)] = elements[u'cost1']
                routes[nlocation][u'nexthop{0}'.format(mroutecount)] = elements[u'nexthop1']
                routes[nlocation][u'interface{0}'.format(mroutecount)] = elements[u'interface1']
                mroutecount = mroutecount + 1
            else:
                pass
        self.result = routes
        


class compareroute(object):
    #Variable Defination Area
    def __init__(self):
        #Variable Defination Area
        self.dfroute = []    #Different route 
        self.msroute = []    #Disappeared(missed) route
        self.addroute = []    #NewAdded route
        #Code Start Point
    
    def compareroute(self, route1, route2, flag1, flag2):
        #VAR flag1 for cancelling dfroute comparison.Optimize algrithm speed. 1 make dfroute comparison, 0 do not.
        #VAR flag2 for transmitting msroute to different variable. 1 for msroute. 0 for nwroute.
        for a in route1:
            count = 0
            for b in route2:
                if a[u'subnet'] == b[u'subnet']:
                    if flag1 and not(a == b):
                        self.dfroute = self.dfroute + [copy.deepcopy(a)]
                        self.dfroute = self.dfroute + [copy.deepcopy(b)]
                    count = 1
                    continue
            if count == 0:
                if flag2:
                    self.msroute = self.msroute + [copy.deepcopy(a)]
                else:
                    self.addroute = self.addroute + [copy.deepcopy(a)]
    
    def main(self, route1, route2):
        u'''Class main funtion'''
        #Variable Defination Area
        #Code Start Point
        self.compareroute(route1, route2, 1, 1)
        self.compareroute(route2, route1, 0, 0)

        


def main():
    u'''app main funtion'''

    
    app1 = wx.App(False)
    frame1 = crMain(None)
    frame1.Show()
    app1.MainLoop()

 




    
if __name__ == u'__main__':  
    main()



