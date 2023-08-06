"""A class for manipulating time series based on measurements at
unevenly-spaced times, see:

http://en.wikipedia.org/wiki/Unevenly_spaced_time_series

"""
# standard library
import datetime
import pprint
from itertools import tee
import csv
try:
    import itertools.izip as zip
except ImportError:
    pass
from copy import deepcopy
from queue import PriorityQueue
from future.utils import listitems, iteritems

# 3rd party
import sortedcontainers
from dateutil.parser import parse as date_parse
from infinity import inf

# local
from . import histogram
from . import utils
from .domain import Domain


class TimeSeries(object):
    """A class to help manipulate and analyze time series that are the
    result of taking measurements at irregular points in time. For
    example, here would be a simple time series that starts at 8am and
    goes to 9:59am:

    >>> ts = TimeSeries()
    >>> ts['8:00am'] = 0
    >>> ts['8:47am'] = 1
    >>> ts['8:51am'] = 0
    >>> ts['9:15am'] = 1
    >>> ts['9:59am'] = 0

    The value of the time series is the last recorded measurement: for
    example, at 8:05am the value is 0 and at 8:48am the value is 1. So:

    >>> ts['8:05am']
    0

    >>> ts['8:48am']
    1

    There are also a bunch of things for operating on another time
    series: sums, difference, logical operators and such.

    """

    def __init__(self, data=None, domain=None, default_value=None):

        if domain is None:
            self.domain = Domain(domain)
            self._d = sortedcontainers.SortedDict(data)
        else:
            self.domain = None
            self.set_domain(domain)

            if self.is_data_in_domain(data):
                self._d = sortedcontainers.SortedDict(data)
            else:
                raise KeyError("Data given are not in domain.")

        self.default_value = default_value

    def set_domain(self, domain):
        """Set the domain for this TimeSeries.

        Args:
            domain (:ref:`Domain <domain>`): the new domain.

        """
        
        if domain is None:
            dom = Domain(-inf, inf)

        else:
            if isinstance(domain, Domain):
                dom = domain
            else:
                dom = Domain(domain)

            if hasattr(self, '_d'):
                if not self.is_data_in_domain(self._d, domain=dom):
                    raise ValueError("Data are not in the domain.")

        self.domain = dom

    def get_domain(self):
        """Return the domain"""
        return self.domain

    def is_data_in_domain(self, data, domain=None):
        """Check if data (sorteddict/dict) is inside the domain"""
        if domain is None:
            domain = self.domain
            
        temp = sortedcontainers.SortedDict(data)
        for key in temp.keys():
            if key not in domain:
                return False

        return True

    def __iter__(self):
        """Iterate over sorted (time, value) pairs."""
        return iteritems(self._d)

    def default(self):
        """Return the default value of the time series."""
        if self.default_value is None and self.n_measurements() == 0:
            msg = "can't get value without a default value or measurements"
            raise KeyError(msg)
        else:
            if self.default_value is None:
                return self.first()[1]
            else:
                return self.default_value

    def get(self, time):
        """Get the value of the time series, even in-between measured values.

        """
        if time not in self.domain:
            msg = "{} is outside of the domain.".format(time)
            raise KeyError(msg)

        index = self._d.bisect_right(time)
        if index > 0:
            previous_measurement_time = self._d.iloc[index - 1]
            return self._d[previous_measurement_time]
        elif index == 0:
            return self.default()
        else:
            msg = (
                'self._d.bisect_right({}) returned a negative value. '
                """This "can't" happen: please file an issue at """
                'https://github.com/datascopeanalytics/traces/issues'
            ).format(time)
            raise ValueError(msg)

    def get_by_index(self, index):
        """Get the (t, value) pair of the time series by index."""
        return self._d.peekitem(index)

    def last(self):
        """Returns the last (time, value) pair of the time series."""
        return self.get_by_index(-1)

    def first(self):
        """Returns the first (time, value) pair of the time series."""
        return self.get_by_index(0)

    def set(self, time, value, compact=False):
        """Set the value for the time series. If compact is True, only set the
        value if it's different from what it would be anyway.

        """
        # if time not in self.domain:
        #     raise KeyError("{} is outside of the domain.".format(time))

        if (len(self) == 0) or (not compact) or \
                (compact and self.get(time) != value):
            self._d[time] = value

    def update(self, data, compact=False):
        """Set the values of TimeSeries using a list.
        Compact it if necessary."""

        if not self.is_data_in_domain(data):
            raise KeyError("Data are not in the domain.")

        self._d.update(data)
        if compact:
            self.compact()

    def compact(self):
        """Convert this instance to a compact version: the value will be the
        same at all times, but repeated measurements are discarded.

        """
        previous_value = None
        remove_item = []
        for time, value in self._d.items():
            if value == previous_value:
                remove_item.append(time)
            previous_value = value
        for item in remove_item:
            del self[item]

    def items(self):
        """ts.items() -> list of the (key, value) pairs in ts, as 2-tuples"""
        return listitems(self._d)

    def remove(self, time):
        """Allow removal of measurements from the time series. This throws an
        error if the given time is not actually a measurement point.

        """
        try:
            del self._d[time]
        except KeyError:
            raise KeyError('no measurement at %s' % time)

    def n_measurements(self):
        """Return the number of measurements in the time series."""
        return len(self._d)

    def __len__(self):
        """Should this return the length of time in seconds that the time
        series spans, or the number of measurements in the time
        series? For now, it's the number of measurements.

        """
        return self.n_measurements()

    def __repr__(self):
        return '<TimeSeries>\n%s\n</TimeSeries>' % \
            pprint.pformat(self._d)

    def iterintervals(self, n=2):
        """Iterate over groups of `n` consecutive measurement points in the
        time series, optionally only the groups where the starting
        value of the time series matches `value`.

        """
        # tee the original iterator into n identical iterators
        streams = tee(iter(self), n)

        # advance the "cursor" on each iterator by an increasing
        # offset
        for stream_index, stream in enumerate(streams):
            for i in range(stream_index):
                next(stream)

        # now, zip the offset streams back together to yield tuples
        for intervals in zip(*streams):
            yield intervals

    def iterperiods(self, start_time=None, end_time=None, value=None):
        """This iterates over the periods (optionally, within a given time
        span) and yields (interval start, interval end, value) tuples.

        Will only yield time intervals that are not length 0 that are
        within the domain.

        """
        if start_time is None:
            start_time = self.domain.start()

        if end_time is None:
            end_time = self.domain.end()

        # if value is None, don't filter
        if value is None:
            def value_function(t0_, t1_, value_):
                return True

        # if value is a function, use the function to filter
        elif callable(value):
            value_function = value

        # if value is a constant other than None, then filter to
        # return only the intervals where the value equals the
        # constant
        else:
            def value_function(t0_, t1_, value_):
                return value_ == value

        # get start index and value
        start_index = self._d.bisect_right(start_time)
        if start_index:
            start_value = self._d[self._d.iloc[start_index - 1]]
        else:
            start_value = self.default()

        # get last measurement before end of time span
        end_index = self._d.bisect_right(end_time)

        # look over each interval of time series within the
        # region. Use the region start time and value to begin
        ts_interval_closes = set(self._d.islice(start_index, end_index))
        domain_interval_opens = set(
            b for (b, e) in self.domain.intervals() if b > start_time)
        iter_time = sorted(
            list(ts_interval_closes.union(domain_interval_opens)))

        int_t0, int_value = start_time, start_value

        for int_t1 in iter_time:

            try:
                domain_t0, domain_t1 = self.domain.get_interval(int_t0)
            except KeyError:
                pass
            else:
                if domain_t1 < int_t1:
                    clipped_t1 = domain_t1
                else:
                    clipped_t1 = int_t1

                # yield the time, duration, and value of the period
                nonzero = (clipped_t1 != int_t0)
                if nonzero and value_function(int_t0, clipped_t1, int_value):
                    yield int_t0, clipped_t1, int_value

            # set start point to the end of this interval for next
            # iteration
            int_t0 = int_t1
            int_value = self[int_t0]

        # yield the time, duration, and value of the final period
        if int_t0 < end_time:

            try:
                domain_t0, domain_t1 = self.domain.get_interval(int_t0)
            except KeyError:
                pass
            else:
                if domain_t1 < end_time:
                    end_time = domain_t1

                nonzero = (end_time != int_t0)
                if nonzero and value_function(int_t0, end_time, int_value):
                    yield int_t0, end_time, int_value

    def slice(self, start_time, end_time, slice_domain=True):
        """Return a slice of the time series that has a first reading at
        `start_time` and a last reading at `end_time`.

        """

        if end_time <= start_time:
            message = (
                "Can't slice a Timeseries when end_time <= start_time. "
                "Received start_time={} and end_time={}."
            ).format(start_time, end_time)
            raise ValueError(message)

        if start_time > self.domain.end() or end_time < self.domain.start():
            message = (
                "Can't slice a Timeseries when end_time and "
                "start_time are outside of the domain. "
                "Received start_time={} and end_time={}. "
                "Domain is {}."
            ).format(start_time, end_time, self.get_domain())
            raise ValueError(message)

        result = TimeSeries()
        if start_time in self.domain:
            result[start_time] = self[start_time]
        for time, value in self.items():
            if (time > start_time) and (time <= end_time):
                result[time] = value

            if time > end_time:
                break

        if slice_domain:
            new_domain = self.domain.slice(start_time, end_time)
            result.set_domain(new_domain)
        else:
            result.set_domain(self.domain)

        return result

    def regularize(self, sampling_period, start_time=None, end_time=None):
        """Sampling at regular time periods

        Output: Dict that can be converted into pandas.Series
        directly by calling pandas.Series(Dict)

        :param arg1: description
        :param arg2: description
        :type arg1: type description
        :type arg1: type description
        :return: return description
        :rtype: the return type description

        """
        if self.domain.n_intervals() > 1:
            raise NotImplementedError(
                'Cannot calculate moving average '
                'when Domain is not connected.')

        if start_time is None:
            start_time = self.domain.start()
            if start_time == -inf:
                msg = 'Start time of the domain is negative infinity.' \
                      ' Cannot regularize without specifying a start time.'
                raise ValueError(msg)

        if end_time is None:
            end_time = self.domain.end()
            if start_time == inf:
                msg = 'End time of the domain is infinity.' \
                      ' Cannot regularize without specifying an end time.'
                raise ValueError(msg)

        if start_time == -inf or end_time == inf:
            raise ValueError('Start/end time cannot be infinity.')

        if start_time > end_time:
            msg = (
                "Can't regularize a Timeseries when end_time <= start_time. "
                "Received start_time={} and end_time={}."
            ).format(start_time, end_time)
            raise ValueError(msg)

        if start_time < self.domain.start() or end_time > self.domain.end():
            message = (
                "Can't regularize a Timeseries when end_time or "
                "start_time is outside of the domain. "
                "Received start_time={} and end_time={}. "
                "Domain is {}."
            ).format(start_time, end_time, self.get_domain())
            raise ValueError(message)

        if sampling_period <= 0:
            msg = "Can't regularize a Timeseries when sampling_period <= 0."
            raise ValueError(msg)

        if sampling_period > utils.duration_to_number(end_time - start_time):
            msg = "Can't regularize a Timeseries when sampling_period " \
                  "is greater than the duration between " \
                  "start_time and end_time."
            raise ValueError(msg)

        if isinstance(start_time, datetime.datetime):
            if not isinstance(sampling_period, int):
                msg = "Can't regularize a Timeseries when " \
                      "the class of the time is datetime and " \
                      "sampling_period is not an integer."
                raise TypeError(msg)
            period_time = datetime.timedelta(seconds=sampling_period)
        else:
            period_time = sampling_period

        # if start_time is None:
        #     start_time = self.get_by_index(0)[0]
        # if end_time is None:
        #     end_time = self.last()[0]

        result = {}
        current_time = start_time
        while current_time <= end_time:
            result[current_time] = self[current_time]
            current_time += period_time
        return result

    def moving_average(self, window_size, sampling_period,
                       start_time=None, end_time=None):
        """Averaging over regular intervals

        Output: Dict that can be converted into pandas.Series
        directly by calling pandas.Series(Dict)

        """
        if start_time is None:
            start_time = self.domain.start()
            if start_time == -inf:
                raise ValueError('Start time of the domain '
                                 'is negative infinity.'
                                 ' Cannot calculate moving average '
                                 'without specifying a start time.')

        if end_time is None:
            end_time = self.domain.end()
            if start_time == inf:
                raise ValueError('End time of the domain '
                                 'is infinity.'
                                 ' Cannot calculate moving average '
                                 'without specifying an end time.')

        if start_time == -inf or end_time == inf:
            raise ValueError('Start/end time cannot be infinity.')

        if start_time > end_time:
            msg = (
                "Can't calculate moving average of a Timeseries "
                "when end_time <= start_time. "
                "Received start_time={} and end_time={}."
            ).format(start_time, end_time)
            raise ValueError(msg)

        if start_time < self.domain.start() or end_time > self.domain.end():
            message = (
                "Can't calculate moving average of "
                "a Timeseries when end_time or "
                "start_time is outside of the domain. "
                "Received start_time={} and end_time={}. "
                "Domain is {}."
            ).format(start_time, end_time, self.get_domain())
            raise ValueError(message)

        if self.domain.n_intervals() > 1:
            raise NotImplementedError(
                'Cannot calculate moving average '
                'when Domain is not connected.')

        if (window_size <= 0) or (sampling_period <= 0):
            msg = "Can't calculate moving average of a Timeseries " \
                  "when window_size <= 0 or sampling_period <= 0."
            raise ValueError(msg)

        if sampling_period > utils.duration_to_number(end_time - start_time):
            msg = "Can't calculate moving average of a Timeseries " \
                  "when sampling_period is greater than " \
                  "the duration between start_time and end_time."
            raise ValueError(msg)

        half = float(window_size) / 2

        if isinstance(start_time, datetime.datetime):
            if not isinstance(sampling_period, int):
                msg = "Can't calculate moving average of a Timeseries " \
                      "when the class of the time is datetime and " \
                      "sampling_period is not an integer."
                raise TypeError(msg)

            buffer_time = datetime.timedelta(seconds=half)
            period_time = datetime.timedelta(seconds=sampling_period)
        else:
            buffer_time = half
            period_time = sampling_period

        temp = deepcopy(self)
        temp.domain = Domain(self.domain.start() - buffer_time,
                             self.domain.end() + buffer_time)

        result = {}
        current_time = start_time
        while current_time <= end_time:
            window_start = current_time - buffer_time
            window_end = current_time + buffer_time
            mean = temp.mean(window_start, window_end)
            result[current_time] = mean
            current_time += period_time
        return result

    def mean(self, start_time=None, end_time=None):
        """This calculated the average value of the time series over the given
        time range from `start_time` to `end_time`.

        """
        if start_time is None:
            start_time = self.domain.start()
            if start_time == -inf:
                raise ValueError('Start time of the domain '
                                 'is negative infinity.'
                                 ' Cannot calculate mean without '
                                 'specifying a start time.')

        if end_time is None:
            end_time = self.domain.end()
            if start_time == inf:
                raise ValueError('End time of the domain '
                                 'is infinity.'
                                 ' Cannot calculate mean without '
                                 'specifying an end time.')

        if start_time == -inf or end_time == inf:
            raise ValueError('Start/end time cannot be infinity.')

        if start_time > end_time:
            msg = (
                "Can't calculate mean of a Timeseries "
                "when end_time <= start_time. "
                "Received start_time={} and end_time={}."
            ).format(start_time, end_time)
            raise ValueError(msg)

        if start_time < self.domain.start() or end_time > self.domain.end():
            message = (
                "Can't calculate mean of a Timeseries "
                "when end_time or "
                "start_time is outside of the domain. "
                "Received start_time={} and end_time={}. "
                "Domain is {}."
            ).format(start_time, end_time, self.get_domain())
            raise ValueError(message)

        if self.domain.n_intervals() > 1:
            raise NotImplementedError(
                'Cannot calculate mean when Domain is not connected.')

        total_seconds = utils.duration_to_number(end_time - start_time)

        mean = 0.0
        for (t0, t1, value) in self.iterperiods(start_time, end_time):
            # calculate contribution to weighted average for this
            # interval
            try:
                mean += (utils.duration_to_number(t1 - t0) * value)
            except TypeError:
                msg = "Can't take mean of non-numeric type (%s)" % type(value)
                raise TypeError(msg)

        # return the mean value over the time period
        return mean / float(total_seconds)

    def distribution(self, start_time=None, end_time=None,
                     normalized=True, mask=None):
        """Calculate the distribution of values over the given time range from
        `start_time` to `end_time`.

        Args:

            start_time (orderable, optional): The lower time bound of
                when to calculate the distribution. By default, the
                start of the domain will be used.

            end_time (orderable, optional): The upper time bound of
                when to calculate the distribution. By default, the
                end of the domain will be used.

            normalized (bool): If True, distribution will sum to
                one. If False and the time values of the TimeSeries
                are datetimes, the units will be seconds.

            mask (:obj:`Domain` or :obj:`TimeSeries`, optional): A
                Domain on which to calculate the distribution. This
                Domain is combined with a logical and with either the
                (start, end) time domain, if given, or the domain of
                the TimeSeries.

        Returns:

            :obj:`Histogram` with the results.

        Examples:

            TODO: need some examples.

        >>> print([i for i in example_generator(4)])
        [0, 1, 2, 3]

        """
        if start_time is None:
            start_time = self.domain.start()

        if end_time is None:
            end_time = self.domain.end()

        # if a TimeSeries is given as mask, convert to a domain
        if isinstance(mask, TimeSeries):
            mask = mask.to_domain()

        # logical and with start, end time domain
        distribution_mask = Domain([start_time, end_time])
        if mask:
            distribution_mask &= mask

        counter = histogram.Histogram()
        for start_time, end_time in distribution_mask.intervals():
            for t0, t1, value in self.iterperiods(start_time, end_time):
                counter[value] += utils.duration_to_number(
                    t1 - t0,
                    units='seconds',
                )

        # divide by total duration if result needs to be normalized
        if normalized:
            return counter.normalized()
        else:
            return counter

    def _check_time_series(self, other):
        """Function used to check the type of the argument and raise an
        informative error message if it's not a TimeSeries.

        """
        if not isinstance(other, TimeSeries):
            msg = "unsupported operand types(s) for +: %s and %s" % \
                (type(self), type(other))
            raise TypeError(msg)

    @staticmethod
    def _iter_merge(timeseries_list):
        """This function uses a priority queue to efficiently yield the (time,
        value_list) tuples that occur from merging together many time
        series.

        """
        # cast to list since this is getting iterated over several
        # times (causes problem if timeseries_list is a generator)
        timeseries_list = list(timeseries_list)

        # Create iterators for each timeseries and then add the first
        # item from each iterator onto a priority queue. The first
        # item to be popped will be the one with the lowest time
        queue = PriorityQueue()
        for index, timeseries in enumerate(timeseries_list):
            iterator = iter(timeseries)
            try:
                item = (next(iterator), index, iterator)
            except StopIteration:
                pass
            else:
                queue.put(item)

        # `state` keeps track of the value of the merged
        # TimeSeries. It starts with the default. It starts as a list
        # of the default value for each individual TimeSeries.
        state = [ts.default() for ts in timeseries_list]
        while not queue.empty():

            # get the next time with a measurement from queue
            (t, next_value), index, iterator = queue.get()

            # make a copy of previous state, and modify only the value
            # at the index of the TimeSeries that this item came from
            state = list(state)
            state[index] = next_value
            yield t, state

            # add the next measurement from the time series to the
            # queue (if there is one)
            try:
                queue.put((next(iterator), index, iterator))
            except StopIteration:
                pass

    @classmethod
    def iter_merge(cls, timeseries_list):
        """Iterate through several time series in order, yielding (time, list)
        tuples where list is the values of each individual TimeSeries
        in the list at time t.

        """

        if len(timeseries_list) == 0:
            raise ValueError(
                "timeseries_list is empty. There is nothing to merge.")

        domain = timeseries_list[0].domain
        for ts in timeseries_list:
            if len(ts) == 0:
                raise ValueError("Can't merge empty TimeSeries.")
            if not domain == ts.domain:
                raise ValueError(
                    "The domains of the TimeSeries are not the same.")

        # This function mostly wraps _iter_merge, the main point of
        # this is to deal with the case of tied times, where we only
        # want to yield the last list of values that occurs for any
        # group of tied times.
        index, previous_t, previous_state = -1, object(), object()
        for index, (t, state) in enumerate(cls._iter_merge(timeseries_list)):
            if index > 0 and t != previous_t:
                yield previous_t, previous_state
            previous_t, previous_state = t, state

        # only yield final thing if there was at least one element
        # yielded by _iter_merge
        if index > -1:
            yield previous_t, previous_state

    @classmethod
    def merge(cls, ts_list, compact=True, operation=None):
        """Iterate through several time series in order, yielding (time,
        `value`) where `value` is the either the list of each
        individual TimeSeries in the list at time t (in the same order
        as in ts_list) or the result of the optional `operation` on
        that list of values.

        """

        result = cls()
        for t, merged in cls.iter_merge(ts_list):
            if operation is None:
                value = merged
            else:
                value = operation(merged)
            result.set(t, value, compact=compact)
        return result

    @staticmethod
    def csv_time_transform(raw):
        return date_parse(raw)

    @staticmethod
    def csv_value_transform(raw):
        return str(raw)
    
    @classmethod
    def from_csv(cls, filename, time_column, value_column,
                 time_transform=None,
                 value_transform=None,
                 skip_header=True):

        # use default on class if not given
        if time_transform is None:
            time_transform = cls.csv_time_transform
        if value_transform is None:
            value_transform = cls.csv_value_transform

        result = cls()
        with open(filename) as infile:
            reader = csv.reader(infile)
            if skip_header:
                reader.next()
            for row in reader:
                time = time_transform(row[time_column])
                value = value_transform(row[value_column])
                result[time] = value
        return result
    
    def operation(self, other, function):
        """Calculate "elementwise" operation either between this TimeSeries
        and another one, i.e.

        operation(t) = function(self(t), other(t))

        or between this timeseries and a constant:

        operation(t) = function(self(t), other)

        If it's another time series, the measurement times in the
        resulting TimeSeries will be the union of the sets of
        measurement times of the input time series. If it's a
        constant, the measurement times will not change.

        """
        result = TimeSeries()
        if isinstance(other, TimeSeries):
            for time, value in self:
                result[time] = function(value, other[time])
            for time, value in other:
                result[time] = function(self[time], value)
        else:
            for time, value in self:
                result[time] = function(value, other)
        return result

    def to_domain(self, start_time=None, end_time=None):
        """"""
        intervals = []
        iterator = self.iterperiods(start_time=start_time, end_time=end_time)
        for t0, t1, value in iterator:
            if value:
                intervals.append((t0, t1))
        return Domain(intervals)

    def to_bool(self, invert=False):
        """Return the truth value of each element."""
        if invert:
            def function(x, y): return False if x else True
        else:
            def function(x, y): return True if x else False
        return self.operation(None, function)

    def threshold(self, value, inclusive=False):
        """Return True if > than treshold value (or >= threshold value if
        inclusive=True).

        """
        if inclusive:
            def function(x, y): return True if x >= y else False
        else:
            def function(x, y): return True if x > y else False
        return self.operation(value, function)

    def sum(self, other):
        """sum(x, y) = x(t) + y(t)."""
        return TimeSeries.merge([self, other], operation=sum)

    def difference(self, other):
        """difference(x, y) = x(t) - y(t)."""
        return self.operation(other, lambda x, y: x - y)

    def multiply(self, other):
        """mul(t) = self(t) * other(t)."""
        return self.operation(other, lambda x, y: x * y)

    def logical_and(self, other):
        """logical_and(t) = self(t) and other(t)."""
        return self.operation(other, lambda x, y: int(x and y))

    def logical_or(self, other):
        """logical_or(t) = self(t) or other(t)."""
        return self.operation(other, lambda x, y: int(x or y))

    def logical_xor(self, other):
        """logical_xor(t) = self(t) ^ other(t)."""
        return self.operation(other, lambda x, y: int(bool(x) ^ bool(y)))

    def __setitem__(self, time, value):
        """Allow a[time] = value syntax."""
        return self.set(time, value)

    def __getitem__(self, time):
        """Allow a[time] syntax."""
        return self.get(time)

    def __delitem__(self, time):
        """Allow del[time] syntax."""
        return self.remove(time)

    def __add__(self, other):
        """Allow a + b syntax"""
        return self.sum(other)

    def __radd__(self, other):
        """Allow the operation 0 + TimeSeries() so that builtin sum function
        works on an iterable of TimeSeries.

        """
        # skip type check if other is the integer 0
        if not other == 0:
            self._check_time_series(other)

        # 0 + self = self
        return self

    def __sub__(self, other):
        """Allow a - b syntax"""
        return self.difference(other)

    def __mul__(self, other):
        """Allow a * b syntax"""
        return self.multiply(other)

    def __and__(self, other):
        """Allow a & b syntax"""
        return self.logical_and(other)

    def __or__(self, other):
        """Allow a | b syntax"""
        return self.logical_or(other)

    def __xor__(self, other):
        """Allow a ^ b syntax"""
        return self.logical_xor(other)

    def __eq__(self, other):
        return self.items() == other.items()

    def __ne__(self, other):
        return not(self == other)
