"""Retired backoffice catalog owner ORM module.

D2C backoffice no longer owns product/SKU/unit/price-list tables. Product master
data comes from PMS projections, and D2C-owned merchant decisions live in listing
and pricing configuration tables.

This module is intentionally kept as an empty compatibility module for package
layout stability. Do not add SQLAlchemy models here.
"""
