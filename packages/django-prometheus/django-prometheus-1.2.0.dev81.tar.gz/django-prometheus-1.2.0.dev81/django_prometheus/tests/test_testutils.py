#!/usr/bin/env python
import unittest
from operator import itemgetter

import prometheus_client

from django_prometheus.testutils import PrometheusTestCaseMixin


class SomeTestCase(PrometheusTestCaseMixin):
    """A class that pretends to be a unit test."""

    def __init__(self):
        self.passes = True
        super(SomeTestCase, self).__init__()

    def assertEqual(self, left, right, *args, **kwargs):
        self.passes = self.passes and (left == right)

    def assertFalse(self, expression, *args, **kwargs):
        self.passes = self.passes and (not expression)


class PrometheusTestCaseMixinTest(unittest.TestCase):
    def setUp(self):
        self.registry = prometheus_client.CollectorRegistry()
        self.some_gauge = prometheus_client.Gauge(
            "some_gauge", "Some gauge.", registry=self.registry
        )
        self.some_gauge.set(42)
        self.some_labelled_gauge = prometheus_client.Gauge(
            "some_labelled_gauge",
            "Some labelled gauge.",
            ["labelred", "labelblue"],
            registry=self.registry,
        )
        self.some_labelled_gauge.labels("pink", "indigo").set(1)
        self.some_labelled_gauge.labels("pink", "royal").set(2)
        self.some_labelled_gauge.labels("carmin", "indigo").set(3)
        self.some_labelled_gauge.labels("carmin", "royal").set(4)
        self.t = SomeTestCase()

    def testGetMetrics(self):
        """Tests getMetric."""
        assert 42 == self.t.getMetric("some_gauge", registry=self.registry)
        assert 1 == self.t.getMetric(
            "some_labelled_gauge",
            registry=self.registry,
            labelred="pink",
            labelblue="indigo",
        )

    def testGetMetricVector(self):
        """Tests getMetricVector."""
        vector = self.t.getMetricVector(
            "some_nonexistent_gauge", registry=self.registry
        )
        assert [] == vector
        vector = self.t.getMetricVector("some_gauge", registry=self.registry)
        assert [({}, 42)] == vector
        vector = self.t.getMetricVector("some_labelled_gauge", registry=self.registry)
        assert sorted(
            [
                ({"labelred": u"pink", "labelblue": u"indigo"}, 1),
                ({"labelred": u"pink", "labelblue": u"royal"}, 2),
                ({"labelred": u"carmin", "labelblue": u"indigo"}, 3),
                ({"labelred": u"carmin", "labelblue": u"royal"}, 4),
            ],
            key=itemgetter(1),
        ) == sorted(vector, key=itemgetter(1))

    def testAssertMetricEquals(self):
        """Tests assertMetricEquals."""
        # First we test that a scalar metric can be tested.
        self.t.assertMetricEquals(42, "some_gauge", registry=self.registry)
        assert self.t.passes is True
        self.t.assertMetricEquals(43, "some_gauge", registry=self.registry)
        assert self.t.passes is False
        self.t.passes = True

        # Here we test that assertMetricEquals fails on nonexistent gauges.
        self.t.assertMetricEquals(42, "some_nonexistent_gauge", registry=self.registry)
        assert not self.t.passes
        self.t.passes = True

        # Here we test that labelled metrics can be tested.
        self.t.assertMetricEquals(
            1,
            "some_labelled_gauge",
            registry=self.registry,
            labelred="pink",
            labelblue="indigo",
        )
        assert self.t.passes is True
        self.t.assertMetricEquals(
            1,
            "some_labelled_gauge",
            registry=self.registry,
            labelred="tomato",
            labelblue="sky",
        )
        assert self.t.passes is False
        self.t.passes = True

    def testRegistrySaving(self):
        """Tests saveRegistry and frozen registries operations."""
        frozen_registry = self.t.saveRegistry(registry=self.registry)
        # Test that we can manipulate a frozen scalar metric.
        assert 42 == self.t.getMetricFromFrozenRegistry("some_gauge", frozen_registry)
        self.some_gauge.set(99)
        assert 42 == self.t.getMetricFromFrozenRegistry("some_gauge", frozen_registry)
        self.t.assertMetricDiff(
            frozen_registry, 99 - 42, "some_gauge", registry=self.registry
        )
        assert self.t.passes is True
        self.t.assertMetricDiff(
            frozen_registry, 1, "some_gauge", registry=self.registry
        )
        assert self.t.passes is False
        self.t.passes = True

        # Now test the same thing with a labelled metric.
        assert 1 == self.t.getMetricFromFrozenRegistry(
            "some_labelled_gauge", frozen_registry, labelred="pink", labelblue="indigo"
        )
        self.some_labelled_gauge.labels("pink", "indigo").set(5)
        assert 1 == self.t.getMetricFromFrozenRegistry(
            "some_labelled_gauge", frozen_registry, labelred="pink", labelblue="indigo"
        )
        self.t.assertMetricDiff(
            frozen_registry,
            5 - 1,
            "some_labelled_gauge",
            registry=self.registry,
            labelred="pink",
            labelblue="indigo",
        )
        assert self.t.passes is True
        self.t.assertMetricDiff(
            frozen_registry,
            1,
            "some_labelled_gauge",
            registry=self.registry,
            labelred="pink",
            labelblue="indigo",
        )
        assert self.t.passes is False
