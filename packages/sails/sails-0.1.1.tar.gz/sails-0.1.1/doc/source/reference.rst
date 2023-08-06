Module reference
================

Model fitting and Diagnostics
#############################

Model fitting classes
*********************

.. autoclass:: sails.modelfit.VieiraMorfLinearModel
   :members:

.. autoclass:: sails.modelfit.OLSLinearModel
   :members:


Model fitting helper functions
******************************

.. autofunction:: sails.modelfit.sliding_window_fit


Model diagnostics
*****************

.. autoclass:: sails.diags.DelayDiagnostics
   :members:

.. autoclass:: sails.diags.ModelDiagnostics
   :members:

.. autofunction:: sails.modelfit.get_residuals


Model Decomposition
###################

.. autoclass:: sails.modal.MvarModalDecomposition
   :members:


Model metric estimatation
*************************

.. autoclass:: sails.mvar_metrics.FourierMvarMetrics
   :members:

.. autoclass:: sails.mvar_metrics.ModalMvarMetrics
   :members:

.. autofunction:: sails.mvar_metrics.modal_transfer_function


Plotting
########

.. autofunction:: sails.plotting.root_plot
.. autofunction:: sails.plotting.plot_vector
.. autofunction:: sails.plotting.plot_matrix

Simulation
##########

.. automodule:: sails.simulate
   :members:

Support routines
################

Abstract Classes
****************

.. autoclass:: sails.modelfit.AbstractLinearModel
   :members:

.. autoclass:: sails.mvar_metrics.AbstractMVARMetrics
   :members:

Statistical Functions
*********************

.. autofunction:: sails.mvar_metrics.sdf_spectrum
.. autofunction:: sails.mvar_metrics.psd_spectrum
.. autofunction:: sails.mvar_metrics.ar_spectrum
.. autofunction:: sails.mvar_metrics.transfer_function
.. autofunction:: sails.mvar_metrics.spectral_matrix
.. autofunction:: sails.mvar_metrics.coherency
.. autofunction:: sails.mvar_metrics.partial_coherence
.. autofunction:: sails.mvar_metrics.partial_directed_coherence
.. autofunction:: sails.mvar_metrics.isolated_effective_coherence
.. autofunction:: sails.mvar_metrics.directed_transfer_function

.. autofunction:: sails.modal.adjust_phase

.. automodule:: sails.stats
   :members:

.. automodule:: sails.modelvalidation
   :members:


Tutorial helper functions
*************************

.. automodule:: sails.tutorial_utils
   :members:


