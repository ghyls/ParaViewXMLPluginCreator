The XML Plugin Generator
------------------------

This tool will generate a XML plugin for ParaView from a Python script. Once
the script is written and the interface is described, writing the XML will take
less than half a second. There is no need to compile, and it is very easy to
make changes and update the plugin with them.

Every plugin from the TimeTools set of plugins has been made by this method,
but for now, we will just write a simple script using all the functionalities
of the XML generator.

Writing the python script: the engine of the plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We will start by writing a python script that will take the value from the
variables set by the user on the interface and perform some simple operations.

The whole script must be therefore included inside a function, whose arguments
are the variables that we will take from the plugin interface in ParaView.

It is also recommended to include the code inside a ``try`` statement, in order 
to avoid that ParaView crashes if a error occurs.

When we are still writing and debugging the script, it's no worth to generate
the XML and load it into ParaView each time that we want to test it. The best
way to do this is by writing on the script some "test" values for the variables
that will appear on the interface, and pasting the script into a "Programmable
Source" (or filter), which we can access by clicking :menuselection:`Sources
--> Programmable Source` or :menuselection:`Filters --> Alphabetical -->
Programmable Filter`. Let's work for now with that simple script, that prints
something related to some integer, string and boolean variables:

.. code-block:: python

    available_colors = ["blue", "green", "yellow", "black"]

    Name = 'Charles'
    Surname = 'Darwin'
    Color_index = 2
    Int1 = 3
    Int2 = 5
    Bool = False


    print("hello, " + Name + ' ' + Surname)

    result = Int1 + Int2
    print(str(Int1)+ ' + ' + str(Int2) + ' = ' + str(result)) 

    print("You have chosen the color " + available_colors[Color_index])

    if Bool: print("boolean variable is selected")
    else: print("boolean variable is unselected")


Once inside  the Programmable Source, we can paste our script on the "Script"
field and press Apply. The output will be shown on the terminal from where we
have run ParaView (if we ran it from terminal) or in the "Output Messages"
window inside ParaView (:menuselection:`View --> Output Messages`).

.. figure:: https://github.com/mariohyls/ParaViewXMLPluginCreator/blob/master/output_message.png
   :align: center
   :alt: The output is shown in "Output Messages" window.

   The output is shown in the "Output Messages" window

Now that our script works as expected, is time to wrap it inside a function:

.. code-block:: python

    def print_something(Name, Surname, Color_index, Int1, Int2, Bool):
        try:

            print("hello, " + Name + ' ' + Surname)

            result = Int1 + Int2
            print(str(Int1)+ ' + ' + str(Int2) + ' = ' + str(result)) 

            available_colors = ["blue", "green", "yellow", "black"]
            print("You have chosen the color " + available_colors[Color_index])

            if Bool: print("boolean variable is selected")
            else: print("boolean variable is unselected")

        except Exception as e: 
            print("Some errors occurred!")
            print(e)

Note that we have replaced our "test" variables for function arguments. Now,
we can move to *xmlGenerator.py* to create the interface of the plugin.

Generating the XML
~~~~~~~~~~~~~~~~~~


Once inside the script, we should edit only the content between the
``#-----------`` delimiters (unless we want to add new functions, etc). There
are only two editable portions. the first one is at the beginning of the
script, and it is used for setting the general properties of the plugin, such
as it's name or it's type ('sources' or 'filters') [2]_ . The second one is
almost at the end and is used for setting the elements that will appear on the
plugin's interface. Let's deal now with the first one:

Suppose that our function ``print_something`` is defined inside a file called
*test.py*. Therefore, we will import it like ``from test import
print_something``. We can import as many functions as we want, from the same or
from different files. 


Then, we can fill the rest of the fields as follows:

.. code-block:: python

    #------------------------------------------------------------------------------
    #import here the functions that your script is using
    from test import print_something

    #enter the name you want for your Plugin inside ParaView
    name = "Print Something" 

    #   ...and the name of the xml
    outputName = "print_something.xml"

    #   ...and the type of the plugin ("sources" or "filters")
    pluginType = "sources"
    #-------------------------------------------------------------------------------

Now, we will move to the second and last editable part of the script. We will
add there all the fields that we want to appear in our interface. 

"Name" and "Surname" are strings. We will implement them with the function
``AddString``, that will create a field where we will just type the string.

.. code-block:: python

    AddString("Name", "YourName", documentation="enter here your name")
    AddString("Surname", "YourSurname", documentation="enter here your surname")

.. note:: The meaning of the arguments of every function is described just under it's definition on the
          script.

For the "Color" variable, the user will chose one color from a drop-down list
with some choices. For this purpose, we will use the ``AddIntEnum``
function, to chose between *blue, green, yellow and black*. The order of the
elements is here important, and has to match the ordering in the script's
array.

.. code-block:: python

    AddIntEnum("Color_index", ["blue", "green", "yellow", "black"], "green", \
                                label="Color", documentation="chose your color")

This function will return the index in the list of the element ("blue",
"green", ...) that we have selected, as an integer. For avoiding any confusion,
although the variable in the script linked with this field is an integer
(*Color_index*), we are actually choosing from a list of colors (not numbers).
For that reason, we have set the label "Color" to appear next to the drop-down
list. The default label for every field is it's name ("Color_index" in this
case) 

We will also add the "Int" numbers in two different ways.
For the first one, we will use ``AddInt``, that will create a blank on
which we will just type the number. 

.. code-block:: python   

    AddInt("Int1", "3", documentation="just type an integer")

For the second one, we will use a slider, which will range from 0 to 14.
The function that does the job is ``AddIntSlider``.

.. code-block:: python  

    AddIntSlider("Int2", 1, [0, 14])


For the bool variable, we will use the function ``AddBool``. We will write no
help for it and we will move it in "advanced" properties panel. It's default
value will be *False*.

.. code-block:: python  

    AddBool("Bool", 0, visibility="advanced")


We will now add our function ``print_something`` that deals with all those
variables, by the following command:

.. code-block:: python  

    AddScript(print_something)

This function sends by default the field "Script" which contains the code to
the "advanced" panel. If we want it visible by default, we should add the
argument ``visibility="default"``. If we want it totally hidden, we should set
``visibility="never"``.

Also, we will add a button which restarts the plugin. It is quite useful, since
the *Apply* button is only available to push each time we change some
parameters in the interface. If we want to refresh the plugin without having
made any changes (which can be very useful in some cases), we could just press
the following "refresh" button:

.. code-block:: python

    AddRefreshButton("Refresh")


in Last place, we will include that plugin in a custom category, which will
allow us to find it easily in ParaView.:

.. code-block:: python  

    AddCategory("Printing Tools")

Once done, we can just run the script and a XML file will be created in the
workspace folder.

.. note:: The name of each field *must* match the name of the correspondent
          argument in our function, in order to properly link them.


.. [2] The main difference between a source and a filter, is that a filter
       works with *already existing data*, while a source *generates* new data. Our
       function doesn't take data from anywhere, so it will be a source. 

Running the plugin in ParaView
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We will now test the plugin in ParaView. Once ParaView is opened, load the
plugin by clicking :menuselection:`Tools --> Manage Plugins... --> Load New`.
Navigate then to the folder where you have generated the plugin and select it.
For ParaView 5.4.1, you will have to specify that you are looking for a *xml*
file. This is no longer necessary in further versions.

Once the plugin is loaded, run it by clicking :menuselection:`Sources -->
Printing Tools --> Print something`. The plugin will appear as a source in the
Pipeline like this:

.. figure:: https://github.com/mariohyls/ParaViewXMLPluginCreator/blob/master/loaded_plugin.png
   :align: center
   :alt: The plugin is now loaded and visible in the Pipeline

   The plugin is now loaded and visible in the Pipeline.

Now we can start playing with the plugin. To run it, press either *Apply* or
*Refresh*. Enter the values that you want in the fields and check that the
result is as expected. Remember that the bool variable is *hidden* in
"advanced" options, so we can modify it only by pressing the *gear* button.

.. figure:: https://github.com/mariohyls/ParaViewXMLPluginCreator/blob/master/testing_plugin.png
   :align: center
   :alt: We check that everything works as expected
   
   We check that everything works as expected

Note that till now we have made no mention to IMAS or VTK. This tool can
actually be used for any type of plugin for ParaView (as long as it fits into a
*Programmable Source* or *Programmable Filter*).
