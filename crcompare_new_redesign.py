#!/usr/bin/env python
'''
#App Name: crcompare.py
#Version: 1.0 
#Author: ray.h(torkuu@gmail.com)
#Compile_Env: python 3.3.2
#Last_Modify: 20140114.1723
'''
import re
import copy

class getallcontent:
    #Variable Defination Area

    def __init__(self):
        self.result = []
        pass

    def txtfile(self, filename):
        a = open(filename, 'rU')
        self.result = a.readlines()

    def wxtextctrl(self, wxtext):

        pass

class parseroute:
    #Variable Defination Area
    CV_rtype = r'^.{2}'
    CV_srtype = r'(?<=^.{2}).{2}'
    CV_subnet = r'(\d{1,3}\.){3}\d{1,3}/?\d{0,2}'
    CV_ad = r'(?<=\[)\d+'
    CV_cost = r'\d+(?=\])'
    CV_nexthop = r'(?<=via\s)(\d{1,3}\.){3}\d{1,3}/?\d{0,2}'
    CV_interface = r'(?<=, )\b[A-Z].*$'

    def __init__(self):
        #Variable Defination Area
        self.result = []    #save parsed result
        self.routecount = 0    #count routes amount
        self.rtypesummary = {}    #count rtype
        #Code Start Point
    
    def parse_element(self, rline):
        '''parese route elements'''
        #Variable Defination Area
        LV_elements = {}    #save route elements (local variable)
        #Code Start Point
        # route type
        LV_elements['rtype'] = (re.search(parseroute.CV_rtype, rline).group()).strip(' ')
        # route sub type
        LV_elements['srtype'] = re.search(parseroute.CV_srtype, rline).group().strip(' ')
        # route subnet
        if re.search(parseroute.CV_subnet, rline):
            LV_elements['subnet'] = re.search(parseroute.CV_subnet, rline).group()
        else:
            LV_elements['subnet'] = 'ERROR'
        # route ad
        if re.search(parseroute.CV_ad, rline):
            LV_elements['ad1'] = re.search(parseroute.CV_ad, rline).group()
        else:
            LV_elements['ad1'] = ''
        # route cost
        if re.search(parseroute.CV_cost, rline):
            LV_elements['cost1'] = re.search(parseroute.CV_cost, rline).group()
        else:
            LV_elements['cost1'] = ''
        # route nexthop
        if re.search(parseroute.CV_nexthop, rline):
            LV_elements['nexthop1'] = re.search(parseroute.CV_nexthop, rline).group()
        else:
            LV_elements['nexthop1'] = ''
        # route interface
        if re.search(parseroute.CV_interface, rline):
            LV_elements['interface1'] = re.search(parseroute.CV_interface, rline).group()
        else:
            LV_elements['interface1'] = ''

        return LV_elements

    def summary(self):
        '''Get route summary'''
        #Variable Defination Area
        LV_rtype = []
        #Code Start Point
        self.routecount = len(self.result)
        for a in self.result:
            if a['rtype'] in LV_rtype:
                self.rtypesummary[a['rtype']] = str(int(self.rtypesummary[a['rtype']]) + 1)
            else:
                self.rtypesummary[a['rtype']] = '1'
                LV_rtype.append(a['rtype'])

    def main(self, o_routes):
        '''Class main funtion'''
        #Variable Defination Area
        routes = []        #save all parsed routes
        elements = {}    #save parsed route elements
        nlocation = 0    #save normal route location in routes[]
        mroutecount = 0    #new normal route start at 2, new wraped normal route (without nexthop and interface) start at 1, split route add count for addictive variable
        #Code Start Point
        for b in o_routes:
            if re.search(r'^\b[a-zA-Z]{1}\b\*?', b):
                #parse route element
                elements = self.parse_element(b)
                routes = routes + [copy.deepcopy(elements)]
                nlocation = len(routes)-1
                if elements['nexthop1'] == '' and elements['interface1'] == '':
                    mroutecount = 1
                else:
                    mroutecount = 2
            elif re.search(r'\s*\[.*', b):
                #parse route element
                elements = self.parse_element(b)
                #add wraped routes and ECMP routes element to first normal route
                routes[nlocation]['ad{0}'.format(mroutecount)] = elements['ad1']
                routes[nlocation]['cost{0}'.format(mroutecount)] = elements['cost1']
                routes[nlocation]['nexthop{0}'.format(mroutecount)] = elements['nexthop1']
                routes[nlocation]['interface{0}'.format(mroutecount)] = elements['interface1']
                mroutecount = mroutecount + 1
            else:
                pass
        self.result = routes
        


class compareroute:
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
                if a['subnet'] == b['subnet']:
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
        '''Class main funtion'''
        #Variable Defination Area
        #Code Start Point
        self.compareroute(route1, route2, 1, 1)
        self.compareroute(route2, route1, 0, 0)

        


def main():
    '''app main funtion'''
    file1 = 'aaa.txt'
    file2 = 'aaa1.txt'

    object1 = getallcontent()
    object1.txtfile(file1)
    parse1 = parseroute()
    parse1.main(object1.result)
    parse1.summary()
    print ('file1 summary\n', parse1.routecount, '\n', parse1.rtypesummary)
    object2 = getallcontent()
    object2.txtfile(file2)
    parse2 = parseroute()
    parse2.main(object2.result)
    parse2.summary()
    print ('file2 summary\n', parse2.routecount, '\n', parse2.rtypesummary)


    crroute = compareroute()
    crroute.main(parse1.result, parse2.result)

    print ('Different Route\n', crroute.dfroute)
    print ('Disappeared Route\n', crroute.msroute)
    print ('NewAdded Route\n', crroute.addroute)



    
if __name__ == '__main__':  
    main()


