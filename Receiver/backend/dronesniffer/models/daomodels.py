from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

__all__ = ["RemoteId"]


class RemoteId(SQLModel, table=True):
    """
    Represents a Remote ID (RID) object. It contains all the properties needed by the different RID formats.

    Attributes:
        id (int, optional): ID associated with the packet given by the database.
        oui (str): Oui of the Manufacturer.
        serial_number (str, optional): Serial number of the drone.
        timestamp (datetime, optional): Time packets has been sent.
        lng (float, optional): Longitude of drone. Value between -180 and 180.
        lat (float, optional): Latitude of drone. Value between -90 and 90.
        altitude (float, optional): Altitude of drone (meter above sea level)
        height (float, optional): Height above ground of drone.
        x_speed(float, optional): Speed of drone in direction x.
        y_speed(float, optional): Speed of drone in direction y.
        z_speed(float, optional): Speed of drone in direction z.
        yaw(float, optional): Yaw angle of drone.
        pilot_lng (float, optional): Longitude of pilot. Value between -180 and 180.
        pilot_lat (float, optional): Latitude of pilot. Value between -90 and 90.
        home_lng (float, optional): Longitude of home (drone starting point). Value between -180 and 180.
        home_lat (float, optional): Latitude of home (drone starting point). Value between -90 and 90.
        uuid (str): User unique identifier as 20-digit string.
        spoofed (bool): Assumption that RID is spoofed.
    """
    # Database fields
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Identification fields
    oui: str
    uuid: str = Field(index=True)
    serial_number: Optional[str] = Field(default=None, index=True)  # 16 length (alphanumerical string)
    timestamp: Optional[datetime] = None
    spoofed: Optional[bool] = None
    
    operational_status : Optional[int] = None  # ASD-STAN operational status

    accuracy_horizontal : Optional[float] = None  # ASD-STAN horizontal accuracy
    accuracy_vertical : Optional[float] = None  # ASD-STAN vertical accuracy
    accuracy_velocity : Optional[float] = None  # ASD-STAN velocity accuracy

    flight_purpose : Optional[str] = None  # ASD-STAN flight purpose
    ua_type : Optional[int] = None  # ASD-STAN drone type
    drone_class : Optional[int] = None  # ASD-STAN drone class

    # Drone position and orientation
    lat: Optional[float] = Field(default=None, le=90, ge=-90)
    lng: Optional[float] = Field(default=None, le=180, ge=-180)
    altitude: Optional[int] = None
    height: Optional[int] = None

    # Drone movement (DJI only)
    x_speed: Optional[float] = None
    y_speed: Optional[float] = None
    z_speed: Optional[float] = None

    # Drone rotation (DJI only)
    pitch: Optional[float] = None
    roll: Optional[float] = None
    yaw: Optional[float] = None

    # Pilot position
    pilot_lat: Optional[float] = Field(default=None, le=90, ge=-90)
    pilot_lng: Optional[float] = Field(default=None, le=180, ge=-180)
    pilot_altitude: Optional[int] = None
    pilot_registration_number : Optional[str] = None  # Pilot registration number (ADS-STAN Operator ID)

    # Home position
    home_lat: Optional[float] = Field(default=None, le=90, ge=-90)
    home_lng: Optional[float] = Field(default=None, le=180, ge=-180)

    def add_home_loc(self, drone_dict: dict) -> None:
        """
        Method to add home location of a drone flight. If the serial number of a drone has already been captured
        and therefore a home location exists. This value will be reused to set the home location. If the serial
        number has not been detected yet a new entry will be made into the drone_dict param and set the drones home
        location as well.

        Args:
            drone_dict: Dict containing serial number as the key and home location as value.
        """
        serial = self.serial_number
        if serial not in drone_dict:
            drone_dict[serial] = (self.lat, self.lng)
            self.home_lat = self.lat
            self.home_lng = self.lng
        else:
            self.home_lat, self.home_lng = drone_dict[serial]
