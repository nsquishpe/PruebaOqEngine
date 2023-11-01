# FAQ about running hazard calculations

## performance

### Can I estimate the runtime of a classical calculation without running it?

Since engine 3.15 you can. The trick is to run a reduced calculation first, by
using the command

  $ oq engine --run job.ini --sample-sources=0.01

This will reduce the number of ruptures by ~100 times so that the
reduced calculation will complete in a reasonable amount of time. Then
in the log you will see the estimate runtime for the full calculation.
For instance for the SHARE model on a computer with
an i7 processor you will see something like this:

[2022-04-19 08:57:05 #4054 INFO] Estimated time 72.3 hours

The estimate is rather rough, so do not take it at the letter. The
runtime can be reduced by orders of magnitude by tuning parameters
like the `pointsource_distance` and `ps_grid_spacing`, discussed at
length in the [advanced manual](https://docs.openquake.org/oq-engine/advanced/general.html#pointsource-distance).

## logic trees

### How should I interpret the "Realizations" output?

This is explained in the advanced manual:

https://docs.openquake.org/oq-engine/advanced/logic_trees.html

## classical calculations

### How do I export the hazard curves/maps/uhs for each realization?

By default the engine only exports statistical results, i.e. the mean
hazard curves/maps/uhs. If you want the individual results you must set
`individual_rlzs=true` in the job.ini files. Please take care: if you have
thousands of realizations (which is quite common) the data transfer
and disk space requirements will be thousands of times larger than
just returning the mean results: the calculation might fail. This is
why by default `individual_rlzs` is false.

### Argh, I forgot to set `individual_rlzs`! Must I repeat the calculation?

No, just set `individual_rlzs=true` in the job.ini and run
```bash
$ oq engine --run job.ini --hc=<ID> --exports csv
```
where `<ID>` must be replaced with the ID of the original calculation.
The individual outputs will be regenerated by reusing the result of the
previous calculation: it will be a lot faster than repeating the calculation
from scratch.

### Argh, I set the wrong `poes` in the job.ini? Must I repeat the calculation?

No, set the right `poes` in the job.ini and as before run
```bash
$ oq engine --run job.ini --hc=<ID> --exports csv
```
where `<ID>` must be replaced with the ID of the original calculation.
Hazard maps and UHS can be regenerated from an existing calculation
quite efficiently.

## disaggregation calculations

### I am getting an error "disaggregation matrix is too large"!

This means that you have too many disaggregation bins. Please act on the
binning parameters, i.e. on `mag_bin_width`, `distance_bin_width`,
`coordinate_bin_width`, `num_epsilon_bins`. The most relevant parameter is
`coordinate_bin_width` which is quadratic: for instance by changing from
`coordinate_bin_width=0.1` to `coordinate_bin_width=1.0` the size of your
disaggregation matrix will be reduced by 100 times.

## event based calculations

### What is the relation between sources, ruptures, events and realizations?

A single rupture can produce multiple seismic events during the
investigation time. How many depends on the number of stochastic event sets,
on the rupture occurrence rate and on the `ses_seed` parameters, as
[explained here](https://docs.openquake.org/oq-engine/advanced/event_based.html#rupture-sampling-how-does-it-work).
In the engine a rupture is uniquely identified by
a rupture ID, which is a 32 bit positive integer.
Starting from engine 3.7, seismic events are uniquely identified by an
event ID, which is a 32 bit positive integer. The relation
between event ID and rupture ID is given encoded in the `events` table
in the datastore, which also contains the realization associated to the
event. The properties of the
rupture generating the events can be ascertained by looking inside the
`ruptures` table. In particular ther `srcidx` contains the index of the
source that generated the rupture. The `srcidx` can be used to extract
the properties of the sources by looking inside the `source_info` table,
which contains the `source_id` string used in the XML source model.

## general

### Can I run a calculation from a Jupyter notebook?

You can run any kind of calculation from a Jupyter notebook, but usually
calculations are long and it is not convenient to run them interactively.
Scenarios are an exception, since they are usually fast, unless you use
spatial correlation with a lot of sites. Assuming the parameters of the
calculation are in a `job.ini` file you can run the following lines in
the notebook:
```python
In[1]: from openquake.calculators.base import run_calc
In[2]: calc = run_calc('job.ini')
```
Then you can inspect the contents of the datastore and perform your
postprocessing:
```python
In[3]: calc.datastore.open('r')  # open the datastore for reading
```
The inner format of the datastore is not guaranteed to be the same
across releases and it is not documented, so this approach is
recommended to the most adventurous people.

### how do I plot/analyze/postprocess the results of a calculation?

The official way to plot the result of a calculation is to use the
[QGIS plugin](https://plugins.qgis.org/plugins/svir/). However you
may want a kind of plot which is not available in the plugin, or
you may want to batch-produce hundreds of plots, or you may want to
plot the results of a postprocessing operation. In such cases you
need to use the [extract API](extract-api) and to write your own
plotting/postprocessing code.