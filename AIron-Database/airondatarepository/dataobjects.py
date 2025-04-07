from dataclasses import dataclass
from airondatarepository.dataenums import ScheduleType
import datetime

@dataclass
class User:
    full_name: str
    email: str
    password: str
    inputs: list
    schedules: list

@dataclass
class Schedule:
    id: str
    name: str
    type: ScheduleType
    json: str
    created_on: str