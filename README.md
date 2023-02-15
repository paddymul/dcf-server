# Data-Cleaning-Framework

We all know how awkward it is to clean data in jupyter notebooks.  Multiple cells of exploratory work, trying different transforms, looking up different transforms, adhoc functions that work in one notebook and have to be either copied/pasta-ed to the next notebook, or rewritten from scratch.  Data Cleaning Framework  (DCF) makes all of that better by providing a visual UI for common cleaning operations AND emitting python code that performs the transformation. Specifically, the DCF is a tool built to interactively explore, clean, and transform pandas dataframes.  There are three main UI components: 


# How to use DCF

## Order of Operations
The ideal order of operations is as follows

* Column level fixes
  * drop (remove this column)
  * fillna (fill NaN/None with a value)
  * OneHotEncoding ( create multiple boolean columns from the possible values of this column )
  * MakeCategorical ( change the values of string to a Categorical Data type)
  * Quantize
* DataFrame transformations
these transforms largely keep the shape of the data the same

  * Resample
  * ManyColdDecoding (the opposite of OneHotEncoding, take multiple boolean columns and transform into a single categorical
  * Index shift (add a column with the value from previous row's column)
* Dataframe transformations 2
These result in a single new dataframe with a vastly different shape
  * Stack/Unstack columns
  * GroupBy (with UI for sellect group by function for each column)
* DataFrame transformations 2
These transforms emit multiple DataFrames
  * Relational extract (extract one or more columns into a second dataframe that can be joined back to a foreign key column)
  * Split on column (emit separate dataframes for each value of a categorical, no shape editting)
* DataFrame combination
  * concat (concatenate multiple dataframes, with UI affordances to assure a similar shape)
  * join (join two dataframes on a key, with UI affordances)

DCF can only work on a single input dataframe shape at a time.  Any newly created columns are visible on output, but not available for manipulation in the same DCF Cell.


# Components
* a rich table widget that is embeddable into applications and in the jupyter notebook.
* A UI for selecting and trying transforms interactively
* An output table widget showing the transformed dataframe


# What works now, what's coming

## Exists now
  * React frontend app
    * Displays a datatframe
	* Simple UI for column level functions
	* Shows generated python code
	* Shows transformed data frame
  * DCF server
    * Serves up dataframes for use by frontend
	* responds to dcf commands
	* shows generated python code
  * DCF Intepreter
    * Based on Peter Norvig's lispy.py, a simple syntax that is easy for the frontend to generate (no parens, just JSON arrays)
  * DCF core (actual transforms supported)
    * dropcol
	* fillna

## Next major features
  * Jupyter Notebook widget
    * embed the same UI from the frontend into a jupyter notebook shell
	* No need to fire up a separate server, commands sent via ipywidgets.comms
	* Add a "send generated python to next cell" function
  * React frontend app
    * Styling
	  * Tabs to switch between output_df, generated python, and DCF-command
	  * Better column editor, maybe embed column commands into another table widget
	  * Tabs for different types of transform commands
	  * Server only, some UI for DataFrame selection
    * Pre filtering concept (only operate on first 1000 rows, some sample of all rows)
	* DataFrame joining UI
	* Summary statistics tab for incoming dataframe
	* Multi index columns
	* DateTimeIndex support
  * DCF core
    * OneHotEncoding
	* MakeCategorical
	* Quantize
	* Resample
	* ManyColdDecoding
	* IndexShift
	* Computed
	* Stack/Unstack
	* GroupBy
	* RelationalExtract
	* Split
	* concat
	* join
