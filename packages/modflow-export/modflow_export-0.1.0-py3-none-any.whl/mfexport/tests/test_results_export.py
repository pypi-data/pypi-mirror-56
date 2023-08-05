import os
import pytest
from flopy.utils import binaryfile as bf
import numpy as np
import fiona
import rasterio
from shapely.geometry import box
from ..grid import load_modelgrid
from ..results import export_cell_budget, export_heads, export_drawdown, export_sfr_results


@pytest.fixture(scope='module')
def lpr_output_path(tmpdir):
    return os.path.join(tmpdir, 'lpr')


def check_files(outfiles, variables, kstpkper=None, layers=None):
    replace = [('model_top', 'top')]
    variables = set(variables)
    if kstpkper is not None and np.isscalar(kstpkper[0]):
        kstpkper = [kstpkper]
    written = set()
    for f in outfiles:
        assert os.path.getsize(f) > 0
        fname = os.path.split(f)[1]
        for pair in replace:
            fname = fname.replace(*pair)
        props = parse_fname(fname)
        assert props['var'] in variables
        written.add(props['var'])
        if kstpkper is not None:
            assert (props['stp'], props['per']) in kstpkper
        if props['lay'] is not None:
            assert props['lay'] in layers
    # verify that all variables were exported
    assert len(written.difference(variables)) == 0


def parse_fname(fname):
    props = {'var': None,
             'lay': None,
             'per': None,
             'stp': None,
             'suffix': None}
    if 'stress_period_data' in fname:
        props['var'] = os.path.splitext(fname)[0]
        return props
    info = os.path.splitext(fname)[0].split('_')
    props['var'] = info.pop(0)
    for i in range(len(info)):
        item = info.pop(0)
        if 'ctr' in item:
            continue
        for p in ['lay', 'per', 'stp']:
            if p in item:
                props[p] = int(item.strip(p))
    return props


def compare_polygons(p1, p2, **kwargs):
    """Check that two polygons have the same extent"""
    assert np.allclose(p1.area, p2.area, **kwargs)
    assert np.allclose(p1.intersection(p2).area, p1.area, **kwargs)


def test_cell_budget_export(model):
    m, grid, output_path = model
    precision = 'single'
    binary_grid_file = None
    skip = []
    if m.version == 'mf6':
        precision = 'double'
        binary_grid_file = os.path.join(m.model_ws, '{}.dis.grb'.format(m.name))
        skip = ['WEL']
    file = os.path.join(m.model_ws, '{}.cbc'.format(m.name))
    #file = 'Examples/data/lpr/lpr_inset.cbc'
    assert os.path.exists(file)
    cbobj = bf.CellBudgetFile(file, precision=precision)
    layers = list(range(cbobj.nlay))
    kstpkper = cbobj.get_kstpkper()[0]
    variables = [bs.decode().strip() for bs in cbobj.textlist
                 if bs.decode().strip() not in skip]
    nrow, ncol = cbobj.nrow, cbobj.ncol
    cbobj.close()
    outfiles = export_cell_budget(file, grid,
                                  binary_grid_file=binary_grid_file,
                                  kstpkper=kstpkper,
                                  precision=precision,
                                  output_path=output_path)
    check_files(outfiles, variables, kstpkper)
    tifs = [f for f in outfiles if f.endswith('.tif')]
    for f in tifs:
        with rasterio.open(f) as src:
            assert src.width == ncol
            assert src.height == nrow
            compare_polygons(grid.bbox, box(*src.bounds))


def test_heads_export(model):
    m, grid, output_path = model
    file = os.path.join(m.model_ws, '{}.hds'.format(m.name))
    #file = 'Examples/data/lpr/lpr_inset.hds'
    variables = ['hds', 'wt']
    hdsobj = bf.HeadFile(file)
    kstpkper = hdsobj.get_kstpkper()[-1:]
    layers = list(range(hdsobj.nlay))
    nrow, ncol = hdsobj.nrow, hdsobj.ncol
    hdsobj.close()
    outfiles = export_heads(file, grid, -1e4, -9999,
                 kstpkper=kstpkper,
                 output_path=output_path)
    check_files(outfiles, variables, kstpkper, layers)
    tifs = [f for f in outfiles if f.endswith('.tif')]
    for f in tifs:
        with rasterio.open(f) as src:
            assert src.width == ncol
            assert src.height == nrow
            compare_polygons(grid.bbox, box(*src.bounds))
    shps = [f for f in outfiles if f.endswith('.shp')]
    for f in shps:
        with fiona.open(f) as src:
            assert box(*src.bounds).within(grid.bbox)
            #compare_polygons(grid.bbox, box(*src.bounds), rtol=0.1)


def test_drawdown_export(model):
    m, grid, output_path = model
    file = os.path.join(m.model_ws, '{}.hds'.format(m.name))
    #file = 'Examples/data/lpr/lpr_inset.hds'
    variables = ['ddn', 'wt-ddn']
    hdsobj = bf.HeadFile(file)
    kstpkper0 = hdsobj.get_kstpkper()[1]
    kstpkper1 = hdsobj.get_kstpkper()[-1]
    layers = list(range(hdsobj.nlay))
    nrow, ncol = hdsobj.nrow, hdsobj.ncol
    hdsobj.close()
    outfiles = export_drawdown(file, grid, -1e4, -9999,
                               kstpkper0=kstpkper0,
                               kstpkper1=kstpkper1,
                               output_path=output_path)
    check_files(outfiles, variables, [kstpkper1], layers)
    tifs = [f for f in outfiles if f.endswith('.tif')]
    for f in tifs:
        with rasterio.open(f) as src:
            assert src.width == ncol
            assert src.height == nrow
            compare_polygons(grid.bbox, box(*src.bounds))
    shps = [f for f in outfiles if f.endswith('.shp')]
    for f in shps:
        with fiona.open(f) as src:
            assert box(*src.bounds).within(grid.bbox)


def test_sfr_results_export(lpr_model, lpr_modelgrid, lpr_output_path):
    mf2005_sfr_outputfile = 'Examples/data/lpr/lpr_inset.sfr.out'
    kstpkper = [(4, 0)]
    variables = ['sfrout', 'baseflow', 'qaquifer']
    outfiles = export_sfr_results(mf2005_sfr_outputfile=mf2005_sfr_outputfile,
                                  model=lpr_model,
                                  grid=lpr_modelgrid,
                                  kstpkper=kstpkper,
                                  output_length_units='feet',
                                  output_time_units='seconds',
                                  output_path=lpr_output_path
                                  )
    check_files(outfiles, variables, kstpkper)


def test_mf6sfr_results_export(shellmound_model, shellmound_modelgrid, shellmound_output_path):
    mf6_sfr_stage_file = os.path.join(shellmound_model.model_ws, '{}.sfr.stage.bin'
                                      .format(shellmound_model.name))
    mf6_sfr_budget_file = os.path.join(shellmound_model.model_ws, '{}.sfr.cbc'
                                       .format(shellmound_model.name))
    hdsobj = bf.HeadFile(mf6_sfr_stage_file, text='stage')
    kstpkper = hdsobj.get_kstpkper()[:1] + hdsobj.get_kstpkper()[-1:]
    variables = ['sfrout', 'baseflow', 'qaquifer']
    outfiles = export_sfr_results(mf6_sfr_stage_file=mf6_sfr_stage_file,
                                  mf6_sfr_budget_file=mf6_sfr_budget_file,
                                  model=shellmound_model,
                                  grid=shellmound_modelgrid,
                                  kstpkper=kstpkper,
                                  output_length_units='feet',
                                  output_time_units='seconds',
                                  output_path=shellmound_output_path
                                  )
    check_files(outfiles, variables, kstpkper)


def test_parse_fname():
    fname = 'wel0_stress_period_data.shp'
    result = parse_fname(fname)
    assert result['var'] == os.path.splitext(fname)[0]