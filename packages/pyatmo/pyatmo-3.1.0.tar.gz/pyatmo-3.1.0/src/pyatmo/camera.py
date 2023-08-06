import imghdr
import time
from urllib.error import URLError

from .exceptions import InvalidHome, NoDevice
from .helpers import _BASE_URL, LOG, postRequest

_GETHOMEDATA_REQ = _BASE_URL + "api/gethomedata"
_GETCAMERAPICTURE_REQ = _BASE_URL + "api/getcamerapicture"
_GETEVENTSUNTIL_REQ = _BASE_URL + "api/geteventsuntil"
_SETPERSONSAWAY_REQ = _BASE_URL + "api/setpersonsaway"
_SETPERSONSHOME_REQ = _BASE_URL + "api/setpersonshome"


class CameraData:
    """
    List the Netatmo camera informations
        (Homes, cameras, smoke detectors, modules, events, persons)
    Args:
        authData (ClientAuth):
            Authentication information with a working access Token
    """

    def __init__(self, authData, size=15):
        self.getAuthToken = authData.accessToken
        postParams = {"access_token": self.getAuthToken, "size": size}
        resp = postRequest(_GETHOMEDATA_REQ, postParams)
        if resp is None:
            raise URLError("No device data returned by Netatmo server")
        self.rawData = resp["body"].get("homes")
        if not self.rawData:
            raise NoDevice("No device data available")
        self.homes = {d["id"]: d for d in self.rawData}
        if not self.homes:
            raise NoDevice("No device available")
        self.persons = {}
        self.events = {}
        self.outdoor_events = {}
        self.cameras = {}
        self.smokedetectors = {}
        self.modules = {}
        self.lastEvent = {}
        self.outdoor_lastEvent = {}
        self.types = {}
        self.default_home = None
        self.default_home_id = None
        self.default_camera = None
        self.default_smokedetector = None
        for item in self.rawData:
            homeId = item.get("id")
            nameHome = item.get("name")
            if not nameHome:
                nameHome = "Unknown"
                self.homes[homeId]["name"] = nameHome
            if not homeId:
                LOG.error('No key ["id"] in %s', item.keys())
                continue
            if homeId not in self.cameras:
                self.cameras[homeId] = {}
            if homeId not in self.smokedetectors:
                self.smokedetectors[homeId] = {}
            if homeId not in self.types:
                self.types[homeId] = {}
            for p in item["persons"]:
                self.persons[p["id"]] = p
            if "events" in item:
                if not self.default_home and not self.default_home_id:
                    self.default_home = item["name"]
                    self.default_home_id = item["id"]
                for e in item["events"]:
                    if e["type"] == "outdoor":
                        if e["camera_id"] not in self.outdoor_events:
                            self.outdoor_events[e["camera_id"]] = {}
                        self.outdoor_events[e["camera_id"]][e["time"]] = e
                    elif e["type"] != "outdoor":
                        if e["camera_id"] not in self.events:
                            self.events[e["camera_id"]] = {}
                        self.events[e["camera_id"]][e["time"]] = e
            for c in item["cameras"]:
                self.cameras[homeId][c["id"]] = c
                if c["type"] == "NACamera" and "modules" in c:
                    for m in c["modules"]:
                        self.modules[m["id"]] = m
                        self.modules[m["id"]]["cam_id"] = c["id"]
            for s in item["smokedetectors"]:
                self.smokedetectors[homeId][s["id"]] = s
            for t in item["cameras"]:
                self.types[homeId][t["type"]] = t
            for t in item["smokedetectors"]:
                self.types[homeId][t["type"]] = t
        for camera in self.events:
            self.lastEvent[camera] = self.events[camera][
                sorted(self.events[camera])[-1]
            ]
        for camera in self.outdoor_events:
            self.outdoor_lastEvent[camera] = self.outdoor_events[camera][
                sorted(self.outdoor_events[camera])[-1]
            ]
        if self.modules != {}:
            self.default_module = list(self.modules.values())[0]["name"]
        else:
            self.default_module = None
        if self.default_home is not None and self.cameras[self.default_home_id]:
            self.default_camera = list(self.cameras[self.default_home_id].values())[0]

    def homeById(self, hid):
        return None if hid not in self.homes else self.homes[hid]

    def homeByName(self, home=None):
        if not home:
            return self.homeByName(self.default_home)
        for key, value in self.homes.items():
            if value["name"] == home:
                return self.homes[key]
        raise InvalidHome()

    def getHomeName(self, home_id=None):
        if home_id is None:
            home_id = self.default_home_id
        for key, value in self.homes.items():
            if value["id"] == home_id:
                return self.homes[key]["name"]
        raise InvalidHome("Invalid Home ID %s" % home_id)

    def gethomeId(self, home=None):
        if not home:
            home = self.default_home
        for key, value in self.homes.items():
            if value["name"] == home:
                return self.homes[key]["id"]
        raise InvalidHome("Invalid Home %s" % home)

    def cameraById(self, cid):
        for home, _ in self.cameras.items():
            if cid in self.cameras[home]:
                return self.cameras[home][cid]
        return None

    def cameraByName(self, camera=None, home=None, home_id=None):
        if home_id is None:
            if home is None:
                hid = self.default_home_id
            else:
                try:
                    hid = self.homeByName(home)["id"]
                except InvalidHome:
                    LOG.debug("Invalid home %s", home)
                    return None
        else:
            hid = home_id
        if camera is None and home is None and home_id is None:
            return self.default_camera
        if not (home_id or home) and camera:
            for h_id, cam_ids in self.cameras.items():
                for cam_id in cam_ids:
                    if self.cameras[h_id][cam_id]["name"] == camera:
                        return self.cameras[h_id][cam_id]
        elif hid and camera:
            hid = self.homeByName(home)["id"]
            if hid not in self.cameras:
                return None
            for cam_id in self.cameras[hid]:
                if self.cameras[hid][cam_id]["name"] == camera:
                    return self.cameras[hid][cam_id]
        else:
            return list(self.cameras[hid].values())[0]

    def moduleById(self, mid):
        return None if mid not in self.modules else self.modules[mid]

    def moduleByName(self, module=None, camera=None, home=None):
        if not module:
            if self.default_module:
                return self.moduleByName(self.default_module)
            return None
        cam = None
        if camera or home:
            cam = self.cameraByName(camera, home)
            if not cam:
                return None
        for key, value in self.modules.items():
            if value["name"] == module:
                if cam and value["cam_id"] != cam["id"]:
                    return None
                return self.modules[key]
        return None

    def smokedetectorById(self, sid):
        for home, sd in self.smokedetectors.items():
            if sid in self.smokedetectors[home]:
                return self.smokedetectors[home][sid]
        return None

    def smokedetectorByName(self, smokedetector=None, home=None, home_id=None):
        if home_id is None:
            if home is None:
                hid = self.default_home_id
            else:
                try:
                    hid = self.homeByName(home)["id"]
                except InvalidHome:
                    LOG.debug("Invalid home %s", home)
                    return None
        else:
            hid = home_id
        if smokedetector is None and home is None and home_id is None:
            return self.default_smokedetector
        elif not (home_id or home) and smokedetector:
            for h_id, cam_ids in self.smokedetectors.items():
                for cam_id in cam_ids:
                    if self.smokedetectors[h_id][cam_id]["name"] == smokedetector:
                        return self.smokedetectors[h_id][cam_id]
        elif hid and smokedetector:
            hid = self.homeByName(home)["id"]
            if hid not in self.smokedetectors:
                return None
            for cam_id in self.smokedetectors[hid]:
                if self.smokedetectors[hid][cam_id]["name"] == smokedetector:
                    return self.smokedetectors[hid][cam_id]
        else:
            return list(self.smokedetectors[hid].values())[0]

    def cameraType(self, camera=None, home=None, cid=None, home_id=None):
        """
        Return the type of a given camera.
        """
        cameratype = None
        if cid:
            camera_data = self.cameraById(cid)
        else:
            camera_data = self.cameraByName(camera=camera, home=home, home_id=home_id)
        if camera_data:
            cameratype = camera_data["type"]
        return cameratype

    def cameraUrls(self, camera=None, home=None, cid=None, home_id=None):
        """
        Return the vpn_url and the local_url (if available) of a given camera
        in order to access its live feed
        """
        local_url = None
        vpn_url = None
        if cid:
            camera_data = self.cameraById(cid)
        elif home_id:
            camera_data = self.cameraByName(camera=camera, home_id=home_id)
        else:
            camera_data = self.cameraByName(camera=camera, home=home)

        if camera_data:
            vpn_url = camera_data.get("vpn_url")
            if camera_data.get("is_local"):
                try:
                    resp = postRequest("{0}/command/ping".format(vpn_url), {})
                    temp_local_url = resp["local_url"]
                except URLError:
                    return None, None

                try:
                    resp = postRequest("{0}/command/ping".format(temp_local_url), {})
                    if temp_local_url == resp["local_url"]:
                        local_url = temp_local_url
                except URLError:
                    pass
        return vpn_url, local_url

    def personsAtHome(self, home=None, home_id=None):
        """
        Return the list of known persons who are currently at home
        """
        if home_id:
            home_data = self.homeById(home_id)
        else:
            if not home:
                home = self.default_home
            home_data = self.homeByName(home)
        atHome = []
        for p in home_data["persons"]:
            # Only check known personshome
            if "pseudo" in p:
                if not p["out_of_sight"]:
                    atHome.append(p["pseudo"])
        return atHome

    def setPersonsHome(self, person_ids, home_id):
        """
        Mark persons as home.
        """
        postParams = {
            "access_token": self.getAuthToken,
            "home_id": home_id,
            "person_ids[]": person_ids,
        }
        resp = postRequest(_SETPERSONSHOME_REQ, postParams)
        return resp

    def setPersonsAway(self, person_id, home_id):
        """
        Mark a person as away or set the whole home to being empty.
        """
        postParams = {
            "access_token": self.getAuthToken,
            "home_id": home_id,
            "person_id": person_id,
        }
        resp = postRequest(_SETPERSONSAWAY_REQ, postParams)
        return resp

    def getPersonId(self, name):
        for pid, data in self.persons.items():
            if "pseudo" in data and name == data["pseudo"]:
                return pid
        return None

    def getCameraPicture(self, image_id, key):
        """
        Download a specific image (of an event or user face) from the camera
        """
        postParams = {
            "access_token": self.getAuthToken,
            "image_id": image_id,
            "key": key,
        }
        resp = postRequest(_GETCAMERAPICTURE_REQ, postParams)
        image_type = imghdr.what("NONE.FILE", resp)
        return resp, image_type

    def getProfileImage(self, name):
        """
        Retrieve the face of a given person
        """
        for p in self.persons:
            if "pseudo" in self.persons[p]:
                if name == self.persons[p]["pseudo"]:
                    image_id = self.persons[p]["face"]["id"]
                    key = self.persons[p]["face"]["key"]
                    return self.getCameraPicture(image_id, key)
        return None, None

    def updateEvent(self, event=None, home=None, devicetype=None, home_id=None):
        """
        Update the list of events
        """
        if not home_id:
            try:
                if not home:
                    home = self.default_home
                home_id = self.gethomeId(home)
            except InvalidHome:
                LOG.debug("Invalid Home %s", home)
                return None
        if devicetype == "NACamera":
            # for the Welcome camera
            if not event:
                # If no event is provided we need to retrieve the oldest of
                # the last event seen by each camera
                listEvent = {}
                for cam_id in self.lastEvent:
                    listEvent[self.lastEvent[cam_id]["time"]] = self.lastEvent[cam_id]
                event = listEvent[sorted(listEvent)[0]]
        if devicetype == "NOC":
            # for the Presence camera
            if not event:
                # If no event is provided we need to retrieve the oldest of
                # the last event seen by each camera
                listEvent = {}
                for cam_id in self.outdoor_lastEvent:
                    listEvent[
                        self.outdoor_lastEvent[cam_id]["time"]
                    ] = self.outdoor_lastEvent[cam_id]
                event = listEvent[sorted(listEvent)[0]]
        if devicetype == "NSD":
            # for the smoke detector
            if not event:
                # If no event is provided we need to retrieve the oldest of
                # the last event by each smoke detector
                listEvent = {}
                for sid in self.outdoor_lastEvent:
                    listEvent[
                        self.outdoor_lastEvent[sid]["time"]
                    ] = self.outdoor_lastEvent[sid]
                event = listEvent[sorted(listEvent)[0]]

        postParams = {
            "access_token": self.getAuthToken,
            "home_id": home_id,
            "event_id": event["id"],
        }
        resp = postRequest(_GETEVENTSUNTIL_REQ, postParams)
        eventList = resp["body"]["events_list"]
        for e in eventList:
            if e["type"] == "outdoor":
                if e["camera_id"] not in self.outdoor_events:
                    self.outdoor_events[e["camera_id"]] = {}
                self.outdoor_events[e["camera_id"]][e["time"]] = e
            elif e["type"] != "outdoor":
                if e["camera_id"] not in self.events:
                    self.events[e["camera_id"]] = {}
                self.events[e["camera_id"]][e["time"]] = e
        for camera in self.events:
            self.lastEvent[camera] = self.events[camera][
                sorted(self.events[camera])[-1]
            ]
        for camera in self.outdoor_events:
            self.outdoor_lastEvent[camera] = self.outdoor_events[camera][
                sorted(self.outdoor_events[camera])[-1]
            ]

    def personSeenByCamera(self, name, home=None, camera=None, exclude=0):
        """
        Evaluate if a specific person has been seen
        """
        try:
            cam_id = self.cameraByName(camera=camera, home=home)["id"]
        except TypeError:
            LOG.error("personSeenByCamera: Camera name or home is unknown")
            return False
        # Check in the last event is someone known has been seen
        if exclude:
            limit = time.time() - exclude
            array_time_event = sorted(self.events[cam_id], reverse=True)
            for time_ev in array_time_event:
                if time_ev < limit:
                    return False
                if self.events[cam_id][time_ev]["type"] == "person":
                    person_id = self.events[cam_id][time_ev]["person_id"]
                    if "pseudo" in self.persons[person_id]:
                        if self.persons[person_id]["pseudo"] == name:
                            return True
        elif self.lastEvent[cam_id]["type"] == "person":
            person_id = self.lastEvent[cam_id]["person_id"]
            if "pseudo" in self.persons[person_id]:
                if self.persons[person_id]["pseudo"] == name:
                    return True
        return False

    def _knownPersons(self):
        known_persons = {}
        for p_id, p in self.persons.items():
            if "pseudo" in p:
                known_persons[p_id] = p
        return known_persons

    def knownPersons(self):
        return {pid: p["pseudo"] for pid, p in self._knownPersons().items()}

    def knownPersonsNames(self):
        names = []
        for _, p in self._knownPersons().items():
            names.append(p["pseudo"])
        return names

    def someoneKnownSeen(self, home=None, camera=None, exclude=0, cid=None):
        """
        Evaluate if someone known has been seen
        """
        if not cid:
            try:
                cid = self.cameraByName(camera=camera, home=home)["id"]
            except TypeError:
                LOG.error("someoneKnownSeen: Camera name or home is unknown")
                return False

        if exclude:
            limit = time.time() - exclude
            array_time_event = sorted(self.events[cid], reverse=True)
            for time_ev in array_time_event:
                if time_ev < limit:
                    return False
                if self.events[cid][time_ev]["type"] == "person":
                    if self.events[cid][time_ev]["person_id"] in self._knownPersons():
                        return True
        # Check in the last event if someone known has been seen
        elif self.lastEvent[cid]["type"] == "person":
            if self.lastEvent[cid]["person_id"] in self._knownPersons():
                return True
        return False

    def someoneUnknownSeen(self, home=None, camera=None, exclude=0, cid=None):
        """
        Evaluate if someone unknown has been seen
        """
        if not cid:
            try:
                cid = self.cameraByName(camera=camera, home=home)["id"]
            except TypeError:
                LOG.error("someoneUnknownSeen: Camera name or home is unknown")
                return False

        if exclude:
            limit = time.time() - exclude
            array_time_event = sorted(self.events[cid], reverse=True)
            for time_ev in array_time_event:
                if time_ev < limit:
                    return False
                if self.events[cid][time_ev]["type"] == "person":
                    if (
                        self.events[cid][time_ev]["person_id"]
                        not in self._knownPersons()
                    ):
                        return True
        # Check in the last event is someone known has been seen
        elif self.lastEvent[cid]["type"] == "person":
            if self.lastEvent[cid]["person_id"] not in self._knownPersons():
                return True
        return False

    def motionDetected(self, home=None, camera=None, exclude=0, cid=None):
        """
        Evaluate if movement has been detected
        """
        if not cid:
            try:
                cid = self.cameraByName(camera=camera, home=home)["id"]
            except TypeError:
                LOG.error("motionDetected: Camera name or home is unknown")
                return False

        if exclude:
            limit = time.time() - exclude
            array_time_event = sorted(self.events[cid], reverse=True)
            for time_ev in array_time_event:
                if time_ev < limit:
                    return False
                if self.events[cid][time_ev]["type"] == "movement":
                    return True
        elif self.lastEvent[cid]["type"] == "movement":
            return True
        return False

    def outdoormotionDetected(self, home=None, camera=None, offset=0, cid=None):
        """
        Evaluate if outdoor movement has been detected
        """
        if not cid:
            try:
                cid = self.cameraByName(camera=camera, home=home)["id"]
            except TypeError:
                LOG.error("outdoormotionDetected: Camera name or home is unknown")
                return False

        if cid in self.lastEvent:
            if self.lastEvent[cid]["type"] == "movement":
                if self.lastEvent[cid][
                    "video_status"
                ] == "recording" and self.lastEvent[cid]["time"] + offset > int(
                    time.time()
                ):
                    return True
        return False

    def humanDetected(self, home=None, camera=None, offset=0, cid=None):
        """
        Evaluate if a human has been detected
        """
        if not cid:
            try:
                cid = self.cameraByName(camera=camera, home=home)["id"]
            except TypeError:
                LOG.error("personSeenByCamera: Camera name or home is unknown")
                return False

        if self.outdoor_lastEvent[cid]["video_status"] == "recording":
            for e in self.outdoor_lastEvent[cid]["event_list"]:
                if e["type"] == "human" and e["time"] + offset > int(time.time()):
                    return True
        return False

    def animalDetected(self, home=None, camera=None, offset=0, cid=None):
        """
        Evaluate if an animal has been detected
        """
        if not cid:
            try:
                cid = self.cameraByName(camera=camera, home=home)["id"]
            except TypeError:
                LOG.error("animalDetected: Camera name or home is unknown")
                return False

        if self.outdoor_lastEvent[cid]["video_status"] == "recording":
            for e in self.outdoor_lastEvent[cid]["event_list"]:
                if e["type"] == "animal" and e["time"] + offset > int(time.time()):
                    return True
        return False

    def carDetected(self, home=None, camera=None, offset=0, cid=None):
        """
        Evaluate if a car has been detected
        """
        if not cid:
            try:
                cid = self.cameraByName(camera=camera, home=home)["id"]
            except TypeError:
                LOG.error("carDetected: Camera name or home is unknown")
                return False

        if self.outdoor_lastEvent[cid]["video_status"] == "recording":
            for e in self.outdoor_lastEvent[cid]["event_list"]:
                if e["type"] == "vehicle" and e["time"] + offset > int(time.time()):
                    return True
        return False

    def moduleMotionDetected(self, module=None, home=None, camera=None, exclude=0):
        """
        Evaluate if movement has been detected
        """
        try:
            mod = self.moduleByName(module, camera=camera, home=home)
            mod_id = mod["id"]
            cam_id = mod["cam_id"]
        except TypeError:
            LOG.error(
                "moduleMotionDetected: Module name or" "Camera name or home is unknown"
            )
            return False

        if exclude:
            limit = time.time() - exclude
            array_time_event = sorted(self.events[cam_id], reverse=True)
            for time_ev in array_time_event:
                if time_ev < limit:
                    return False
                if (
                    self.events[cam_id][time_ev]["type"] == "tag_big_move"
                    or self.events[cam_id][time_ev]["type"] == "tag_small_move"
                ) and self.events[cam_id][time_ev]["module_id"] == mod_id:
                    return True
        elif (
            self.lastEvent[cam_id]["type"] == "tag_big_move"
            or self.lastEvent[cam_id]["type"] == "tag_small_move"
        ) and self.lastEvent[cam_id]["module_id"] == mod_id:
            return True
        return False

    def moduleOpened(self, module=None, home=None, camera=None, exclude=0):
        """
        Evaluate if module status is open
        """
        try:
            mod = self.moduleByName(module, camera=camera, home=home)
            mod_id = mod["id"]
            cam_id = mod["cam_id"]
        except TypeError:
            LOG.error("moduleOpened: Camera name, or home, or module is unknown")
            return False

        if exclude:
            limit = time.time() - exclude
            array_time_event = sorted(self.events[cam_id], reverse=True)
            for time_ev in array_time_event:
                if time_ev < limit:
                    return False
                if (
                    self.events[cam_id][time_ev]["type"] == "tag_open"
                    and self.events[cam_id][time_ev]["module_id"] == mod_id
                ):
                    return True
        elif (
            self.lastEvent[cam_id]["type"] == "tag_open"
            and self.lastEvent[cam_id]["module_id"] == mod_id
        ):
            return True
        return False
