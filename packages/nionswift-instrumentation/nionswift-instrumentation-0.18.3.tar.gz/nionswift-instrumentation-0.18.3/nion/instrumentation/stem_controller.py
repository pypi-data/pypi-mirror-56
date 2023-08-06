# standard libraries
import asyncio
import copy
import enum
import functools
import gettext
import math
import threading
import typing

# third party libraries
# None

# local libraries
from nion.swift.model import Graphics
from nion.swift.model import HardwareSource
from nion.utils import Binding
from nion.utils import Event
from nion.utils import Geometry
from nion.utils import Model
from nion.utils import Registry


_ = gettext.gettext


class PMTType(enum.Enum):
    DF = 0
    BF = 1


class SubscanState(enum.Enum):
    INVALID = -1
    DISABLED = 0
    ENABLED = 1


AxisType = typing.Tuple[str, str]


class ScanContext:
    def __init__(self):
        self.center_nm = None
        self.fov_size_nm = None
        self.rotation_rad = None

    def __repr__(self) -> str:
        return f"{self.fov_size_nm[0]}nm {math.degrees(self.rotation_rad)}deg" if self.fov_size_nm else "NO CONTEXT"

    def __eq__(self, other) -> bool:
        return other is not None and isinstance(other, self.__class__) and other.center_nm == self.center_nm and other.fov_size_nm == self.fov_size_nm and other.rotation_rad == self.rotation_rad

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        result.center_nm = self.center_nm
        result.fov_size_nm = self.fov_size_nm
        result.rotation_rad = self.rotation_rad
        return result

    @property
    def is_valid(self) -> bool:
        return self.fov_size_nm is not None

    def clear(self) -> None:
        self.center_nm = None
        self.fov_size_nm = None
        self.rotation_rad = None

    def update(self, center_nm: Geometry.FloatPoint, fov_size_nm: Geometry.FloatSize, rotation_rad: float) -> None:
        self.center_nm = Geometry.FloatPoint.make(center_nm)
        self.fov_size_nm = Geometry.FloatSize.make(fov_size_nm)
        self.rotation_rad = rotation_rad


class STEMController:
    """An interface to a STEM microscope.

    Methods and properties starting with a single underscore are called internally and shouldn't be called by general
    clients.

    Methods starting with double underscores are private.

    Probe
    -----
    probe_state (parked, blanked, scanning)
    probe_position (fractional coordinates, optional)
    set_probe_position(probe_position)
    validate_probe_position()

    probe_state_changed_event (probe_state, probe_position)
    """

    def __init__(self):
        self.__probe_position_value = Model.PropertyModel()
        self.__probe_position_value.on_value_changed = self.set_probe_position
        self.__probe_state_stack = list()  # parked, or scanning
        self.__probe_state_stack.append("parked")
        self.__scan_context = ScanContext()
        self.probe_state_changed_event = Event.Event()
        self.__subscan_state_value = Model.PropertyModel(SubscanState.INVALID)
        self.__subscan_region_value = Model.PropertyModel(None)
        self.__subscan_rotation_value = Model.PropertyModel(0.0)
        self.scan_data_item_states_changed_event = Event.Event()
        self.__ronchigram_camera = None
        self.__eels_camera = None
        self.__scan_controller = None

    def close(self):
        pass

    # configuration methods

    @property
    def ronchigram_camera(self) -> HardwareSource.HardwareSource:
        if self.__ronchigram_camera:
            return self.__ronchigram_camera
        return Registry.get_component("ronchigram_camera_hardware_source")

    def set_ronchigram_camera(self, camera: HardwareSource.HardwareSource) -> None:
        assert camera.features.get("is_ronchigram_camera", False)
        self.__ronchigram_camera = camera

    @property
    def eels_camera(self) -> HardwareSource.HardwareSource:
        if self.__eels_camera:
            return self.__eels_camera
        return Registry.get_component("eels_camera_hardware_source")

    def set_eels_camera(self, camera: HardwareSource.HardwareSource) -> None:
        assert camera.features.get("is_eels_camera", False)
        self.__eels_camera = camera

    @property
    def scan_controller(self) -> HardwareSource.HardwareSource:
        if self.__scan_controller:
            return self.__scan_controller
        return Registry.get_component("scan_hardware_source")

    def set_scan_controller(self, scan_controller: HardwareSource.HardwareSource) -> None:
        self.__scan_controller = scan_controller

    # end configuration methods

    def _enter_scanning_state(self) -> None:
        # push 'scanning' onto the probe state stack; the `probe_state` will now be `scanning`
        self.__probe_state_stack.append("scanning")
        # fire off the probe state changed event.
        self.probe_state_changed_event.fire(self.probe_state, self.probe_position)
        # ensure that SubscanState is valid (ENABLED or DISABLED, not INVALID)
        if self._subscan_state_value.value == SubscanState.INVALID:
            self._subscan_state_value.value = SubscanState.DISABLED

    def _exit_scanning_state(self) -> None:
        # pop the 'scanning' probe state and fire off the probe state changed event.
        self.__probe_state_stack.pop()
        self.probe_state_changed_event.fire(self.probe_state, self.probe_position)

    def _enter_synchronized_state(self, scan_controller: HardwareSource.HardwareSource, *, camera: HardwareSource.HardwareSource=None) -> None:
        pass

    def _exit_synchronized_state(self, scan_controller: HardwareSource.HardwareSource, *, camera: HardwareSource.HardwareSource=None) -> None:
        pass

    @property
    def _probe_position_value(self):
        """Internal use."""
        return self.__probe_position_value

    @property
    def _subscan_state_value(self):
        """Internal use."""
        return self.__subscan_state_value

    @property
    def _subscan_region_value(self):
        """Internal use."""
        return self.__subscan_region_value

    @property
    def _subscan_rotation_value(self):
        """Internal use."""
        return self.__subscan_rotation_value

    def disconnect_probe_connections(self):
        self.scan_data_item_states_changed_event.fire(list())

    def _data_item_states_changed(self, data_item_states):
        if len(data_item_states) > 0:
            self.scan_data_item_states_changed_event.fire(data_item_states)

    @property
    def scan_context(self) -> ScanContext:
        return self.__scan_context

    def _update_scan_context(self, center_nm: Geometry.FloatPoint, fov_size_nm: Geometry.FloatSize, rotation_rad: float) -> None:
        self.__scan_context.update(center_nm, fov_size_nm, rotation_rad)

    def _clear_scan_context(self) -> None:
        self.__scan_context.clear()

    @property
    def probe_position(self):
        """ Return the probe position, in normalized coordinates with origin at top left. Only valid if probe_state is 'parked'."""
        return self.__probe_position_value.value

    @probe_position.setter
    def probe_position(self, value):
        self.set_probe_position(value)

    def set_probe_position(self, new_probe_position):
        """ Set the probe position, in normalized coordinates with origin at top left. """
        if new_probe_position is not None:
            # convert the probe position to a FloatPoint and limit it to the 0.0 to 1.0 range in both axes.
            new_probe_position = Geometry.FloatPoint.make(new_probe_position)
            new_probe_position = Geometry.FloatPoint(y=max(min(new_probe_position.y, 1.0), 0.0),
                                                     x=max(min(new_probe_position.x, 1.0), 0.0))
        old_probe_position = self.__probe_position_value.value
        if ((old_probe_position is None) != (new_probe_position is None)) or (old_probe_position != new_probe_position):
            # this path is only taken if set_probe_position is not called as a result of the probe_position model
            # value changing.
            self.__probe_position_value.value = new_probe_position
        # update the probe position for listeners and also explicitly update for probe_graphic_connections.
        self.probe_state_changed_event.fire(self.probe_state, self.probe_position)

    def validate_probe_position(self):
        """Validate the probe position.

        This is called when the user switches from not controlling to controlling the position."""
        self.set_probe_position(Geometry.FloatPoint(y=0.5, x=0.5))

    @property
    def probe_state(self) -> str:
        """Probe state is the current probe state and can be 'parked', or 'scanning'."""
        return self.__probe_state_stack[-1]

    # instrument API

    def set_control_output(self, name, value, options=None):
        options = options if options else dict()
        value_type = options.get("value_type", "output")
        inform = options.get("inform", False)
        confirm = options.get("confirm", False)
        confirm_tolerance_factor = options.get("confirm_tolerance_factor", 1.0)  # instrument keeps track of default; this is a factor applied to the default
        confirm_timeout = options.get("confirm_timeout", 16.0)
        if value_type == "output":
            if inform:
                self.InformControl(name, value)
            elif confirm:
                if not self.SetValAndConfirm(name, value, confirm_tolerance_factor, int(confirm_timeout * 1000)):
                    raise TimeoutError("Setting '" + name + "'.")
            else:
                self.SetVal(name, value)
        elif value_type == "delta" and not inform:
            self.SetValDelta(name, value)
        else:
            raise NotImplemented()

    def get_control_output(self, name):
        return self.GetVal(name)

    def get_control_state(self, name):
        value_exists, value = self.TryGetVal(name)
        return "unknown" if value_exists else None

    def get_property(self, name):
        if name in ("probe_position", "probe_state"):
            return getattr(self, name)
        return self.get_control_output(name)

    def set_property(self, name, value):
        if name in ("probe_position"):
            return setattr(self, name, value)
        return self.set_control_output(name, value)

    def apply_metadata_groups(self, properties: typing.Dict, metatdata_groups: typing.Tuple[typing.List[str], str]) -> None:
        """Apply metadata groups to properties.

        Metadata groups is a tuple with two elements. The first is a list of strings representing a dict-path in which
        to add the controls. The second is a control group from which to read a list of controls to be added as name
        value pairs to the dict-path.
        """
        pass

    # end instrument API

    # required functions (templates). subclasses should override.

    def TryGetVal(self, s: str) -> (bool, float):
        return False, None

    def GetVal(self, s: str, default_value: float=None) -> float:
        raise Exception(f"No element named '{s}' exists! Cannot get value.")

    def SetVal(self, s: str, val: float) -> bool:
        return False

    def SetValWait(self, s: str, val: float, timeout_ms: int) -> bool:
        return False

    def SetValAndConfirm(self, s: str, val: float, tolfactor: float, timeout_ms: int) -> bool:
        return False

    def SetValDelta(self, s: str, delta: float) -> bool:
        return False

    def SetValDeltaAndConfirm(self, s: str, delta: float, tolfactor: float, timeout_ms: int) -> bool:
        return False

    def InformControl(self, s: str, val: float) -> bool:
        return False

    def GetVal2D(self, s:str, default_value: Geometry.FloatPoint=None, *, axis: AxisType) -> Geometry.FloatPoint:
        raise Exception(f"No 2D element named '{s}' exists! Cannot get value.")

    def SetVal2D(self, s:str, value: Geometry.FloatPoint, *, axis: AxisType) -> bool:
        return False

    def SetVal2DAndConfirm(self, s: str, val: Geometry.FloatPoint, tolfactor: float, timeout_ms: int, *, axis: AxisType) -> bool:
        return False

    def SetVal2DDelta(self, s: str, delta: Geometry.FloatPoint, *, axis: AxisType) -> bool:
        return False

    def SetVal2DDeltaAndConfirm(self, s: str, delta: Geometry.FloatPoint, tolfactor: float, timeout_ms: int, *, axis: AxisType) -> bool:
        return False

    def InformControl2D(self, s: str, val: Geometry.FloatPoint, *, axis: AxisType) -> bool:
        return False

    # end required functions

    # high level commands

    def change_stage_position(self, *, dy: int=None, dx: int=None):
        """Shift the stage by dx, dy (meters). Do not wait for confirmation."""
        raise NotImplemented()

    def change_pmt_gain(self, pmt_type: PMTType, *, factor: float) -> None:
        """Change specified PMT by factor. Do not wait for confirmation."""
        raise NotImplemented()

    # end high level commands


class PropertyToGraphicBinding(Binding.PropertyBinding):

    """
        Binds a property of an operation item to a property of a graphic item.
    """

    def __init__(self, event_loop, region, region_property_name, graphic, graphic_property_name):
        super().__init__(region, region_property_name)
        self.__graphic = graphic
        self.__graphic_property_changed_listener = graphic.property_changed_event.listen(self.__property_changed)
        self.__graphic_property_name = graphic_property_name
        self.__region_property_name = region_property_name
        self.__task = None
        def set_target_value(value):
            async def do_set_value():
                if value is not None:
                    setattr(self.__graphic, graphic_property_name, value)
                self.__task = None
            if self.__task:
                self.__task.cancel()
            self.__task = event_loop.create_task(do_set_value())
        self.target_setter = set_target_value

    def close(self):
        if self.__task:
            self.__task.cancel()
            self.__task = None
        self.__graphic_property_changed_listener.close()
        self.__graphic_property_changed_listener = None
        self.__graphic = None
        super().close()

    # watch for property changes on the graphic.
    def __property_changed(self, property_name):
        if property_name == self.__graphic_property_name:
            old_property_value = getattr(self.source, self.__region_property_name)
            # to prevent message loops, check to make sure it changed
            property_value = getattr(self.__graphic, property_name)
            if property_value is not None:
                property_value = Geometry.FloatPoint(y=property_value[0], x=property_value[1])
            if property_value != old_property_value:
                self.update_source(property_value)


class ProbeGraphicConnection:
    """Manage the connection between the hardware and the graphics representing the probe on a display."""

    def __init__(self, event_loop, display_item, probe_position_value, hide_probe_graphics_fn):
        self.event_loop = event_loop
        self.display_item = display_item
        self.probe_position_value = probe_position_value
        self.graphic = None
        self.binding = None
        self.remove_region_graphic_event_listener = None
        self.hide_probe_graphics_fn = hide_probe_graphics_fn

    def close(self):
        graphic = self.graphic
        self.hide_probe_graphic()
        if graphic:
            self.display_item.remove_graphic(graphic)

    def update_probe_state(self, probe_position):
        if probe_position is not None:
            self.probe_position_value.value = probe_position
            self.show_probe_graphic()
        else:
            graphic = self.graphic
            self.hide_probe_graphic()
            if graphic:
                self.display_item.remove_graphic(graphic)
        if self.graphic:
            self.graphic.color = "#F80"

    def show_probe_graphic(self):
        if not self.graphic:
            self.graphic = Graphics.PointGraphic()
            self.graphic.graphic_id = "probe"
            self.graphic.label = _("Probe")
            self.graphic.position = self.probe_position_value.value
            self.graphic.is_bounds_constrained = True
            self.display_item.add_graphic(self.graphic)
            self.binding = PropertyToGraphicBinding(self.event_loop, self.probe_position_value, "value", self.graphic, "position")
            def graphic_removed():
                self.hide_probe_graphic()
                # next make sure all other probe graphics get hidden so that setting the probe_position_value
                # doesn't set graphics positions to None
                self.hide_probe_graphics_fn()
                self.probe_position_value.value = None
            def display_removed():
                self.hide_probe_graphic()
            self.remove_region_graphic_event_listener = self.graphic.about_to_be_removed_event.listen(graphic_removed)
            self.display_about_to_be_removed_listener = self.display_item.about_to_be_removed_event.listen(display_removed)

    def hide_probe_graphic(self):
        if self.graphic:
            self.binding.close()
            self.binding = None
            self.remove_region_graphic_event_listener.close()
            self.remove_region_graphic_event_listener = None
            self.display_about_to_be_removed_listener.close()
            self.display_about_to_be_removed_listener = None
            self.graphic = None


class ProbeView:
    """Observes the probe (STEM controller) and updates data items and graphics."""

    def __init__(self, stem_controller: STEMController, document_model, event_loop: asyncio.AbstractEventLoop):
        assert event_loop is not None
        self.__document_model = document_model
        self.__event_loop = event_loop
        self.__last_data_items_lock = threading.RLock()
        self.__last_data_items = list()
        self.__probe_state = None
        self.__probe_graphic_connections = list()
        self.__probe_position_value = stem_controller._probe_position_value
        self.__probe_state_changed_listener = stem_controller.probe_state_changed_event.listen(self.__probe_state_changed)
        self.__probe_data_items_changed_listener = stem_controller.scan_data_item_states_changed_event.listen(self.__probe_data_item_states_changed)

    def close(self):
        self.__probe_data_items_changed_listener.close()
        self.__probe_data_items_changed_listener = None
        self.__probe_state_changed_listener.close()
        self.__probe_state_changed_listener = None
        self.__last_data_items = list()
        self.__event_loop = None

    def __probe_data_item_states_changed(self, data_item_states):
        # thread safe.
        if not any(data_item_state.get("channel_id").endswith("_subscan") for data_item_state in data_item_states):
            with self.__last_data_items_lock:
                self.__last_data_items = [data_item_state.get("data_item") for data_item_state in data_item_states]

    def __probe_state_changed(self, probe_state, probe_position):
        # thread safe. move actual call to main thread using the event loop.
        self.__latest_probe_state = probe_state
        self.__latest_probe_position = probe_position
        self.__event_loop.create_task(self.__update_probe_state())

    async def __update_probe_state(self):
        # thread unsafe. always called on main thread (via event loop).
        # don't pass arguments to this function; instead use 'latest' values.
        # this helps avoid strange cyclic updates.
        probe_state = self.__latest_probe_state
        probe_position = self.__latest_probe_position
        if probe_state != self.__probe_state:
            if probe_state == "scanning":
                self.__hide_probe_graphics()
            else:
                self.__show_probe_graphics(probe_position)
            self.__probe_state = probe_state
        self.__update_probe_graphics(probe_position)

    def __hide_probe_graphics(self):
        # thread unsafe.
        probe_graphic_connections = copy.copy(self.__probe_graphic_connections)
        self.__probe_graphic_connections = list()
        for probe_graphic_connection in probe_graphic_connections:
            probe_graphic_connection.close()

    def __show_probe_graphics(self, probe_position):
        # thread unsafe.
        with self.__last_data_items_lock:
            data_items = self.__last_data_items
            # self.__last_data_items = list()
        for data_item in data_items:
            # scanning has stopped, figure out the displays that might be used to display the probe position
            # then watch for changes to that list. changes will include the display being removed by the user
            # or newer more appropriate displays becoming available.
            display_item = self.__document_model.get_display_item_for_data_item(data_item)
            if display_item:
                # the probe position value object gives the ProbeGraphicConnection the ability to
                # get, set, and watch for changes to the probe position.
                probe_graphic_connection = ProbeGraphicConnection(self.__event_loop, display_item, self.__probe_position_value, self.__hide_probe_graphics)
                probe_graphic_connection.update_probe_state(probe_position)
                self.__probe_graphic_connections.append(probe_graphic_connection)

    def __update_probe_graphics(self, probe_position):
        # thread unsafe.
        for probe_graphic_connection in self.__probe_graphic_connections:
            probe_graphic_connection.update_probe_state(probe_position)


class SubscanView:
    """Observes the STEM controller and updates data items and graphics."""

    def __init__(self, stem_controller: STEMController, document_model, event_loop: asyncio.AbstractEventLoop):
        assert event_loop is not None
        self.__document_model = document_model
        self.__event_loop = event_loop
        self.__last_data_items_lock = threading.RLock()
        self.__scan_data_items = list()
        self.__subscan_connections = list()
        self.__subscan_state_model = stem_controller._subscan_state_value
        self.__subscan_region_value = stem_controller._subscan_region_value
        self.__subscan_rotation_value = stem_controller._subscan_rotation_value
        self.__subscan_region_changed_listener = stem_controller._subscan_region_value.property_changed_event.listen(self.__subscan_region_changed)
        self.__subscan_rotation_changed_listener = stem_controller._subscan_rotation_value.property_changed_event.listen(self.__subscan_rotation_changed)
        self.__scan_data_items_changed_listener = stem_controller.scan_data_item_states_changed_event.listen(self.__scan_data_item_states_changed)
        self.__subscan_graphic_trackers = list()
        self.__update_subscan_region_value = None
        self.__update_subscan_rotation_value = 0.0

    def close(self):
        self.__scan_data_items_changed_listener.close()
        self.__scan_data_items_changed_listener = None
        self.__scan_data_items = list()
        self.__event_loop = None

    def __scan_data_item_states_changed(self, data_item_states):
        # thread safe.
        if self.__subscan_state_model.value == SubscanState.DISABLED:
            with self.__last_data_items_lock:
                self.__scan_data_items = [data_item_state.get("data_item") for data_item_state in data_item_states]

    def __subscan_region_changed(self, name):
        # pass the value to update subscan region via the field; that way less worry about overruns
        self.__update_subscan_region_value = self.__subscan_region_value.value
        self.__event_loop.create_task(self.__update_subscan_region())

    def __subscan_rotation_changed(self, name):
        # pass the value to update subscan region via the field; that way less worry about overruns
        self.__update_subscan_rotation_value = self.__subscan_rotation_value.value
        self.__event_loop.create_task(self.__update_subscan_region())

    async def __update_subscan_region(self):
        subscan_region = self.__update_subscan_region_value
        subscan_rotation = self.__update_subscan_rotation_value
        with self.__last_data_items_lock:
            scan_data_items = self.__scan_data_items
        if subscan_region:
            # create subscan graphics for each scan data item if it doesn't exist
            if not self.__subscan_graphic_trackers:
                for scan_data_item in scan_data_items:
                    display_item = self.__document_model.get_display_item_for_data_item(scan_data_item)
                    if display_item:
                        subscan_graphic = Graphics.RectangleGraphic()
                        subscan_graphic.graphic_id = "subscan"
                        subscan_graphic.label = _("Subscan")
                        subscan_graphic.bounds = subscan_region
                        subscan_graphic.rotation = subscan_rotation
                        subscan_graphic.is_bounds_constrained = True

                        def subscan_graphic_property_changed(subscan_graphic, name):
                            if name == "bounds":
                                self.__subscan_region_value.value = subscan_graphic.bounds
                            if name == "rotation":
                                self.__subscan_rotation_value.value = subscan_graphic.rotation

                        subscan_graphic_property_changed_listener = subscan_graphic.property_changed_event.listen(functools.partial(subscan_graphic_property_changed, subscan_graphic))

                        def graphic_removed(subscan_graphic):
                            self.__remove_one_subscan_graphic(subscan_graphic)
                            self.__subscan_state_model.value = SubscanState.DISABLED
                            self.__subscan_region_value.value = None

                        def display_removed(subscan_graphic):
                            self.__remove_one_subscan_graphic(subscan_graphic)

                        remove_region_graphic_event_listener = subscan_graphic.about_to_be_removed_event.listen(functools.partial(graphic_removed, subscan_graphic))
                        display_about_to_be_removed_listener = display_item.about_to_be_removed_event.listen(functools.partial(display_removed, subscan_graphic))
                        self.__subscan_graphic_trackers.append((subscan_graphic, subscan_graphic_property_changed_listener, remove_region_graphic_event_listener, display_about_to_be_removed_listener))
                        display_item.add_graphic(subscan_graphic)
            # apply new value to any existing subscan graphics
            for subscan_graphic, l1, l2, l3 in self.__subscan_graphic_trackers:
                subscan_graphic.bounds = subscan_region
                subscan_graphic.rotation = subscan_rotation
        else:
            # remove any graphics
            for subscan_graphic, subscan_graphic_property_changed_listener, remove_region_graphic_event_listener, display_about_to_be_removed_listener in self.__subscan_graphic_trackers:
                subscan_graphic_property_changed_listener.close()
                remove_region_graphic_event_listener.close()
                display_about_to_be_removed_listener.close()
                subscan_graphic.container.remove_graphic(subscan_graphic)
            self.__subscan_graphic_trackers = list()

    def __remove_one_subscan_graphic(self, subscan_graphic_to_remove):
        subscan_graphic_trackers = list()
        for subscan_graphic, subscan_graphic_property_changed_listener, remove_region_graphic_event_listener, display_about_to_be_removed_listener in self.__subscan_graphic_trackers:
            if subscan_graphic_to_remove != subscan_graphic:
                subscan_graphic_trackers.append((subscan_graphic, subscan_graphic_property_changed_listener, remove_region_graphic_event_listener, display_about_to_be_removed_listener))
            else:
                subscan_graphic_property_changed_listener.close()
                remove_region_graphic_event_listener.close()
                display_about_to_be_removed_listener.close()
        self.__subscan_graphic_trackers = subscan_graphic_trackers


class ProbeViewController:
    """Manage a ProbeView for each instrument (STEMController) that gets registered."""

    def __init__(self, document_model, event_loop):
        assert event_loop is not None
        self.__document_model = document_model
        self.__event_loop = event_loop
        # be sure to keep a reference or it will be closed immediately.
        self.__instrument_added_event_listener = None
        self.__instrument_removed_event_listener = None
        self.__instrument_added_event_listener = HardwareSource.HardwareSourceManager().instrument_added_event.listen(self.register_instrument)
        self.__instrument_removed_event_listener = HardwareSource.HardwareSourceManager().instrument_removed_event.listen(self.unregister_instrument)
        for instrument in HardwareSource.HardwareSourceManager().instruments:
            self.register_instrument(instrument)

    def close(self):
        # close will be called when the extension is unloaded. in turn, close any references so they get closed. this
        # is not strictly necessary since the references will be deleted naturally when this object is deleted.
        self.__instrument_added_event_listener.close()
        self.__instrument_added_event_listener = None
        self.__instrument_removed_event_listener.close()
        self.__instrument_removed_event_listener = None

    def register_instrument(self, instrument):
        # if this is a stem controller, add a probe view
        if hasattr(instrument, "_probe_position_value"):
            instrument._probe_view = ProbeView(instrument, self.__document_model, self.__event_loop)
        if hasattr(instrument, "_subscan_region_value"):
            instrument._subscan_view = SubscanView(instrument, self.__document_model, self.__event_loop)

    def unregister_instrument(self, instrument):
        if hasattr(instrument, "_probe_view"):
            instrument._probe_view.close()
            instrument._probe_view = None
        if hasattr(instrument, "_subscan_view"):
            instrument._subscan_view.close()
            instrument._subscan_view = None


# the plan is to migrate away from the hardware manager as a registration system.
# but keep this here until that migration is complete.

def component_registered(component, component_types):
    if "stem_controller" in component_types:
        HardwareSource.HardwareSourceManager().register_instrument(component.instrument_id, component)

def component_unregistered(component, component_types):
    if "stem_controller" in component_types:
        HardwareSource.HardwareSourceManager().unregister_instrument(component.instrument_id)

component_registered_listener = Registry.listen_component_registered_event(component_registered)
component_unregistered_listener = Registry.listen_component_unregistered_event(component_unregistered)

for component in Registry.get_components_by_type("stem_controller"):
    component_registered(component, {"stem_controller"})


"""
from nion.swift.model import HardwareSource
s = HardwareSource.HardwareSourceManager().get_instrument_by_id('usim_stem_controller')
s._subscan_region_value.value = ((0.1, 0.1), (0.2, 0.3))
"""
