# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2010 Joachim Hoessler <hoessler@gmail.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

import urllib
import urllib2
from datetime import datetime
from time import strptime

from trac.config import Option, ListOption, BoolOption
from trac.core import TracError, Component, implements
from trac.ticket.query import Query
from trac.util.datefmt import from_utimestamp
from trac.web.api import IRequestHandler, RequestDone
from trac.wiki.api import parse_args

AVAILABLE_OPTIONS = ['startdate', 'enddate', 'today', 'width', 'height',
                     'color', 'bgcolor', 'wecolor', 'weekends', 'gridlines',
                     'expected', 'colorexpected', 'title']


def get_estimation_field():
    return Option('estimation-tools', 'estimation_field', 'estimatedhours',
                  doc="""Defines what custom field should be used to calculate
        estimation charts. Defaults to 'estimatedhours'""")


def get_closed_states():
    return ListOption('estimation-tools', 'closed_states', 'closed',
                      doc="""Set to a comma separated list of workflow states that count
        as "closed", where the effort will be treated as zero, e.g.
        closed_states=closed,another_state. Defaults to closed.""")


def get_estimation_suffix():
    return Option('estimation-tools', 'estimation_suffix', 'h',
                  doc="""Suffix used for estimations. Defaults to 'h'""")


def get_serverside_charts():
    return BoolOption('estimation-tools', 'serverside_charts', 'false',
                      doc="""Generate charts links internally and fetch charts server-side
        before returning to client, instead of generating Google links that
        the users browser fetches directly. Particularly useful for sites
        served behind SSL. Server-side charts uses POST requests internally,
        increasing chart data size from 2K to 16K. Defaults to false.""")


class EstimationToolsBase(Component):
    """ Base class EstimationTools components that auto-disables if
    estimation field is not properly configured. """

    abstract = True
    estimation_field = get_estimation_field()

    def __init__(self, *args, **kwargs):
        if not self.env.config.has_option('ticket-custom',
                                          self.estimation_field):
            # No estimation field configured. Disable plugin and log error.
            self.log.error("EstimationTools (%s): "
                           "Estimation field not configured. "
                           "Component disabled.", self.__class__.__name__)
            self.env.disable_component(self)


class GoogleChartProxy(EstimationToolsBase):
    """ A Google Chart API proxy handler that moves chart fetching server-side.
    Implemented to allow serving the charts under SSL encryption between client
    and server - without the nagging error messages."""

    implements(IRequestHandler)

    def match_request(self, req):
        return req.path_info == '/estimationtools/chart'

    def process_request(self, req):
        req.perm.require('TICKET_VIEW')
        data = req.args.get('data', '')
        opener = urllib2.build_opener(urllib2.HTTPHandler())
        chart_req = urllib2.Request('http://chart.googleapis.com/chart',
                                    data=data)
        self.log.debug("Fetch chart, %r + data: %r",
                       chart_req.get_method(), data)
        chart = opener.open(chart_req)
        for header, value in chart.headers.items():
            req.send_header(header, value)
        req.write(chart.read())
        raise RequestDone


def parse_options(env, content, options):
    """Parses the parameters, makes some sanity checks, and creates default values
    for missing parameters.
    """
    _, parsed_options = parse_args(content, strict=False)

    options.update(parsed_options)
    today = datetime.now().date()

    startdatearg = options.get('startdate')
    if startdatearg:
        options['startdate'] = \
            datetime(*strptime(startdatearg, "%Y-%m-%d")[0:5]).date()

    enddatearg = options.get('enddate')
    options['enddate'] = None
    if enddatearg:
        options['enddate'] = \
            datetime(*strptime(enddatearg, "%Y-%m-%d")[0:5]).date()

    if not options['enddate'] and options.get('milestone'):
        # use first milestone
        milestone = options['milestone'].split('|')[0]
        # try to get end date from db
        for completed, due in env.db_query("""
                SELECT completed, due FROM milestone WHERE name = %s
                """, (milestone,)):
            if completed:
                options['enddate'] = from_utimestamp(completed).date()
            elif due:
                due = from_utimestamp(due).date()
                if due >= today:
                    options['enddate'] = due
            break
        else:
            raise TracError("Couldn't find milestone %s" % milestone)

    options['enddate'] = options['enddate'] or today
    options['today'] = options.get('today') or today

    if options.get('weekends'):
        options['weekends'] = parse_bool(options['weekends'])

    # all arguments that are no key should be treated as part of the query
    query_args = {}
    for key in options.keys():
        if key not in AVAILABLE_OPTIONS:
            query_args[key] = options[key]
    return options, query_args


def execute_query(env, req, query_args):
    # set maximum number of returned tickets to 0 to get all tickets at once

    def quote(v):
        return unicode(v).replace('%', '%25').replace('&', '%26') \
                         .replace('=', '%3D')

    query_args['max'] = 0
    query_string = '&'.join('%s=%s' % (quote(item[0]), quote(item[1]))
                            for item in query_args.iteritems())
    env.log.debug("query_string: %s", query_string)
    query = Query.from_string(env, query_string)

    tickets = query.execute(req)

    tickets = [t for t in tickets
               if ('TICKET_VIEW' or 'TICKET_VIEW_CC')
               in req.perm('ticket', t['id'])]

    return tickets


def parse_bool(s):
    if s is True or s is False:
        return s
    s = str(s).strip().lower()
    return s not in ['false', 'f', 'n', '0', '']


def urldecode(query):
    # Adapted from example on Python mailing lists
    d = {}
    a = query.split('&')
    for s in a:
        if s.find('='):
            k, v = map(urllib.unquote, s.split('='))
            try:
                d[k].append(v)
            except KeyError:
                d[k] = [v]
    return d
