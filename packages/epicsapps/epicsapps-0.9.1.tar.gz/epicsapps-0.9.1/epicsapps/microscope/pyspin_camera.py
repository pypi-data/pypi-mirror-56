import time
import atexit
from PIL import Image
import numpy as np
import wx

try:
    import PySpin
except ImportError:
    print("Cannot load PySpin library")

def map_attrs(object):
    out = {}
    for attr in dir(object):
        if attr.startswith('_'):
            continue
        out[attr.lower()] = getattr(object, attr)
    return out

pixel_formats = {'bgr': PySpin.PixelFormat_BGR8,
                 'rgb8': PySpin.PixelFormat_RGB8,
                 'rgb': PySpin.PixelFormat_RGB8,
                 'mono': PySpin.PixelFormat_Mono8}

pixel_formats['rgb'] = PySpin.PixelFormat_RGB8
# pixel_formats['rgb'] = PySpin.PixelFormat_BayerRG8


integer_props = ['Width', 'Height', 'OffsetX', 'OffsetY']

float_props = ['Gain', 'Gamma', 'ExposureTime']
float_props = ['Gain', 'ExposureTime']
balance_props = ['WhiteBalance']

all_props = balance_props + float_props + integer_props

class PySpinCamera(object):
    """PySpin Camera object"""
    def __init__(self, camera_id=0):
        self._system = PySpin.System.GetInstance()
        self.cam = None
        self.device_id = None
        self.camera_id = camera_id
        # DEFAULT, NO_COLOR_PROCESSING, NEAREST_NEIGHBOR, EDGE_SENSING, HQ_LINEAR,
        # RIGOROUS, IPP, DIRECTIONAL_FILTER, WEIGHTED_DIRECTIONAL_FILTER
        # PySpin.NEAREST_NEIGHBOR)
        self.convert_method = PySpin.DEFAULT
        self.Connect()
        atexit.register(self.Exit)

    def Connect(self):
        if self.cam is not None:
            return
        self._cameras = self._system.GetCameras()
        for cam in self._cameras:
            dev_id = cam.TLDevice.DeviceID.GetValue()
            dev_name = cam.TLDevice.DeviceModelName.GetValue()
            # print(dev_name, dev_id, int(dev_id) == int(self.camera_id))
            if int(dev_id) == int(self.camera_id):
                self.device_id = dev_id
                self.device_name = dev_name
                self.cam = cam
                break

        if self.cam is None:
            raise ValueError("PySpin camera %s not found!!" % repr(self.camera_id))

        self.device_version = self.cam.TLDevice.DeviceVersion.GetValue()
        self.nodemap_tldevice = self.cam.GetTLDeviceNodeMap()
        self.cam.Init()
        self.nodemap = self.cam.GetNodeMap()
        self.SetFullSize()

    def StartCapture(self):
        """start capture"""
        self.cam.Init()
        self.cam.BeginAcquisition()
        self.SetFramerate(14.25)
        self.SetExposureTime(30.0, auto=False)

    def StopCapture(self):
        """"""
        try:
            self.cam.EndAcquisition()
        except:
            pass

    def SetFramerate(self, framerate=14.5):
        acq_mode = PySpin.CEnumerationPtr(self.nodemap.GetNode('AcquisitionMode'))
        acq_mode.SetIntValue(acq_mode.GetEntryByName('Continuous').GetValue())

        arate = PySpin.CFloatPtr(self.nodemap.GetNode('AcquisitionFrameRate'))
        arate.SetValue(framerate*1.0)
        time.sleep(0.1)

    def Exit(self):
        self.StopCapture()
        self.cam.DeInit()
        self._cameras.Clear()
        del self.cam
        del self.nodemap
        self._system.ReleaseInstance()

    def SetFullSize(self):
        ptr = PySpin.CIntegerPtr
        for name in ('Height', 'Width'):
            prop = ptr(self.nodemap.GetNode(name))
            prop.SetValue(prop.GetMax())
        for name in ('OffsetX', 'OffsetY'):
            prop = ptr(self.nodemap.GetNode(name))
            prop.SetValue(0)
        # self.SetGamma(1.0)
        self.SetGain(1, auto=False)
        self.SetExposureTime(30.0, auto=False)

    def GetWhiteBalance(self):
        """ Get White Balance (red, blue)"""
        if True: # try:
            wb_auto = PySpin.CEnumerationPtr(self.nodemap.GetNode('BalanceWhiteAuto'))
            wb_auto.SetIntValue(wb_auto.GetEntryByName('Off').GetValue())
            wb_ratio = PySpin.CEnumerationPtr(self.nodemap.GetNode('BalanceRatioSelector'))

            # Blue
            wb_ratio.SetIntValue(wb_ratio.GetEntryByName('Blue').GetValue())
            blue = PySpin.CFloatPtr(self.nodemap.GetNode('BalanceRatio')).GetValue()

            # Red
            wb_ratio.SetIntValue(wb_ratio.GetEntryByName('Red').GetValue())
            red = PySpin.CFloatPtr(self.nodemap.GetNode('BalanceRatio')).GetValue()
            return blue, red
        else: # except:
            print("Could not get White Balance ")
            return 1, 1

    def GetGamma(self):
        """ Get Gamma"""
        try:
            return PySpin.CFloatPtr(self.nodemap.GetNode('Gamma')).GetValue()
        except:
            return 0

    def GetGain(self):
        """ Get Gain"""
        return PySpin.CFloatPtr(self.nodemap.GetNode('Gain')).GetValue()

    def GetExposureTime(self):
        """ Get Exposure Time (in milliseconds)"""
        usec = PySpin.CFloatPtr(self.nodemap.GetNode('ExposureTime')).GetValue()
        return usec * 1.e-3

    def SetWhiteBalance(self, blue, red, auto=False):
        """Set white balance blue, red values

        Arguments
        ---------
        blue     value for blue
        red      value for red
        auto     whether to set auto [default=False]

        """
        wb_auto = PySpin.CEnumerationPtr(self.nodemap.GetNode('BalanceWhiteAuto'))
        sauto = 'Off'
        if auto:
            wb_auto.SetIntValue(wb_auto.GetEntryByName('Once').GetValue())
        else:
            wb_auto.SetIntValue(wb_auto.GetEntryByName('Off').GetValue())
            wb_ratio = PySpin.CEnumerationPtr(self.nodemap.GetNode('BalanceRatioSelector'))

            # set Blue
            wb_ratio.SetIntValue(wb_ratio.GetEntryByName('Blue').GetValue())
            PySpin.CFloatPtr(self.nodemap.GetNode('BalanceRatio')).SetValue(blue)

            # set Red
            wb_ratio.SetIntValue(wb_ratio.GetEntryByName('Red').GetValue())
            PySpin.CFloatPtr(self.nodemap.GetNode('BalanceRatio')).SetValue(red)

    def SetGamma(self, value):
        """Set Gamma
        Arguments
        ---------
        value      gain value
        """
        pass
        # try:
        #     PySpin.CFloatPtr(self.nodemap.GetNode('Gamma')).SetValue(value)
        # except:
        #     pass # print(" no set gamma?")

    def SetGain(self, value=None, auto=False):
        """Set Gain
        Arguments
        ---------
        value      gain value
        auto       whether to set to auto [default=False]
        """
        node_main = self.nodemap.GetNode('Gain')
        node_auto = PySpin.CEnumerationPtr(self.nodemap.GetNode('GainAuto'))
        sauto = 'Off'
        if auto:
            sauto = 'Continuous'
        node_auto.SetIntValue(node_auto.GetEntryByName(sauto).GetValue())
        if (not auto) and value is not None:
            PySpin.CFloatPtr(node_main).SetValue(value)
        node_auto.SetIntValue(node_auto.GetEntryByName(sauto).GetValue())

    def SetExposureTime(self, value=None, auto=False):
        """Set Exposure Time
        Arguments
        ---------
        value      exposure time (in milliseconds)
        auto       whether to set to auto [default=False]
        """
        # print("Set Exposure Time ", value, auto)
        node_main = self.nodemap.GetNode('ExposureTime')
        node_auto = PySpin.CEnumerationPtr(self.nodemap.GetNode('ExposureAuto'))
        sauto = 'Off'
        if auto:
            sauto = 'Continuous'
        node_auto.SetIntValue(node_auto.GetEntryByName(sauto).GetValue())
        if (not auto) and value is not None:
            value *= 1.e3  # exposure time is in milliseconds
            PySpin.CFloatPtr(node_main).SetValue(value)
        node_auto.SetIntValue(node_auto.GetEntryByName(sauto).GetValue())

    def SetConvertMethod(self, method='DEFAULT'):
        # DEFAULT, NO_COLOR_PROCESSING, NEAREST_NEIGHBOR, EDGE_SENSING, HQ_LINEAR,
        # RIGOROUS, IPP, DIRECTIONAL_FILTER, WEIGHTED_DIRECTIONAL_FILTER
        # PySpin.NEAREST_NEIGHBOR)
        self.convert_method = getattr(PySpin, method, PySpin.DEFAULT)
        # print("Set Convert Method ", method, self.convert_method)


    def SaveImageFile(self, filename, format="jpg"):
        """save image to disk"""
        img = self.cam.GetNextImage()
        img.Convert(pixel_formats['rgb']).Save(filename)
        img.Release()

    def GetSize(self):
        """returns image size"""
        img = self.cam.GetNextImage()
        size = (img.GetHeight(), img.GetWidth())
        img.Release()
        return size

    def GrabColor(self, format='rgb'):
        return GrabNumPyImage(format=format)

    def GrabNumPyImage(self, format='rgb'):
        """return an image as a NumPy array
        optionally specifying color
        """
        img = self.cam.GetNextImage()
        ncols, nrows = img.GetHeight(), img.GetWidth()
        size = ncols * nrows
        shape = (ncols, nrows)
        if format in ('rgb', 'bgr'):
            shape = (ncols, nrows, 3)
        # print("Grab NP Image ", pixel_formats[format], format, self.convert_method, time.time()-self.t0)
        out = img.Convert(pixel_formats[format], self.convert_method)
        img.Release()
        return out.GetData().reshape(shape)

    def GrabWxImage(self, scale=1.00, rgb=True, quality=wx.IMAGE_QUALITY_HIGH):
        """returns a wximage
        optionally specifying scale and color
        """
        t0 = time.time()
        img = self.cam.GetNextImage()
        ncols, nrows = img.GetHeight(), img.GetWidth()
        scale = max(scale, 0.05)
        width, height = int(scale*nrows), int(scale*ncols)
        format = 'mono'
        if rgb:
            format = 'rgb'
        out = img.Convert(pixel_formats[format], self.convert_method)
        self.data = out.GetData()
        self.data.shape = (ncols, nrows, 3)
        img.Release()
        return wx.Image(nrows, ncols, self.data).Rescale(width, height)

    def GrabPILImage(self):
        """"""
        # We import PIL here so that PIL is only a requirement if you need PIL
        img = self.cam.GetNextImage()
        ncols, nrows = img.GetHeight(), img.GetWidth()
        out = Image.frombytes('L', (ncols, nrows), img.GetData())
        img.Release()
        return out
