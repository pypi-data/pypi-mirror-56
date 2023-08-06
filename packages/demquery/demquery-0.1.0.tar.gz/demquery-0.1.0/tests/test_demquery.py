#!/usr/bin/env python

"""Tests for `demquery` package."""

import pytest

from demquery import Query


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string




# dem
# dir(dem)
# dem.nodatavals
# dem.nodata
# dem = rasterio.open(vrt_path)
# folder = '/Users/kyle/github/mapping/nst-guide/create-database/data/raw/elevation'
# fnames = [
#     'USGS_NED_13_n33w117_IMG.img',
#     'USGS_NED_13_n34w117_IMG.img',
#     'USGS_NED_13_n35w117_IMG.img',
#     'USGS_NED_13_n35w118_IMG.img',
#     'USGS_NED_13_n35w119_IMG.img',
#     'USGS_NED_13_n36w118_IMG.img',
#     'USGS_NED_13_n36w119_IMG.img',
#     'USGS_NED_13_n37w119_IMG.img',
#     'USGS_NED_13_n38w119_IMG.img',
#     'USGS_NED_13_n38w120_IMG.img',
#     'USGS_NED_13_n39w120_IMG.img',
#     'USGS_NED_13_n39w121_IMG.img',
#     'USGS_NED_13_n40w121_IMG.img',
#     'USGS_NED_13_n40w122_IMG.img',
#     'USGS_NED_13_n41w122_IMG.img',
#     'USGS_NED_13_n42w122_IMG.img',
#     'USGS_NED_13_n42w123_IMG.img',
#     'USGS_NED_13_n42w124_IMG.img',
#     'USGS_NED_13_n43w123_IMG.img',
#     'USGS_NED_13_n44w122_IMG.img',
#     'USGS_NED_13_n44w123_IMG.img',
#     'USGS_NED_13_n45w122_IMG.img',
#     'USGS_NED_13_n46w122_IMG.img',
#     'USGS_NED_13_n46w123_IMG.img',
#     'USGS_NED_13_n47w122_IMG.img',
#     'USGS_NED_13_n48w122_IMG.img',
#     'USGS_NED_13_n49w121_IMG.img',
#     'USGS_NED_13_n49w122_IMG.img',
# ]
# paths = [folder + '/' + x for x in fnames]
# dem_paths = paths
# gdf = gpd.read_file(
#     '/Users/kyle/github/mapping/nst-guide/create-database/data/pct/line/halfmile/CA_Sec_A_tracks.geojson'
# )
# line = gdf.iloc[0].geometry
# points = [(x[0], x[1]) for x in line.coords]
#
# self = Query(dem_paths)
# res1 = np.array(self.query_points(points, interp_kind=None))
# res2 = np.array(self.query_points(points, interp_kind='linear'))
# res3 = np.array(self.query_points(points, interp_kind='cubic'))
# res4 = np.array(self.query_points(points, interp_kind='quintic'))
#
# from statistics import mean
#
# np.abs(res1 - res2).mean()
# np.abs(res1 - res3).mean()
# res1 - res2
# np.array(res1) - res2
#
# res1
