


import inspect
import textwrap

import lxml.etree as ET


'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
THERE IS ONLY NEED TO EDIT THE CONTENT BETWEEN THE '#----------' DELIMITERS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''


#-------------------------------------------------------------------------------
#import here the functions that your script is using
from test import print_something

#enter the name you want for your Plugin inside ParaView
name = "Print Something" 

#   ...and the name of the xml
outputName = "print_something.xml"

#   ...and the type of the plugin ("sources" or "filters")
pluginType = "sources"
#-------------------------------------------------------------------------------



def void():{}       #our hero
    

#the root of the XML tree:
root = ET.Element("ServerManagerConfiguration")

#PV stuff
proxy_group = ET.Element("ProxyGroup", name=pluginType)

#More PV stuff. every added element will be a branch of "SourceProxy".
source_proxy = ET.Element("SourceProxy", 
{
    "name":  name,
    "class": "vtkPythonProgrammableFilter",
    "label": name,
})

#this fields are compulsory if we want to make a filter
input_property = ET.Element("InputProperty",
{
    "name":         "Input",
    "command":      "SetInputConnection"
})
proxy_group_domain = ET.Element("ProxyGroupDomain",
{
    "name":         "groups"
})
sources = ET.Element("Group",
{
    "name":         "sources"
})
filters = ET.Element("Group",
{
    "name":         "filters"
})

#let's merge the 4 elements from above into "input_property"
proxy_group_domain.append(sources)
proxy_group_domain.append(filters)
input_property.append(proxy_group_domain)




#those lists will be filled with the "PV blanks" that we will add.
STRING = []             
INT = []                
INT_ENUM = []  
STR_ENUM = []         
INT_SLIDERS = []
BOOL = []
SCRIPT = None
SCRIPT_RI = None
REFRESH = None
CATEGORY = None



#Each function (except the first one) has the same structure. Adding new ones 
#or editing the existing is very simple.

def _function_source(function): #TODO: remove the need of using "inspect" and
                                #textwrap packages

    # this function reads the source code of the input function and converts it
    # into a string, in order to write it on the XML file.     
    #
    # the source of this function function has been taken from Shuhaowu's
    # reprository on GitHub, https://github.com/shuhaowu/pvpyfilter.            

    lines = inspect.getsourcelines(function)[0]
    found_def_start = False
    found_def_end = False
    for i, line in enumerate(lines):
        line = line.strip()
        if not found_def_start:
            if line.startswith("def"):
                found_def_start = True

        if found_def_start and not found_def_end:
            if line.endswith(":"):
                found_def_end = True

        if found_def_start and found_def_end:
            break

    return textwrap.dedent("".join(lines[i + 1:]))

def AddString(name, default, label=None, documentation = '', visibility = "default"):
    #"label":            - the text that will appear next to the blank (string)
    #"name":            - the name of the variable defined in the imported 
    #                   function, linked with that field.
    #"default":         - the default value (string)
    #"documentation":   - some help that will be displayed when the cursor is on
    #                   the blank (string)
    #"visibility":      - Set to "advanced" if you want this field to appear 
    #                   only when the 'gear' is pressed
    #···········································································
    if label is None: label = name

    string = ET.Element("StringVectorProperty", 
    {
    "name":               name,
    "command":            "SetParameter",
    "label":              label,
    "number_of_elements": "1",
    "default_values":     default,
    "initial_string":     name,
    "panel_visibility":   visibility
    })

    doc = ET.Element("Documentation",{})
    doc.text = documentation

    if documentation != '': string.append(doc)
    STRING.append(string)

def AddInt(name, default, label=None, documentation = '', visibility = "default"):
    #"label":           - the text that will appear next to the blank (string)
    #"name":            - the name of the variable defined in the imported 
    #                   function, linked with that field.    
    #"default":         - the default value (string)
    #"documentation":   - some help that will be displayed when the cursor is on
    #                   the blank (string)
    #"visibility":      - Set to "advanced" if you want this field to appear 
    #                   only when the 'gear' is pressed
    #···········································································
    
    if label is None: label = name
    
    number = ET.Element("IntVectorProperty", 
    {
    "name":               name,
    "command":            "SetParameter",
    "label":              label,
    "number_of_elements": "1",
    "default_values":     default,
    "initial_string":     name,
    "panel_visibility":   visibility
    })

    doc = ET.Element("Documentation",{})
    doc.text = documentation

    if documentation != '': number.append(doc)
    INT.append(number)

def AddRefreshButton(name):
    #"name":            - the name that will appear in the button (string)
    #···········································································
    button = ET.Element("Property", 
    {
        "name":             name,
        "command":          "Modified",
        "panel_widget":     "command_button",
        "width":            "5"
    })

    global REFRESH
    REFRESH = button

def AddBool(name, default, label=None, documentation = '', visibility = "default"):
    #"label":           - the text that will appear next to the blank (string)
    #"name":            - the name of the variable defined in the imported 
    #                   function, linked with that field.    
    #"default":         - the default value (string)
    #"documentation":   - some help that will be displayed when the cursor is on
    #                   the blank (string)
    #"visibility":      - Set to "advanced" if you want this field to appear 
    #                   only when the 'gear' is pressed
    #···········································································

    if label is None: label = name

    boolVar = ET.Element("IntVectorProperty", 
    {
    "name":               name,
    "command":            "SetParameter",
    "label":              label,
    "number_of_elements": "1",
    "default_values":     str(default),
    "initial_string":     name,
    "panel_visibility":   visibility
    })

    boolRange = ET.Element("BooleanDomain",
    {
        "name":     name,
    })

    doc = ET.Element("Documentation",{})
    doc.text = documentation

    boolVar.append(boolRange)
    if documentation != '': boolVar.append(doc)
    BOOL.append(boolVar)

def AddIntSlider(name, default, limits, label=None, documentation = '', visibility = "default"):
    #"label":           - the text that will appear next to the blank (string)
    #"name":            - the name of the variable defined in the imported 
    #                   function, linked with that field.    
    #"default":         - the default value (string)
    #"limits":          - the limits of the working range of the slider
    #"documentation":   - some help that will be displayed when the cursor is on
    #                   the blank (string)
    #"visibility":      - Set to "advanced" if you want this field to appear 
    #                   only when the 'gear' is pressed
    #···········································································

    if label is None: label = name

    slider = ET.Element("IntVectorProperty", 
    {
    "name":               name,
    "command":            "SetParameter",
    "label":              label,
    "number_of_elements": "1",
    "default_values":     str(default),
    "initial_string":     name,
    "panel_visibility":   visibility
    })

    sliderRange = ET.Element("IntRangeDomain",
    {
        "name":     name,
        "min":      str(limits[0]),
        "max":      str(limits[1])
    })

    doc = ET.Element("Documentation",{})
    doc.text = documentation

    slider.append(sliderRange)
    if documentation != '': slider.append(doc)
    INT_SLIDERS.append(slider)

def AddIntEnum(name, choices, default, label=None, documentation = '', visibility = "default"):
    #"label":           - the text that will appear next to the blank (string)
    #"name":            - the name of the variable defined in the imported 
    #                   function, linked with that field.
    #"choices"          - is a list of strings containing all the possible options
    #"default":         - the default value (string)
    #"documentation":   - some help that will be displayed when the cursor is on
    #                   the blank (string)
    #"visibility":      - Set to "advanced" if you want this field to appear 
    #                   only when the 'gear' is pressed
    #The output of this field is the index of the selected element, an integer.
    #···········································································

    if label is None: label = name

    default_index = choices.index(default)

    int_enum = ET.Element("IntVectorProperty", 
    {
    "name":               name,
    "command":            "SetParameter",
    "label":              label,
    "number_of_elements": "1",
    "default_values":     str(default_index),
    "initial_string":     name,
    "panel_visibility":   visibility
    })

    enum_domain = ET.Element("EnumerationDomain", 
    {
    "name":     "enum",
    })

    doc = ET.Element("Documentation",{})
    doc.text = documentation

    for i in range(len(choices)):
        entry = ET.Element("Entry", 
        {
        "text":     choices[i],
        "value":    str(i),                    
        })    
        enum_domain.append(entry)
    
    if documentation != '': int_enum.append(doc)
    int_enum.append(enum_domain)
    INT_ENUM.append(int_enum)

def AddScript(function1, function2 = void, visibility="advanced"):
    #it adds the source code of function1 and function2 to the plugin function1
    #and function2 are the names of the functions if both functions are
    #defined, they will be concatenated. remember to import the functions on
    #the top of this script
    #
    # Set visibility as "never" if you want your script to be hidden in every
    # case.
    #···········································································

    request_script = ET.Element("StringVectorProperty", 
    {
        "name":               "Script",
        "command":            "SetScript",
        "number_of_elements": "1",
        "default_values":     _function_source(function1) + \
                              _function_source(function2),
        "panel_visibility":   visibility,
    })
    hints = ET.Element("Hints")
    widget = ET.Element("Widget", 
    {
        "syntax":             "python",
        "type":               "multi_line",                    
    }) 
    hints.append(widget)   
    request_script.append(hints)

    global SCRIPT
    SCRIPT = request_script

def AddScriptRequestInformation(function1, function2 = void):
    #if both functions are defined, they will be concatenated.
    #Add the "RequestInformation" script to ProgrammableSource or 
    #                                                        ProgrammableFilter
    #···········································································


    request_script = ET.Element("StringVectorProperty", 
    {
        "name":               "Script",
        "command":            "SetScript",
        "number_of_elements": "1",
        "default_values":     _function_source(function1) + \
                              _function_source(function2),
        "panel_visibility":   "advanced",
    })
    hints = ET.Element("Hints")
    widget = ET.Element("Widget", 
    {
        "syntax":             "python",
        "type":               "multi_line",                    
    }) 
    hints.append(widget)   
    request_script.append(hints)
    global SCRIPT_RI
    SCRIPT_RI = request_script

def AddCategory(name):
    #If used, your plugin or source will appear in a special category instead of
    #with the other plugins.
    #···········································································

    hints = ET.Element("Hints",{})
    show_in_menu = ET.Element("ShowInMenu",
    {
        "category":         name
    })

    global CATEGORY
    hints.append(show_in_menu)
    CATEGORY = hints



#-------------------------------------------------------------------------------
#Ad here the fields that you want in your plugin. For help about the inputs, 
#look at the comments under the declarations of the functions

AddString("Name", "YourName", documentation="enter here your name")
AddString("Surname", "YourSurname", documentation="enter here your surname")
AddIntEnum("Color_index", ["blue", "green", "yellow", "black"], "green", \
                            label="Color", documentation="chose your color")
AddInt("Int1", "3", documentation="just type an integer")
AddIntSlider("Int2", 1, [0, 14])
AddBool("Bool", 0, visibility="advanced")
AddScript(print_something)
AddRefreshButton("Refresh")
AddCategory("Printing Tools")
#-------------------------------------------------------------------------------





#build the tree--------------------
root.append(proxy_group)
proxy_group.append(source_proxy)
source_proxy.append(input_property)


if SCRIPT != None: 
    source_proxy.append(SCRIPT)

if REFRESH != None: 
    source_proxy.append(REFRESH)

if SCRIPT_RI != None: 
    source_proxy.append(SCRIPT_RI)

if CATEGORY != None: 
    source_proxy.append(CATEGORY)

for elem in STRING:
    source_proxy.append(elem)

for elem in INT:
    source_proxy.append(elem)

for elem in INT_ENUM:
    source_proxy.append(elem)

for elem in STR_ENUM:
    source_proxy.append(elem)

for elem in INT_SLIDERS:
    source_proxy.append(elem)

for elem in BOOL:
    source_proxy.append(elem)
#..................................



#write everything 
ET.ElementTree(root).write(outputName, encoding="UTF-8", xml_declaration=True, \
                pretty_print=True)
