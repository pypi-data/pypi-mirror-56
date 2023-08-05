from . import wellpath
from .drill_op import input, main


def drilling(n, mdt=3000, casings=[], wellpath_data=[], bit=0.216, deltaz=50, profile='V', build_angle=1, kop=0, eob=0,
             sod=0, eod=0, kop2=0, eob2=0, wellpath_mode=0, wellpath_load_mode=0):
    tdata = drill_op.input.data(casings, bit)
    if wellpath_mode == 0:
        depths = wellpath.get(mdt, deltaz, profile, build_angle, kop, eob, sod, eod, kop2, eob2)
    if wellpath_mode == 1:
        depths = wellpath.load(wellpath_data, deltaz, wellpath_load_mode)
    well = input.set_well(tdata, depths)
    temp = main.temp_time(n, well)
    return temp
