# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (C) 2010-2016 GEM Foundation
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake. If not, see <http://www.gnu.org/licenses/>.

# Disable:
# - 'Maximum number of public methods for a class'
# - 'Missing docstring' (because of all of the model Meta)
# pylint: disable=R0904,C0111

'''
Model representations of the OpenQuake DB tables.
'''
import os
import collections
from datetime import datetime

from openquake.commonlib import datastore
from openquake.commonlib.oqvalidation import OqParam, RISK_CALCULATORS
import django
if hasattr(django, 'setup'):
    django.setup()  # for Django >= 1.7
from django.db import models as djm
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections

#: Kind of supported curve statistics
STAT_CHOICES = (
    (u'mean', u'Mean'),
    (u'quantile', u'Quantile'))


#: System Reference ID used for geometry objects
DEFAULT_SRID = 4326


VS30_TYPE_CHOICES = (
    (u"measured", u"Value obtained from on-site measurements"),
    (u"inferred", u"Estimated value"),
)

IMT_CHOICES = (
    (u'PGA', u'Peak Ground Acceleration'),
    (u'PGV', u'Peak Ground Velocity'),
    (u'PGD', u'Peak Ground Displacement'),
    (u'SA', u'Spectral Acceleration'),
    (u'IA', u'Arias Intensity'),
    (u'RSD', u'Relative Significant Duration'),
    (u'MMI', u'Modified Mercalli Intensity'),
)

#: Minimum value for a seed number
MIN_SINT_32 = -(2 ** 31)
#: Maximum value for a seed number
MAX_SINT_32 = (2 ** 31) - 1


#: Kind of supported type of loss outputs
LOSS_TYPES = ["structural", "nonstructural", "fatalities", "contents"]

#: relative tolerance to consider two risk outputs (almost) equal
RISK_RTOL = 0.05


#: absolute tolerance to consider two risk outputs (almost) equal
RISK_ATOL = 0.01

# TODO: these want to be dictionaries
INPUT_TYPE_CHOICES = (
    (u'unknown', u'Unknown'),
    (u'source', u'Source Model'),
    (u'source_model_logic_tree', u'Source Model Logic Tree'),
    (u'gsim_logic_tree', u'Ground Shaking Intensity Model Logic Tree'),
    (u'exposure', u'Exposure'),
    (u'fragility', u'Fragility'),
    (u'site_model', u'Site Model'),
    (u'rupture_model', u'Rupture Model'),

    # vulnerability models
    (u'structural_vulnerability', u'Structural Vulnerability'),
    (u'nonstructural_vulnerability', u'Non Structural Vulnerability'),
    (u'contents_vulnerability', u'Contents Vulnerability'),
    (u'business_interruption_vulnerability',
     u'Business Interruption Vulnerability'),
    (u'occupants_vulnerability', u'Occupants Vulnerability'),
    (u'structural_vulnerability_retrofitted',
     u'Structural Vulnerability Retrofitted'))


def getcursor(route):
    """Return a cursor from a Django route"""
    return connections[route].cursor()


# Tables in the 'uiapi' schema.

class OqJob(djm.Model):
    '''
    An OpenQuake engine run started by the user
    '''
    description = djm.TextField()
    user_name = djm.TextField()
    calculation_mode = djm.TextField()
    hazard_calculation = djm.ForeignKey('OqJob', null=True)
    STATUS_CHOICES = (
        (u'created', u'Created'),
        (u'pre_executing', u'Pre-Executing'),
        (u'executing', u'Executing'),
        (u'post_executing', u'Post-Executing'),
        (u'post_processing', u'Post-Processing'),
        (u'export', u'Exporting results'),
        (u'clean_up', u'Cleaning up'),
        (u'complete', u'Complete'),
    )
    status = djm.TextField(choices=STATUS_CHOICES, default='pre_executing')
    is_running = djm.BooleanField(default=True)
    start_time = djm.DateTimeField(editable=False, default=datetime.utcnow)
    stop_time = djm.DateTimeField(editable=False)
    relevant = djm.BooleanField(null=False, default=True)
    ds_calc_dir = djm.TextField(null=False, blank=True)  # datastore calc_dir

    class Meta:
        db_table = 'job'

    @property
    def job_type(self):
        """
        'hazard' or 'risk'
        """
        # the calculation mode can be unknown if the job parameters
        # have not been written on the database yet
        return 'risk' if self.calculation_mode in RISK_CALCULATORS else 'hazard'

    def has_hdf5(self):
        """
        Check if the associated .hdf5 file exists
        """
        return os.path.exists(self.ds_calc_dir + '.hdf5')

    def get_or_create_output(self, display_name, output_type, ds_key):
        """
        :param disp_name: display name of the output
        :param output_type: the output type
        :returns: an Output instance
        """
        try:
            output = Output.objects.get(
                oq_job=self, display_name=display_name,
                output_type=output_type)
        except ObjectDoesNotExist:
            output = Output.objects.create_output(
                self, display_name, output_type, ds_key)
        return output

    def get_oqparam(self):
        """
        Return an OqParam object as read from the database
        """
        datadir = os.path.dirname(self.ds_calc_dir)
        dstore = datastore.read(self.id, datadir=datadir)
        oqparam = OqParam.from_(dstore.attrs)
        return oqparam

    def __repr__(self):
        return '<%s %d, %s>' % (self.__class__.__name__,
                                self.id, self.job_type)


def oqparam(job_id):
    """
    :param job_id: ID of :class:`openquake.server.db.models.OqJob`
    :returns: instance of :class:`openquake.commonlib.oqvalidation.OqParam`
    """
    return OqJob.objects.get(pk=job_id).get_oqparam()


class Performance(djm.Model):
    '''
    Contains performance information about a job.
    '''
    job = djm.ForeignKey('OqJob')
    operation = djm.TextField(null=False)
    time_sec = djm.FloatField(null=False)
    memory_mb = djm.FloatField(null=False)
    counts = djm.IntegerField(null=False)

    class Meta:
        db_table = 'performance'


class Log(djm.Model):
    '''
    Log table for calculations
    '''
    job = djm.ForeignKey('OqJob', null=True)
    timestamp = djm.DateTimeField(editable=False, default=datetime.utcnow)
    LOG_LEVEL_CHOICES = (
        (u'debug', u'Debug'),
        (u'info', u'Info'),
        (u'progress', u'Progress'),
        (u'warn', u'Warn'),
        (u'error', u'Error'),
        (u'critical', u'Critical'),
    )
    level = djm.TextField(choices=LOG_LEVEL_CHOICES)
    process = djm.TextField(null=False)
    message = djm.TextField(null=False)

    class Meta:
        db_table = 'log'


def extract_from(objlist, attr):
    """
    Extract an attribute from a list of Django objects, by scanning
    them in order until a not None attribute is found. If nothing is
    found, or if an exception ObjectDoesNotExist is raised, return None.

    :param objlist: the list of Django objects
    :param str attr: the name of the attribute to look for
    """
    for obj in objlist:
        try:
            value = getattr(obj, attr, None)
        except ObjectDoesNotExist:
            value = None
        if value is not None:
            return value


class OutputManager(djm.Manager):
    """
    Manager class to filter and create Output objects
    """
    def create_output(self, job, display_name, output_type, ds_key):
        """
        Create an output for the given `job`, `display_name` and
        `output_type` (default to hazard_curve)
        """
        return self.create(oq_job=job,
                           display_name=display_name,
                           output_type=output_type,
                           ds_key=ds_key)


class Output(djm.Model):
    '''
    A single artifact which is a result of an OpenQuake job.
    The data may reside in a file or in the database.
    '''

    #: Metadata of hazard outputs used by risk calculation. See
    #: `hazard_metadata` property for more details
    HazardMetadata = collections.namedtuple(
        'hazard_metadata',
        'investigation_time statistics quantile sm_path gsim_path')

    #: Hold the full paths in the model trees of ground shaking
    #: intensity models and of source models, respectively.
    LogicTreePath = collections.namedtuple(
        'logic_tree_path',
        'gsim_path sm_path')

    #: Hold the statistical params (statistics, quantile).
    StatisticalParams = collections.namedtuple(
        'statistical_params',
        'statistics quantile')

    oq_job = djm.ForeignKey('OqJob', null=False)

    display_name = djm.TextField()

    HAZARD_OUTPUT_TYPE_CHOICES = (
        (u'disagg_matrix', u'Disaggregation Matrix'),
        (u'gmf', u'Ground Motion Field'),
        (u'gmf_scenario', u'Ground Motion Field'),
        (u'hazard_curve', u'Hazard Curve'),
        (u'hazard_curve_multi', u'Hazard Curve (multiple imts)'),
        (u'hazard_map', u'Hazard Map'),
        (u'ses', u'Stochastic Event Set'),
        (u'uh_spectra', u'Uniform Hazard Spectra'),
    )

    RISK_OUTPUT_TYPE_CHOICES = (
        (u'agg_loss_curve', u'Aggregate Loss Curve'),
        (u'aggregate_loss', u'Aggregate Losses'),
        (u'bcr_distribution', u'Benefit-cost ratio distribution'),
        (u'collapse_map', u'Collapse Map Distribution'),
        (u'dmg_dist_per_asset', u'Damage Distribution Per Asset'),
        (u'dmg_dist_per_taxonomy', u'Damage Distribution Per Taxonomy'),
        (u'dmg_dist_total', u'Total Damage Distribution'),
        (u'event_loss', u'Event Loss Table'),
        (u'event_loss_asset', u'Event Loss Asset'),
        (u'loss_curve', u'Loss Curve'),
        (u'event_loss_curve', u'Loss Curve'),
        (u'loss_fraction', u'Loss fractions'),
        (u'loss_map', u'Loss Map'),
        (u'dmg_per_asset', 'Damage Per Asset'),
    )

    output_type = djm.TextField(
        choices=HAZARD_OUTPUT_TYPE_CHOICES + RISK_OUTPUT_TYPE_CHOICES)
    last_update = djm.DateTimeField(editable=False, default=datetime.utcnow)
    ds_key = djm.TextField(null=False, blank=True)  # datastore key

    objects = OutputManager()

    def __str__(self):
        return "%d||%s||%s" % (self.id, self.output_type, self.display_name)

    class Meta:
        db_table = 'output'
        ordering = ['id']

    def is_hazard_curve(self):
        return self.output_type in ['hazard_curve', 'hazard_curve_multi']

    @property
    def output_container(self):
        """
        :returns: the output container associated with this output
        """

        # FIXME(lp). Remove the following outstanding exceptions
        if self.output_type in ['agg_loss_curve', 'event_loss_curve']:
            return self.loss_curve
        elif self.output_type == 'hazard_curve_multi':
            return self.hazard_curve
        elif self.output_type == 'gmf_scenario':
            return self.gmf
        elif self.output_type == 'event_loss_asset':
            return self.event_loss
        return getattr(self, self.output_type)

    @property
    def lt_realization_paths(self):
        """
        :returns: an instance of `LogicTreePath` the output is
        associated with. When the output is not associated with any
        logic tree branch then it returns a LogicTreePath namedtuple
        with a couple of None.
        """
        hazard_output_types = [el[0] for el in self.HAZARD_OUTPUT_TYPE_CHOICES]
        risk_output_types = [el[0] for el in self.RISK_OUTPUT_TYPE_CHOICES]
        container = self.output_container

        if self.output_type in hazard_output_types:
            rlz = getattr(container, 'lt_realization_id', None)
            if rlz is not None:
                return self.LogicTreePath(
                    tuple(container.lt_realization.gsim_lt_path),
                    tuple(container.lt_realization.sm_lt_path))
            else:
                return self.LogicTreePath(None, None)
        elif self.output_type in risk_output_types:
            if getattr(container, 'hazard_output_id', None):
                return container.hazard_output.lt_realization_paths
            else:
                return self.LogicTreePath(None, None)

        raise RuntimeError("unexpected output type %s" % self.output_type)

    @property
    def statistical_params(self):
        """
        :returns: an instance of `StatisticalParams` the output is
        associated with
        """
        if getattr(self.output_container, 'statistics', None) is not None:
            return self.StatisticalParams(self.output_container.statistics,
                                          self.output_container.quantile)
        elif getattr(
                self.output_container, 'hazard_output_id', None) is not None:
            return self.output_container.hazard_output.statistical_params
        else:
            return self.StatisticalParams(None, None)

    @property
    def hazard_metadata(self):
        """
        Given an Output produced by a risk calculation it returns the
        corresponding hazard metadata.

        :returns:
            A `namedtuple` with the following attributes::

                * investigation_time: the hazard investigation time (float)
                * statistics: the kind of hazard statistics (None, "mean" or
                  "quantile")
                * quantile: quantile value (when `statistics` is "quantile")
                * sm_path: a list representing the source model path
                * gsim_path: a list representing the gsim logic tree path

        """
        oq = self.oq_job.get_oqparam()

        statistics, quantile = self.statistical_params
        gsim_lt_path, sm_lt_path = self.lt_realization_paths

        return self.HazardMetadata(oq.investigation_time,
                                   statistics, quantile,
                                   sm_lt_path, gsim_lt_path)
